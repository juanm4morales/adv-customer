import random
from adv_customer.prompts import customer_attributes

def filter_prompt_variables(prompt_template, variables: dict):
    """ 
    Filter the variables to only include those that are expected by the prompt template.
    Args:
        prompt_template (object): The prompt template object.
        variables (dict): A dictionary of variables to filter.
    Returns:
        dict: A dictionary containing only the variables that are expected by the prompt template.
    """
    expected_vars = set(prompt_template.input_variables)
    return {k: v for k, v in variables.items() if k in expected_vars}

def generate_random_customer_profile(seed: int = None):
    """
    Generate a random customer profile based on predefined attributes.
    Args:
        seed (int, optional): Seed for random number generator. Defaults to None.
    Returns:
        str: Randomly generated customer profile.
    """
    if seed is not None:
        random.seed(seed)
    profile = ""
    for key, values in customer_attributes.items():
        attribute = random.choice(values)
        profile += f"{key}: {attribute}\n"
    return profile