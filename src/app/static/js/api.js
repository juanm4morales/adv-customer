// api.js - Módulo para manejar todas las llamadas a la API
export const ApiClient = {
    // Obtener lista de bots
    getBots: async () => {
        try {
            const response = await fetch('/get-bots', {
                method: 'GET',
                headers: {
                    'accept': 'application/json'
                }
            });
            if (!response.ok) {
                throw new Error(`Error en la respuesta del servidor: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error al obtener la lista de bots:', error);
            throw error;
        }
    },

    // Obtener agentes por bot
    getAgents: async (botId) => {
        try {
            const response = await fetch(`/api/get-agents/${botId}`, {
                method: 'GET',
                headers: {
                    'accept': 'application/json'
                }
            });
            if (!response.ok) {
                throw new Error(`Error en la respuesta del servidor: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error al obtener la lista de agentes:', error);
            throw error;
        }
    },

    // Obtener atributos del cliente
    getCustomerAttributes: async (botId, agentId) => {
        try {
            const response = await fetch('/api/get-customer-attributes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ bot_id: botId, agent_id: agentId })
            });
            const data = await response.json();
            
            if (!data || !Array.isArray(data.attributes)) {
                throw new Error('La respuesta de la API no contiene atributos válidos.');
            }
            
            return data;
        } catch (error) {
            console.error('Error al obtener atributos del cliente:', error);
            throw error;
        }
    },

    // Generar conversación
    generateConversation: async (botId, agentId, chatId, customerInfo) => {
        try {
            const payload = {
                bot_id: botId,
                agent_id: agentId,
                chat_id: chatId,
                customer_info: customerInfo
            };

            const response = await fetch('/api/generate-conversation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            return await response.json();
        } catch (error) {
            console.error('Error al generar conversación:', error);
            throw error;
        }
    }
};