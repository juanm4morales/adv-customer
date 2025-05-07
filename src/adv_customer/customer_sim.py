import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from states import State
from nodes import CustomerNode, ChatbotNode, should_continue

import prompts
import schemes
from utils.prompt_utils import safe_filter, random_customer_attributes
from utils.persistence import persist_conversation

load_dotenv()

API_KEY = os.getenv("KLARI_API_KEY")

class CustomerSim:
    """ 
    Class to simulate a customer agent that interacts with a chatbot.
    This class is designed to generate realistic customer interactions based on the chatbot's capabilities and the customer's profile.
    """

    def __init__(self, customer_id: str, customer_name: str, bot_id: str, agent_id: str = None):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_profile = random_customer_attributes()
        self.bot_id = bot_id
        self.bot_info = self._fetch_bot_info()
        self.agents_info = {
            agent["id"]: {
                "role": agent.get("role", "unknown"),
                "prompt": agent["prompt_agent"]["prompt"]
            }
            for idx, agent in enumerate(self.bot_info)
        }
    
        if agent_id is None:
            self.current_agent_id = self._select_agent()
        else:
            if agent_id not in self.agents_info:
                raise ValueError(f"Agent with id {agent_id} not found in agents_info.")
            self.current_agent_id = agent_id
        
        self.customer_info = self._generate_customer_info()
        self.customer_prompt = self._generate_prompt()
        self.graph = self._graph_builder()
        self.config_checkpoint = {"configurable": {"thread_id": "1"}}
        
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
            response.raise_for_status()
            bot_info = response.json()
            return bot_info
        except requests.exceptions.RequestException as request_error:
            raise RuntimeError(f"Request error: {request_error}") from request_error
        except ValueError as value_error:
            raise RuntimeError(f"Error processing the response: {value_error}") from value_error
    
    def _select_agent(self):
        """
        List available agents from self.agents_info and allow the user to select one by ID.
        """
        if not self.agents_info:
            raise ValueError("No agents available for selection.")
        
        print("\n╔═══════════════════════╗")
        print("║  Agentes disponibles  ║")
        print("╚═══════════════════════╝")
        for agent_id, agent in self.agents_info.items():
            print(f" - [ ID {agent_id} ] {agent['role']} ")

        while True:
            try:
                choice = int(input("Selecciona el ID del agente: "))
                if choice in self.agents_info:
                    return choice
                else:
                    print("Selección inválida. Por favor ingrese un ID válido.")
            except ValueError:
                print("Entrada inválida. Por favor intente nuevamente.")
                
    def _generate_customer_attr_names(self):
        llm = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens=1000)
        prompt = prompts.CUSTOMER_INFO_PROMPT.format(
            BOT_AGENT_PROMPT=self.agents_info[self.current_agent_id]["prompt"],
            #BOT_AGENT_ROLE=self.agents_info[self.current_agent_id]["role"]
        )
        attr_names = llm.with_structured_output(schemes.CustomerAttributes).invoke(prompt)
        
        if hasattr(attr_names, "attributes"):
            return attr_names.attributes
        else:
            raise TypeError("El formato de retorno de CustomerAttributes no es válido.")

    def _generate_customer_info(self):
        attr_names = self._generate_customer_attr_names()    
        customer_info = {}
        print("\nPor favor, ingrese los valores para los siguientes atributos del cliente:")
        for attr_name in attr_names:
            value = input(f" - {attr_name}: ")
            customer_info[attr_name] = value
        return customer_info

    def _generate_prompt(self):
        """
        Generate the prompt for the customer agent based on the bot's capabilities and the customer's profile.
        """
        system_prompt_template = prompts.CUSTOMER_SIM_PROMPT_3
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_template),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        agent = self.agents_info[self.current_agent_id]
        # customer_role = roles.roles_dict[agent["role"]]
        agent_role = agent["role"]
        variables = {
            "NAME": self.customer_name,
            "CUSTOMER_INFO": self.customer_info,
            "ADV_AGENT_ROLE": agent_role,
            "CUSTOMER_PROFILE": self.customer_profile,
        }
        variables = safe_filter(prompt_template, variables)
        prompt = prompt_template.partial(**variables)
        
        return prompt
    
    def swap_agent(self, new_agent_id: str):
        """
        Swap the current agent with a new one.
        This method allows changing the agent during the simulation.
        It updates the current agent ID and rebuilds the state graph with the new agent's prompt.

        Args:
            new_agent_id (str): The ID of the new agent to swap in.

        Raises:
            ValueError: If the new_agent_id does not exist in agents_info.
        """
        if new_agent_id not in self.agents_info:
            raise ValueError(f"El agente con ID {new_agent_id} no existe.")
        
        self.current_agent_id = new_agent_id
        self.customer_prompt = self._generate_prompt()
        self.graph = self._graph_builder()
    
    def _graph_builder(self):
        """
        Build the state graph for the customer simulation.
        """
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, max_tokens=2000)
        llm = llm.with_structured_output(schemes.ResponseFormatter)
        customer_sim_runnable = self.customer_prompt | llm
        # Graph
        builder = StateGraph(State)
        # Nodes
        builder.add_node(CustomerNode.name, CustomerNode(customer_sim_runnable))
        builder.add_node(ChatbotNode.name, ChatbotNode(self.bot_id))
        # Edges
        builder.add_edge(START, CustomerNode.name)
        builder.add_conditional_edges(CustomerNode.name, should_continue)
        builder.add_edge(ChatbotNode.name, CustomerNode.name)
        checkpointer = InMemorySaver()
        graph = builder.compile(checkpointer=checkpointer)
        return graph

    def simulate_conversation(self, initial_state=None):
        """
        Simula la conversación completa hasta que finalice.
        """
        
        if initial_state is None:
            initial_state = {
                "messages": [],
                "closed": False,
            }
        print("Iniciando simulación de CustomerSim...\n")
        print("\n" + "="*70)
        for chunk in self.graph.stream(initial_state, self.config_checkpoint, stream_mode="updates"):
            if END not in chunk:
                print(chunk)
                print("\n" + "="*70)
            else:
                print("Fin de la conversación.")
                break
    
    def save_conversation(self, output_dir="conversations"):
        state = self.graph.get_state(self.config_checkpoint)
        filename = f"{self.customer_id}_{self.bot_id}_{self.current_agent_id}.txt"
        file_path = os.path.join(output_dir, filename)
        header_lines = [
            f"Customer ID: {self.customer_id}",
            f"Bot ID: {self.bot_id}",
            f"Agent ID: {self.current_agent_id}",
            f"Customer name: {self.customer_name}",
            f"Customer info: {self.customer_info}",
            f"Customer profile: {self.customer_profile}"
        ]
        header = "\n".join(header_lines)
        messages = state.values["messages"]
        persist_conversation(messages, file_path, header)
