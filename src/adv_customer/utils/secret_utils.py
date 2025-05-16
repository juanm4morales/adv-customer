import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key(env_var) -> str:
    """
    Retrieves and validates a secret API key from environment variables.
    Raises a ValueError if not found or invalid.
    """
    api_key = os.getenv(env_var)

    if not api_key:
        raise ValueError(f"Missing '{env_var}' in environment variables.")
    
    return api_key