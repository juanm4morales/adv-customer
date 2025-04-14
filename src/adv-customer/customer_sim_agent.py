import os
import requests
from state import State
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from nodes import CustomerNode

API_KEY = os.getenv("KLARI_API_KEY")

class CustomerSim:
    """ 
    Class to simulate a customer agent that interacts with a chatbot.
    This class is designed to generate realistic customer interactions based on the chatbot's capabilities and the customer's profile.
    """

    def __init__(self, customer_id: str, customer_name: str, customer_info: dict, bot_id: str):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_info = customer_info
        self.bot_id = bot_id
        self.bot_info = self._fetch_bot_info()
        self.customer_prompt = self._generate_prompt()
        
        self.graph = self._graph_builder()   
    
    def _fetch_bot_info(self):
        """
        Fetch bot information from the API.
        This function retrieves the bot's capabilities and related agents information from the API.
        """
        
        if not API_KEY:
            raise ValueError("The API key is not set. Please set the 'KLARI_API_KEY' variable in the .env file.")


        url = f"https://api.klari.ai/api/v1/external/bots/{self.bot_id}/agents"
        headers = {
            "accept": "application/json",
            "X-Api-Key": API_KEY
        }

        try:
            response = requests.get(url, headers=headers)
            bot_info = response.json()
            return bot_info
        except requests.exceptions.RequestException as request_error:
            raise RuntimeError(f"Request error: {request_error}") from request_error
        except ValueError as value_error:
            raise RuntimeError(f"Error processing the response: {value_error}") from value_error
    
    def _generate_prompt(self):
        """
        Generate the prompt for the customer agent based on the bot's capabilities and the customer's profile.
        
        """
        system_prompt_template = """
        Tu nombre es {NAME}. Eres un cliente diseñado para conversar con un Chatbot cuya descripción y comportamiento están definidos en el siguiente prompt:

        {ADV_AGENT_PROMPT}
    
        Tus datos de cliente son:
        
        {CUSTOMER_INFO}

        Tu tarea es interactuar con este Chatbot asumiendo el rol de un cliente humano realista y coherente. Debes generar mensajes que simulen una conversación natural, con objetivos definidos y posibles dudas o reacciones según el contexto de la conversación.

        Características clave de tu comportamiento como cliente:
        - Adáptate a las capacidades del Chatbot, según lo indicado en su prompt.
        - Mantén coherencia narrativa: conserva tu identidad, necesidades, contexto y emociones a lo largo de la conversación.
        - Inicia la conversación con un mensaje que represente una necesidad, consulta o problema concreto.
        - Sé realista en tus expectativas, pero también creativo en los desvíos conversacionales si sirven para evaluar mejor al agente.

        Tu objetivo es poner a prueba la utilidad, claridad, y consistencia del Chatbot sin parecer artificial. No expliques que estás evaluando; actúa como un cliente genuino.

        Evita repetir exactamente la misma interacción.
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_template),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        agent_info = self.bot_info[0]
        agent_prompt = agent_info["prompt_agent"]["prompt"]
        prompt = prompt.partial(
            NAME=self.customer_name,
            CUSTOMER_INFO=self.customer_info,
            ADV_AGENT_PROMPT=agent_prompt
        )            
        return prompt
    
    def _graph_builder(self):
        """
        Build the state graph for the customer simulation.
        """
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, max_tokens=200)
        customer_sim_runnable = self.customer_prompt | llm
        builder = StateGraph(State)
        builder.add_node("customer_sim", CustomerNode(customer_sim_runnable))
        builder.add_edge(START, "customer_sim")
        builder.add_edge("customer_sim", END)
        
        memory = MemorySaver()
        graph = builder.compile()
        return graph

customerSim = CustomerSim(
    customer_id="12345",
    customer_name="John Doe",
    customer_info={"age": 30, "location": "USA"},
    bot_id="36"
)
i = 0
for chunk in customerSim.graph.stream({"messages": []}):
    # Print out all events aside from the final end chunk
    if END not in chunk:
        print(chunk)
        print("----")
    i += 1
    if i >= 5:
        break