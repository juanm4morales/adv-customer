from langchain_core.messages import AIMessage, HumanMessage
from typing import List, Union
import datetime
import os

def persist_conversation(messages: List[Union[AIMessage, HumanMessage]], file_path:str, header: str = None):
    """Persist the conversation to a file.
    This function appends the conversation messages to a file, creating the directory if it doesn't exist.

    Args:
        messages (List[Union[AIMessage, HumanMessage]]): _description_
        file_path (str): _description_
        header (str, optional): _description_. Defaults to None.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write("datetime: " + str(datetime.datetime.now())+"\n")
        if header is not None:
            f.write(header+"\n")
        f.write("Conversación\n")
        for message in messages:
            if isinstance(message, AIMessage):
                f.write("[AICustomer]:\n")
            elif isinstance(message, HumanMessage):
                f.write("[KlariBot]:\n")
            else:
                f.write("[?]:\n")
            f.write(message.content.strip()+"\n\n")
        f.write("="*40+"\n")

def serialize_messages(messages: List[Union[AIMessage, HumanMessage]]) -> List[dict]:
    """Serialize messages to a list of dictionaries.

    Args:
        messages (List[Union[AIMessage, HumanMessage]]): List of messages to serialize.

    Returns:
        List[dict]: List of serialized messages as dictionaries.
    """
    return [
        {
            "sender_type": "AIMessage" if isinstance(message, AIMessage) else "HumanMessage",
            "message": message.content
        }
        for message in messages
    ]