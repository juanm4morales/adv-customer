from flask import Blueprint, request, jsonify, render_template
import app.controllers.api_controllers as api_controllers
import os
import requests

bp = Blueprint('api', __name__)

@bp.route('/api/get-customer-attributes', methods=['POST'])
def get_customer_attributes():
    """Get customer attributes from the bot.
    
    Args:
        bot_id (str): The ID of the bot.
        agent_id (int): The ID of the agent.
        
    Returns:
        dict: A dictionary containing the customer attributes.
    """
    try:
        data = request.get_json()
        print("Datos recibidos en /api/get-customer-attributes:", data)  # Registro para depuración
        response = api_controllers.get_customer_attributes_controller(data)
        print("Respuesta del servicio get_customer_attributes_service:", response)  # Registro para depuración
        # Ajustar la respuesta para que sea compatible con el cliente
        return jsonify({"attributes": response})
    except Exception as e:
        print("Error en /api/get-customer-attributes:", str(e))  # Registro del error
        return jsonify({"error": str(e)}), 500

@bp.route('/api/generate-conversation', methods=['POST'])
def generate_conversation():
    """Generate a conversation simulation.
    
    Args:
        bot_id (str): The ID of the bot.
        agent_id (int): The ID of the agent.
        customer_info (dict): Information about the customer.

    Returns:
        dict: A dictionary containing the simulated conversation messages.
    """
    try:
        data = request.get_json()
        user_id = request.remote_addr  # Identificar al usuario por su IP
        response = api_controllers.generate_conversation_controller(data, user_id)
        return jsonify({"messages": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/', methods=['GET'])
def index():
    """Render the index page."""
    try:
        api_key = os.getenv('KLARI_API_KEY')
        if not api_key:
            raise ValueError("API key no configurada")

        url = 'https://api.klari.ai/api/v1/external/bots'
        headers = {
            'accept': 'application/json',
            'X-Api-Key': api_key
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        bots = response.json()
        bots_data = [{"id": bot["id"], "name": bot["name"]} for bot in bots]
    except Exception as e:
        print(f"Error al obtener la lista de bots: {e}")
        bots_data = []

    return render_template('index.html', bots=bots_data)

@bp.route('/conversation', methods=['GET'])
def conversation_page():
    """Render the conversation page."""
    return render_template('conversation.html')

@bp.route('/get-bots', methods=['GET'])
def get_bots():
    """Obtener la lista de bots desde el endpoint externo."""
    api_key = os.getenv('KLARI_API_KEY')
    if not api_key:
        return jsonify({"error": "API key no configurada"}), 500

    url = 'https://api.klari.ai/api/v1/external/bots'
    headers = {
        'accept': 'application/json',
        'X-Api-Key': api_key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        bots = response.json()
        return jsonify([{"id": bot["id"], "name": f"{bot['organization']['name']} ({bot['id']})"} for bot in bots])
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/get-agents/<int:bot_id>', methods=['GET'])
def get_agents(bot_id):
    """Obtener la lista de agentes específicos de un bot."""
    try:
        agents = api_controllers.get_agents_controller(bot_id)
        return jsonify(agents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500