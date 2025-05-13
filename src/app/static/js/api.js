export function fetchBots() {
    return fetch('/get-bots', {
        method: 'GET',
        headers: { 'accept': 'application/json' }
    }).then(res => res.json());
}

export function fetchAgents(botId) {
    return fetch(`/api/get-agents/${botId}`, {
        method: 'GET',
        headers: { 'accept': 'application/json' }
    }).then(res => res.json());
}

export function fetchAttributes(botId, agentId) {
    return fetch('/api/get-customer-attributes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bot_id: botId, agent_id: agentId })
    }).then(res => res.json());
}

export function generateConversation(payload) {
    return fetch('/api/generate-conversation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    }).then(res => res.json());
}
