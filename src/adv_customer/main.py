import argparse
from adv_customer.conversation_sim import ConversationSim
import adv_customer.utils.bot_utils as bot_utils

def customer_info_creation(customer_attributes):
        customer_info = {}
        print("\nPor favor, ingrese los valores para los siguientes atributos del cliente:")
        for attr_name in customer_attributes:
            value = input(f" - {attr_name}: ")
            customer_info[attr_name] = value
        return customer_info

def main():
    parser = argparse.ArgumentParser(description="Simulación de conversación con un chatbot.")
    parser.add_argument("bot_id", type=str, help="ID del bot para la simulación")
    parser.add_argument("agent_id", type=int, nargs="?", help="ID del agente (opcional)", default=None)
    args = parser.parse_args()
    
    bot_info = bot_utils.fetch_bot_info(args.bot_id)
    agent_info = next((info for info in bot_info if info.get('id') == args.agent_id), None)
    customer_attr = bot_utils.generate_customer_attr_names(agent_info["prompt_agent"]["prompt"])
    customer_info = customer_info_creation(customer_attr)
    customerSim = ConversationSim(
        customer_id="111111",
        customer_info=customer_info,
        agent_info=agent_info,
    )
    state = customerSim.simulate_conversation(verbose=True)
    customerSim.save_conversation()
    
if __name__ == "__main__":
    main()