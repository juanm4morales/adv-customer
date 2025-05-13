import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .states import State
from .nodes import CustomerNode, ChatbotNode, should_continue

import adv_customer.prompts as prompts
from .schemes import ResponseFormatter
from adv_customer.utils.prompt_utils import filter_prompt_variables, generate_random_customer_profile
from adv_customer.utils.serializer import persist_conversation, serialize_messages

load_dotenv()

API_KEY = os.getenv("KLARI_API_KEY")

class ConversationSim:
    """ 
    Class to simulate a customer agent that interacts with a chatbot.
    This class is designed to generate realistic customer interactions based on the chatbot's capabilities and the customer's profile.
    """
    def __init__(self, customer_id: str, customer_info: dict, agent_info:dict, max_messages:int = 30):
        self.customer_id = customer_id
        self.customer_profile = generate_random_customer_profile()
        try:
            self.agent_id = agent_info["id"]
            self.bot_id = agent_info["bot_id"]
            agent_role = agent_info["role"]
            agent_prompt = agent_info["prompt_agent"]["prompt"]
        except KeyError as e:
            raise KeyError(f"Missing expected key in agent_info: {e}") from e
        self.customer_info = customer_info
        self.customer_prompt = self._generate_prompt(agent_role)
        self.max_messages = max_messages
        self.graph = self._graph_builder()
        self.config_checkpoint = {"configurable": {"thread_id": "1"}}

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

    def _generate_prompt(self, agent_role: str):
        """
        Generate the prompt for the customer agent based on the bot's capabilities and the customer's profile.
        """
        system_prompt_template = prompts.CUSTOMER_SIM_PROMPT_2
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_template),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        variables = {
            "CUSTOMER_INFO": self.customer_info,
            "ADV_AGENT_ROLE": agent_role,
            "CUSTOMER_PROFILE": self.customer_profile,
        }
        variables = filter_prompt_variables(prompt_template, variables)
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
        llm = llm.with_structured_output(ResponseFormatter)
        customer_sim_runnable = self.customer_prompt | llm
        # Graph
        builder = StateGraph(State)
        # Nodes
        builder.add_node(CustomerNode.name, CustomerNode(customer_sim_runnable))
        builder.add_node(ChatbotNode.name, ChatbotNode(self.bot_id))
        # Edges
        builder.add_edge(START, CustomerNode.name)
        builder.add_edge(CustomerNode.name, ChatbotNode.name)
        builder.add_conditional_edges(ChatbotNode.name, lambda state: should_continue(state, self.max_messages))
        
        checkpointer = InMemorySaver()
        graph = builder.compile(checkpointer=checkpointer)
        return graph

    def simulate_conversation(self, initial_state=None, verbose=False):
        """
        Simulate a conversation with the chatbot.
        This method initiates the conversation and streams the responses from the chatbot.

        Args:
            initial_state (dict, optional): Initial state for the conversation. Defaults to None.
            verbose (bool, optional): If True, prints the conversation in real-time. Defaults to False.
        """
        if initial_state is None:
            initial_state = {
                "messages": [],
                "closed": False,
            }
        state = None
        if verbose:
            print("Iniciando simulación de CustomerSim...\n")
            for chunk in self.graph.stream(initial_state, self.config_checkpoint, stream_mode="values"):
                if chunk.get("closed"):
                    print(chunk["messages"][-1])
                    state = chunk
                if chunk.get("messages"):  # Check if the list is not empty
                    last_message = chunk["messages"][-1]
                    last_message.pretty_print()
            print("Fin de la conversación.")
        else:
            state = self.graph.invoke(initial_state, self.config_checkpoint)
        return serialize_messages(state["messages"])
    
    def save_conversation(self, output_dir="conversations"):
        state = self.graph.get_state(self.config_checkpoint)
        filename = f"{self.customer_id}_{self.bot_id}_{self.current_agent_id}.txt"
        file_path = os.path.join(output_dir, filename)
        header_lines = [
            f"Customer ID: {self.customer_id}",
            f"Bot ID: {self.bot_id}",
            f"Agent ID: {self.current_agent_id}",
            f"Customer info: {self.customer_info}",
            f"Customer profile: {self.customer_profile}"
        ]
        header = "\n".join(header_lines)
        messages = state.values["messages"]
        persist_conversation(messages, file_path, header)