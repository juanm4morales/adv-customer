document.addEventListener('DOMContentLoaded', () => {
    const initialForm = document.getElementById('initial-form');
    const dynamicFormContainer = document.getElementById('dynamic-form-container');
    const resultContainer = document.getElementById('result-container');
    const chatContainer = document.getElementById('chat-container');
    const chatMessages = document.getElementById('chat-messages');
    const botSelect = document.getElementById('bot-id');
    const agentSelect = document.getElementById('agent-id');

    let botId = null;
    let agentId = null;

    const toggleVisibility = (element, show) => {
        element.classList.toggle('hidden', !show);
    };

    // Asegurar que createMessageElement esté disponible globalmente
    window.createMessageElement = (message, senderType) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(senderType === 'AIMessage' ? 'message-ai' : 'message-human');
        messageElement.textContent = senderType === 'AIMessage' 
            ? `Cliente: ${message}` 
            : `Asistente: ${message}`;
        return messageElement;
    };

    // Redirigir a la página de conversación generada
    const redirectToConversationPage = (messages) => {
        const conversationPageUrl = '/conversation';
        sessionStorage.setItem('conversationMessages', JSON.stringify(messages));
        window.location.href = conversationPageUrl;
    };

    // Verificar si ya se cargaron los bots en el almacenamiento local
    const cachedBots = localStorage.getItem('bots');
    if (cachedBots) {
        JSON.parse(cachedBots).forEach(bot => {
            const option = document.createElement('option');
            option.value = bot.id;
            option.textContent = bot.name;
            botSelect.appendChild(option);
        });
    } else {
        // Obtener la lista de bots desde el backend
        fetch('/get-bots', {
            method: 'GET',
            headers: {
                'accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(bots => {
            localStorage.setItem('bots', JSON.stringify(bots));
            bots.forEach(bot => {
                const option = document.createElement('option');
                option.value = bot.id;
                option.textContent = bot.name;
                botSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error al obtener la lista de bots:', error);
        });
    }

    // Reemplazar el evento 'change' nativo con el evento de Select2
    $('#bot-id').on('select2:select', (event) => {
        const botId = event.params.data.id;

        // Limpiar el select de agentes
        agentSelect.innerHTML = '<option value="" disabled selected>Selecciona un agente</option>';

        // Obtener la lista de agentes para el bot seleccionado
        fetch(`/api/get-agents/${botId}`, {
            method: 'GET',
            headers: {
                'accept': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la respuesta del servidor: ${response.status}`);
            }
            return response.json();
        })
        .then(agents => {
            if (!Array.isArray(agents)) {
                throw new Error('La respuesta del servidor no contiene una lista de agentes válida.');
            }

            agents.forEach(agent => {
                const option = document.createElement('option');
                option.value = agent.id;
                option.textContent = agent.name;
                agentSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error al obtener la lista de agentes:', error);
        });
    });

    // Manejar el envío del formulario inicial
    initialForm.addEventListener('submit', (event) => {
        event.preventDefault();

        botId = botSelect.value;
        agentId = document.getElementById('agent-id').value;

        const initialSubmitButton = initialForm.querySelector('button[type="submit"]');
        initialSubmitButton.disabled = true;

        fetch('/api/get-customer-attributes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bot_id: botId, agent_id: agentId })
        })
        .then(response => response.json())
        .then(data => {
            initialSubmitButton.disabled = false;

            if (!data || !Array.isArray(data.attributes)) {
                throw new Error('La respuesta de la API no contiene atributos válidos.');
            }

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

                dynamicForm.appendChild(label);
                dynamicForm.appendChild(input);
                dynamicForm.appendChild(document.createElement('br'));
            });

            const dynamicSubmitButton = document.createElement('button');
            dynamicSubmitButton.type = 'submit';
            dynamicSubmitButton.textContent = 'Enviar';
            dynamicForm.appendChild(dynamicSubmitButton);

            dynamicFormContainer.appendChild(dynamicForm);
            toggleVisibility(dynamicFormContainer, true);

            dynamicForm.addEventListener('submit', (event) => {
                event.preventDefault();

                const formData = new FormData(dynamicForm);
                const customerInfo = {};
                formData.forEach((value, key) => {
                    customerInfo[key] = value;
                });

                const payload = {
                    bot_id: botId,
                    agent_id: agentId,
                    chat_id: Date.now().toString(),
                    customer_info: customerInfo
                };

                dynamicSubmitButton.disabled = true;

                fetch('/api/generate-conversation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                })
                .then(response => response.json())
                .then(result => {
                    dynamicSubmitButton.disabled = false;
                    redirectToConversationPage(result.messages);
                })
                .catch(error => {
                    dynamicSubmitButton.disabled = false;
                    console.error('Error:', error);
                    resultContainer.textContent = 'Ocurrió un error al generar la conversación.';
                });
            });
        })
        .catch(error => {
            initialSubmitButton.disabled = false;
            console.error('Error:', error);
            resultContainer.textContent = 'Ocurrió un error al obtener los atributos.';
        });
    });
});

// Manejar la navegación en la página de conversación
document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const backToHomeButton = document.getElementById('back-to-home');
    const backToFormButton = document.getElementById('back-to-form');
    const exportChatButton = document.getElementById('export-chat');
    const chatMessagesContainer = document.getElementById('chat-messages');

    if (chatMessages) {
        const messages = JSON.parse(sessionStorage.getItem('conversationMessages')) || [];
        messages.forEach(message => {
            const messageElement = window.createMessageElement(message.message, message.sender_type);
            chatMessages.appendChild(messageElement);
        });
    }

    if (backToHomeButton) {
        backToHomeButton.addEventListener('click', () => {
            window.location.href = '/';
        });
    }

    if (backToFormButton) {
        backToFormButton.addEventListener('click', () => {
            window.history.back();
        });
    }

    if (exportChatButton) {
        exportChatButton.addEventListener('click', () => {
            const messages = Array.from(chatMessagesContainer.children).map(messageElement => messageElement.textContent);
            const chatContent = messages.join('\n\n');

            const blob = new Blob([chatContent], { type: 'text/plain' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'conversacion.txt';
            link.click();
        });
    }
});