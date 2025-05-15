import argparse
from adv_customer.conversation_sim import ConversationSim
import adv_customer.conversation_setup as conversation_setup

def customer_info_creation(customer_attributes):
        """Create customer information by prompting the user for input.
        Args:
            customer_attributes (list): List of customer attribute names.
        Returns:
            dict: A dictionary containing the customer information.
        """
        customer_info = {}
        print("\nPor favor, ingrese los valores para los siguientes atributos del cliente:")
        for attr_name in customer_attributes:
            value = input(f" - {attr_name}: ")
            customer_info[attr_name] = value
        return customer_info

def main():
    """Main function for simulating a conversation with a chatbot.
    """
    parser = argparse.ArgumentParser(description="Simulación de conversación con un chatbot.")
    parser.add_argument("bot_id", type=str, help="ID del bot para la simulación")
    parser.add_argument("agent_id", type=int, help="ID del agente")
    args = parser.parse_args()
    
    bot_info = conversation_setup.fetch_bot_info(args.bot_id)
    agent_info = next((info for info in bot_info if info.get('id') == args.agent_id), None)
    customer_attr = conversation_setup.generate_customer_attr_names(agent_info["prompt_agent"]["prompt"])
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