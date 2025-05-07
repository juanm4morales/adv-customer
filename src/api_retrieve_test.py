import os
from dotenv import load_dotenv  # Importa la biblioteca dotenv
import requests

# Carga las variables de entorno desde el archivo .env
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
            bot_info = response.json()
            return bot_info
        except requests.exceptions.RequestException as request_error:
            raise RuntimeError(f"Request error: {request_error}") from request_error
        except ValueError as value_error:
            raise RuntimeError(f"Error processing the response: {value_error}") from value_error
        

print(fetch_bot_info("36"))