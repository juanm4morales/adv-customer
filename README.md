# Adversarial Bot

This project simulates conversations between a customer and a chatbot to evaluate the chatbot's performance in various scenarios.

## Requirements

- Python 3.8 or higher
- Required dependencies listed in `requirements.txt`
- Docker and Docker Compose (optional but recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd adversarial-bot
   ```

2. Create a `.env` file in the root directory and add the required environment variables:
   ```
   KLARI_API_KEY, KLARI_BOT_API_KEY, OPENAI_API_KEY
   ```

3. Install the package (only required for local execution without Docker):
   ```bash
   pip install -e .
   ```

## Usage

### Run with Docker Compose (Recommended)

The easiest way to run the application is using Docker Compose:

1. Make sure you have Docker and Docker Compose installed on your system.

2. Build and start the container:
   ```bash
   docker-compose up --build
   ```

3. The application will be available at `http://localhost:5000`.

4. To stop the application:
   ```bash
   docker-compose down
   ```

### Run with Docker

You can also run the application using Docker directly:

1. Build the Docker image:
   ```bash
   docker build -t adversarial-bot .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 --env-file .env adversarial-bot
   ```

3. The application will be available at `http://localhost:5000`.

### Run the Web Application Locally

To start the web application without Docker:

1. Set the Flask application entry point. If your application is located in the src directory, create a .flaskenv file at the root of your project with the following content:

   ```
   FLASK_APP=src/app
   ```

2. Run the Flask application:

   ```bash
   flask run
   ```

3. Open your browser and go to `http://127.0.0.1:5000` to access the web interface.

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
  - `routes/`: API + web app route definitions.
  - `controllers/`: Logic for handling API requests.
- `src/adv_customer`: Core logic for simulating conversations.
  - `prompts.py`: Contains the prompt templates for customer simulation.
  - `schemes.py`: Contains schemes for formatted outputs.
  - `main.py`: Entry point for running the simulation in terminal.
  - `states.py`: Contains the state component of a graph (langgraph).
  - `nodes.py`: Contains the nodes and conditional edges of a graph (langgraph).
  - `conversation_sim.py`: Defines the `ConversationSim` class responsible for simulating customer behavior.
  - `conversation_setup.py`: Contains what is necessary to prepare (setup) a conversation simulation. Used in app module.
  - `utils/`: Contains utilities for prompt creation, serialization and api key retrieval.
- `conversation/{customer_id}_{bot_id}_{agent_id}.txt`: File containing the conversation of the customer {customer_id} with the bot {bot_id} based on the agent {agent_id}.