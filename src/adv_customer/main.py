import argparse
from customer_sim import CustomerSim
import utils.bot_utils as bot_utils

def main():
    parser = argparse.ArgumentParser(description="Simulación de conversación con un chatbot.")
    parser.add_argument("bot_id", type=str, help="ID del bot para la simulación")
    parser.add_argument("agent_id", type=int, nargs="?", help="ID del agente (opcional)", default=None)
    args = parser.parse_args()
    bot_info = bot_utils.fetch_bot_info(args.bot_id)
    agent_info = next((info for info in bot_info if info.get('id') == args.agent_id), None)
    print(agent_info)
    customer_info = bot_utils.generate_customer_attr_names(agent_info["prompt_agent"]["prompt"])
    print(customer_info)
    
    customerSim = CustomerSim(
        customer_id="111111",
        customer_info=customer_info,
        agent_info=agent_info,
    )

    #customerSim.simulate_conversation()
    #customerSim.save_conversation()
    
if __name__ == "__main__":
    main()