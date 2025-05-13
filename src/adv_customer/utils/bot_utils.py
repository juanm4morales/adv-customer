import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import adv_customer.prompts as prompts
from adv_customer.schemes import CustomerAttributes

load_dotenv()

API_KEY = os.getenv("KLARI_API_KEY")

def fetch_bot_info(bot_id: str):
    """
    Fetch bot information from the API.
    This function retrieves the bot's capabilities and related agents information from the API.
    """
    if not API_KEY:
        raise ValueError("The API key is not set. Please set the 'KLARI_API_KEY' variable in the .env file.")

    url = f"https://api.klari.ai/api/v1/external/bots/{bot_id}/agents"
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

def generate_customer_attr_names(agent_prompt: str):
    """
    Generate customer attribute names based on the agent's prompt.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=1000)
    prompt = prompts.CUSTOMER_INFO_PROMPT_2.format(BOT_AGENT_PROMPT=agent_prompt)
    attr_names = llm.with_structured_output(CustomerAttributes).invoke(prompt)

    if hasattr(attr_names, "attributes"):
        return attr_names.attributes
    else:
        raise TypeError("El formato de retorno de CustomerAttributes no es válido.")