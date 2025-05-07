# Adversarial Bot

This project simulates conversations between a customer and a chatbot to evaluate the chatbot's performance in various scenarios.

## Requirements

- Python 3.8 or higher
- Required dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd adversarial-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start a conversation simulation:

```bash
python src/adv_customer/main.py <bot_id>
```

Replace `<bot_id>` with the ID of the chatbot you want to simulate the conversation with.

## Project Structure

- `src/adv_customer/prompts.py`: Contains the prompt templates for customer simulation.
- `src/adv_customer/schemes.py`: Contains schemes for formatted outputs.
- `src/adv_customer/main.py`: Entry point for running the simulation. Requires as argument the {bot_id}
- `src/adv_customer/states.py`: Contains the state component of a graph (langgraph).
- `src/adv_customer/nodes.py`: Contains the nodes and conditional edges of a graph (langgraph).
- `src/adv_customer/customer_sim_agent.py`: Defines the `CustomerSim` class responsible for simulating customer behavior.
- `src/utils`: Contains reusable helper functions and modules for prompt construction, data persistence, and other general-purpose utilities that support the core logic of the project.
- `conversation/{customer_id}_{bot_id}_{agent_id}.txt`: File containing the conversation of the customer {customer_id} with the bot {bot_id} based on the agent {agent_id}.