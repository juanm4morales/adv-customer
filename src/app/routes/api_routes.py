from flask import Blueprint, request, jsonify, render_template
from app.controllers.api_controllers import get_customer_attributes_controller, generate_conversation_controller

bp = Blueprint('api', __name__)

@bp.route('/api/get-customer-attributes', methods=['POST'])
def get_customer_attributes():
    try:
        data = request.get_json()
        print("Datos recibidos en /api/get-customer-attributes:", data)  # Registro para depuración
        response = get_customer_attributes_controller(data)
        print("Respuesta del servicio get_customer_attributes_service:", response)  # Registro para depuración
        # Ajustar la respuesta para que sea compatible con el cliente
        return jsonify({"attributes": response})
    except Exception as e:
        print("Error en /api/get-customer-attributes:", str(e))  # Registro del error
        return jsonify({"error": str(e)}), 500

@bp.route('/api/generate-conversation', methods=['POST'])
def generate_conversation():
    try:
        data = request.get_json()
        user_id = request.remote_addr  # Identificar al usuario por su IP
        response = generate_conversation_controller(data, user_id)
        return jsonify({"messages": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')