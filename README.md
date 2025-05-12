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

2. Install the package:
   ```bash
   pip install .
   ```

3. Create a `.env` file in the root directory and add the required environment variables:
   ```
   KLARI_API_KEY, KLARI_BOT_API_KEY, OPENAI_API_KEY
   ```

## Usage

### Run the Web Application

To start the web application:

1. Run the Flask application:
   ```bash
   flask run
   ```

2. Open your browser and go to `http://127.0.0.1:5000` to access the web interface.

### Run the Simulation Script

Run the main script to start a conversation simulation:

```bash
simulate-conversation <bot_id> <agent_id>
```

Replace `<bot_id>` with the ID of the chatbot you want to simulate the conversation with.

## Project Structure

- `src/app`: Contains the web application code.
  - `templates/`: HTML templates for the web interface.
  - `static/`: Static files such as CSS and JavaScript.
  - `routes/`: API route definitions.
  - `controllers/`: Logic for handling API requests.
- `src/adv_customer`: Core logic for simulating conversations.
  - `prompts.py`: Contains the prompt templates for customer simulation.
  - `schemes.py`: Contains schemes for formatted outputs.
  - `main.py`: Entry point for running the simulation. Requires as argument the {bot_id}.
  - `states.py`: Contains the state component of a graph (langgraph).
  - `nodes.py`: Contains the nodes and conditional edges of a graph (langgraph).
  - `customer_sim_agent.py`: Defines the `CustomerSim` class responsible for simulating customer behavior.
- `conversation/{customer_id}_{bot_id}_{agent_id}.txt`: File containing the conversation of the customer {customer_id} with the bot {bot_id} based on the agent {agent_id}.