import argparse
from customer_sim import CustomerSim

def main():
    parser = argparse.ArgumentParser(description="Simulación de conversación con un chatbot.")
    parser.add_argument("bot_id", type=str, help="ID del bot para la simulación")
    parser.add_argument("agent_id", type=int, nargs="?", help="ID del agente (opcional)", default=None)
    args = parser.parse_args()
    
    customerSim = CustomerSim(
        customer_id="111111",
        customer_name="Pablo",
        bot_id=args.bot_id,
        agent_id=args.agent_id
    )

    customerSim.simulate_conversation()
    customerSim.save_conversation()
    
if __name__ == "__main__":
    main()