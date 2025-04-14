from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage
from state import State

class CustomerNode:
    """
    Node representing a customer agent in the state graph.
    This node interacts with the chatbot and simulates customer behavior.
    It is responsible for generating customer messages and sending them to the chatbot.
    """
    def __init__(self, runnable: Runnable):
        self.runnable = runnable
    
    def __call__(self, state: State):
        """
        Run the customer node with the given state.
        """
        messages = state["messages"]
        response = self.runnable.invoke({"messages": messages})
        return {"messages": [AIMessage(content=response.content)]}

class GenerateObjectives:
    """
    Node representing the generation of customer objectives.
    This node is responsible for generating objectives based on the customer's profile and the chatbot's capabilities.
    It uses a runnable to generate the objectives and returns them in the state.
    """
        
    def __init__(self, runnable: Runnable):
        self.runnable = runnable
    
    def __call__(self, state: State):
        """
        Run the customer node with the given state.
        """
        messages = state["messages"]
        response = self.runnable.invoke({"messages": messages})
        return {"messages": [AIMessage(content=response.content)]}
        
        