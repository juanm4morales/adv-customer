import { fetchBots, fetchAgents, fetchAttributes, generateConversation } from './api.js';
import { toggleVisibility } from './dom-utils.js';

export function initForm() {
    const initialForm = document.getElementById('initial-form');
    const dynamicFormContainer = document.getElementById('dynamic-form-container');
    const resultContainer = document.getElementById('result-container');
    const botSelect = document.getElementById('bot-id');
    const agentSelect = document.getElementById('agent-id');

    let botId = null;
    let agentId = null;

    const cachedBots = localStorage.getItem('bots');
    if (cachedBots) {
        JSON.parse(cachedBots).forEach(bot => {
            const option = new Option(bot.name, bot.id);
            botSelect.appendChild(option);
        });
    } else {
        fetchBots()
            .then(bots => {
                localStorage.setItem('bots', JSON.stringify(bots));
                bots.forEach(bot => {
                    const option = new Option(bot.name, bot.id);
                    botSelect.appendChild(option);
                });
            })
            .catch(err => console.error('Error al obtener bots:', err));
    }

    $('#bot-id').on('select2:select', (event) => {
        const selectedBotId = event.params.data.id;
        agentSelect.innerHTML = '<option value="" disabled selected>Selecciona un agente</option>';

        fetchAgents(selectedBotId)
            .then(agents => {
                agents.forEach(agent => {
                    const option = new Option(agent.name, agent.id);
                    agentSelect.appendChild(option);
                });
            })
            .catch(err => console.error('Error al obtener agentes:', err));
    });

    initialForm.addEventListener('submit', (event) => {
        event.preventDefault();
        botId = botSelect.value;
        agentId = agentSelect.value;

        const initialSubmitButton = initialForm.querySelector('button[type="submit"]');
        initialSubmitButton.disabled = true;

        fetchAttributes(botId, agentId)
            .then(data => {
                initialSubmitButton.disabled = false;
                if (!data || !Array.isArray(data.attributes)) throw new Error('Atributos inválidos');

                toggleVisibility(initialForm, false);

                const dynamicForm = document.createElement('form');
                dynamicForm.id = 'dynamic-form';

                data.attributes.forEach(attribute => {
                    const label = document.createElement('label');
                    label.textContent = attribute;
                    label.htmlFor = attribute;

                    const input = document.createElement('input');
                    input.type = 'text';
                    input.name = attribute;
                    input.id = attribute;

                    dynamicForm.append(label, input, document.createElement('br'));
                });

                const submitBtn = document.createElement('button');
                submitBtn.type = 'submit';
                submitBtn.textContent = 'Enviar';
                dynamicForm.appendChild(submitBtn);

                dynamicFormContainer.appendChild(dynamicForm);
                toggleVisibility(dynamicFormContainer, true);

                dynamicForm.addEventListener('submit', (event) => {
                    event.preventDefault();
                    const formData = new FormData(dynamicForm);
                    const customerInfo = {};
                    formData.forEach((value, key) => customerInfo[key] = value);

                    const payload = {
                        bot_id: botId,
                        agent_id: agentId,
                        chat_id: Date.now().toString(),
                        customer_info: customerInfo
                    };

                    submitBtn.disabled = true;
                    generateConversation(payload)
                        .then(result => {
                            submitBtn.disabled = false;
                            sessionStorage.setItem('conversationMessages', JSON.stringify(result.messages));
                            window.location.href = '/conversation';
                        })
                        .catch(error => {
                            submitBtn.disabled = false;
                            console.error('Error:', error);
                            resultContainer.textContent = 'Ocurrió un error al generar la conversación.';
                        });
                });
            })
            .catch(error => {
                initialSubmitButton.disabled = false;
                console.error('Error:', error);
                resultContainer.textContent = 'Error al obtener atributos.';
            });
    });
}
