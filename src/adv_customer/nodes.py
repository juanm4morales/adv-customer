from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage, HumanMessage
from .states import State
import requests
import os

CUSTOMER_NODE = "customer_node"
CHATBOT_NODE = "chatbot_node"

class CustomerNode:
    """
    Node representing a customer agent in the state graph.
    This node interacts with the chatbot and simulates customer behavior.
    It is responsible for generating customer messages and sending them to the chatbot.
    """
    name = CUSTOMER_NODE
    def __init__(self, runnable: Runnable):
        self.runnable = runnable
    
    def __call__(self, state: State):
        """
        Run the customer node with the given state.
        """
        messages = state["messages"]
        response = self.runnable.invoke({"messages": messages})
        message = response.message
        closed = response.closed
        return {"messages": [AIMessage(content=message)], "closed": closed}

class ChatbotNode:
    """
    Node representing a chatbot interaction.
    """
    name = CHATBOT_NODE
    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        # Read API key from environment variable
        try:
            self.api_key = os.environ["KLARI_BOT_API_KEY"]
        except KeyError:
            raise EnvironmentError("Environment variable 'KLARI_BOT_API_KEY' not set")

        self.base_url = "https://organization.klari.ai/api/v1/external"
        self.headers = {
            "accept": "application/json",
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json",
        }
        self.chat_id = self._create_chat()
    
    def _create_chat(self):
        """Create a new test chat and obtain chat_id"""
        
        payload = {"bot_id": self.bot_id}
        create_chat_url = f"{self.base_url}/create-test-chat"
        
        try:
            response = requests.post(create_chat_url, headers=self.headers, json=payload, timeout=30)
            data = response.json()
            if "_id" not in data:
                raise ValueError("'_id' not found in create-test-chat response")
            return data["_id"]
        except requests.exceptions.RequestException as request_error:
            raise RuntimeError(f"Request error: {request_error}") from request_error
        except ValueError as value_error:
            raise RuntimeError(f"Error processing the response: {value_error}") from value_error
    
    def __call__(self, state: State):
        """
        Run the chatbot node with the given state.
        """
        messages = state["messages"]
        last_message = messages[-1]
        if not isinstance(last_message, AIMessage):
            raise ValueError("Last message in state must be a AIMessage")
        payload = {
            "bot_id": self.bot_id,
            "question_user": last_message.content,
            "chat_id": self.chat_id
        }
        get_response_url = f"{self.base_url}/get-test-response"
        
        try:
            response = requests.post(get_response_url, headers=self.headers, json=payload, timeout=240)
            response.raise_for_status()
            response_data = response.json()
            
            if "message" in response_data:
                bot_message = response_data["message"]
            else:
                raise ValueError("No 'message' field found in API response")
            
            messages.append(HumanMessage(content=bot_message))
            return {"messages": messages}
        except requests.exceptions.RequestException as request_error:
            raise RuntimeError(f"Request error: {request_error}") from request_error
        except ValueError as value_error:
            raise RuntimeError(f"Error processing the response: {value_error}") from value_error

def should_continue(state: State, max_messages_size: int = 30):
    """
    Conditional edge that determines whether to continue the conversation.

    Args:
        state (State): The current state of the conversation.
        max_messages_size (int): The maximum number of messages allowed in the conversation.
    """
    messages = state["messages"]
    
    if state["closed"] or len(messages) > max_messages_size:
        # If the conversation is too long or solved, end the conversation
        return "end"
    
    # Otherwise we can just end
    return CHATBOT_NODE