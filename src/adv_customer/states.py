from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    State of the customer simulation.
    It contains the messages exchanged between the customer and the chatbot,
    the ID of the current agent, and whether the conversation is closed.
    """
    messages: Annotated[list, add_messages]
    closed: bool
