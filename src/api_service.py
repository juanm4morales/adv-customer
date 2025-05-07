import os
from dotenv import load_dotenv  # Importa la biblioteca dotenv
from flask import Flask, request, jsonify
from adv_customer.tools import fetch_bot_info, _generate_customer_attr_names

# Carga las variables de entorno desde el archivo .env
load_dotenv()

API_KEY = os.getenv("KLARI_API_KEY")

# Inicializar la aplicación Flask
app = Flask(__name__)

# Endpoint para obtener atributos del cliente
@app.route('/get-customer-attributes', methods=['POST'])
def get_customer_attributes():
    try:
        data = request.get_json()
        bot_id = data.get('bot_id')
        agent_id = data.get('agent_id')
        attributes = _generate_customer_attr_names(bot_id, agent_id)
        return jsonify(attributes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para generar una conversación
@app.route('/generate-conversation', methods=['POST'])
def generate_conversation():
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        bot_id = data.get('bot_id')
        agent_id = data.get('agent_id')
        customer_info = data.get('customer_info')
        # Simulación de generación de conversación
        conversation = {
            "conversation": f"Simulación de conversación para el cliente con info: {customer_info}"
        }
        return jsonify([conversation])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)