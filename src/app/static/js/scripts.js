document.addEventListener('DOMContentLoaded', () => {
    const initialForm = document.getElementById('initial-form');
    const dynamicFormContainer = document.getElementById('dynamic-form-container');
    const resultContainer = document.getElementById('result-container');

    let botId = null;
    let agentId = null;

    // Manejar el envío del formulario inicial
    initialForm.addEventListener('submit', (event) => {
        event.preventDefault();

        botId = document.getElementById('bot-id').value;
        agentId = document.getElementById('agent-id').value;

        const initialSubmitButton = initialForm.querySelector('button[type="submit"]');
        initialSubmitButton.disabled = true; // Deshabilitar el botón

        fetch('/api/get-customer-attributes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ bot_id: botId, agent_id: agentId })
        })
        .then(response => response.json())
        .then(data => {
            initialSubmitButton.disabled = false; // Habilitar el botón nuevamente

            if (!data || !Array.isArray(data.attributes)) {
                throw new Error('La respuesta de la API no contiene atributos válidos.');
            }

            // Ocultar el formulario inicial
            initialForm.style.display = 'none';

            // Generar el formulario dinámico
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
            dynamicFormContainer.style.display = 'block';

            // Manejar el envío del formulario dinámico
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
                    chat_id: Date.now().toString(), // Generar un chat_id único
                    customer_info: customerInfo
                };

                dynamicSubmitButton.disabled = true; // Deshabilitar el botón

                fetch('/api/generate-conversation', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                })
                .then(response => response.json())
                .then(result => {
                    dynamicSubmitButton.disabled = false; // Habilitar el botón nuevamente

                    // Mostrar el contenedor del chat
                    const chatContainer = document.getElementById('chat-container');
                    const chatMessages = document.getElementById('chat-messages');
                    chatContainer.style.display = 'block';

                    // Limpiar mensajes previos
                    chatMessages.innerHTML = '';

                    // Renderizar los mensajes del chat
                    result.messages.forEach(message => {
                        const messageElement = document.createElement('div');
                        messageElement.style.marginBottom = '10px';
                        messageElement.style.padding = '10px';
                        messageElement.style.borderRadius = '5px';
                        messageElement.style.maxWidth = '80%';

                        if (message.sender_type === 'AIMessage') {
                            messageElement.style.backgroundColor = '#e0f7fa';
                            messageElement.style.alignSelf = 'flex-start';
                            messageElement.textContent = `Cliente: ${message.message}`;
                        } else if (message.sender_type === 'HumanMessage') {
                            messageElement.style.backgroundColor = '#f1f8e9';
                            messageElement.style.alignSelf = 'flex-end';
                            messageElement.textContent = `Asistente: ${message.message}`;
                        }

                        chatMessages.appendChild(messageElement);
                    });
                })
                .catch(error => {
                    dynamicSubmitButton.disabled = false; // Habilitar el botón nuevamente
                    console.error('Error:', error);
                    resultContainer.textContent = 'Ocurrió un error al generar la conversación.';
                });
            });
        })
        .catch(error => {
            initialSubmitButton.disabled = false; // Habilitar el botón nuevamente
            console.error('Error:', error);
            resultContainer.textContent = 'Ocurrió un error al obtener los atributos.';
        });
    });
});