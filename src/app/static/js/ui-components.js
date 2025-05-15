// ui-components.js - Módulo para crear componentes UI
export const UIComponents = {
    // Crear un elemento de mensaje
    createMessageElement: (message, senderType) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(senderType === 'AIMessage' ? 'message-ai' : 'message-human');
        
        // Crear el contenedor del emisor
        const senderElement = document.createElement('div');
        senderElement.classList.add('message-sender');
        senderElement.textContent = senderType === 'AIMessage' ? 'Cliente' : 'Asistente';
        
        // Crear el contenido del mensaje
        const contentElement = document.createElement('div');
        contentElement.textContent = message;
        
        messageElement.appendChild(senderElement);
        messageElement.appendChild(contentElement);
        return messageElement;
    },

    // Crear contenedor de carga
    createLoadingContainer: (text, subtext = null) => {
        const loadingContainer = document.createElement('div');
        loadingContainer.classList.add('loading-container');
        
        let html = `
            <div class="loading-spinner"></div>
            <div class="loading-text">
                ${text}<span class="loading-dots"></span>
            </div>
        `;
        
        if (subtext) {
            html += `
                <div style="color: var(--text-color); opacity: 0.7; font-size: 0.9rem;">
                    ${subtext}
                </div>
            `;
        }
        
        loadingContainer.innerHTML = html;
        return loadingContainer;
    },

    // Crear mensaje de error
    createErrorMessage: (message) => {
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = 'color: var(--accent-color); text-align: center; font-weight: 500;';
        errorDiv.textContent = message;
        return errorDiv;
    },

    // Crear formulario dinámico
    createDynamicForm: (attributes) => {
        const dynamicForm = document.createElement('form');
        dynamicForm.id = 'dynamic-form';

        // Encabezado descriptivo
        const header = document.createElement('div');
        header.className = 'dynamic-form-header';
        header.innerHTML = `<h2>Información del Cliente</h2><p>Por favor, ingresa los valores para los atributos del cliente.</p>`;
        dynamicForm.appendChild(header);

        attributes.forEach(attribute => {
            const label = document.createElement('label');
            label.textContent = attribute;
            label.htmlFor = attribute;

            const input = document.createElement('input');
            input.type = 'text';
            input.name = attribute;
            input.id = attribute;
            // Permitir que el valor sea seteado desde fuera (para reanudar)

            dynamicForm.appendChild(label);
            dynamicForm.appendChild(input);
        });

        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.textContent = 'Enviar';
        dynamicForm.appendChild(submitButton);

        return dynamicForm;
    },

    // Poblar dropdown de bots
    populateBots: (selectElement, bots) => {
        bots.forEach(bot => {
            const option = document.createElement('option');
            option.value = bot.id;
            option.textContent = bot.name;
            selectElement.appendChild(option);
        });
    },

    // Poblar dropdown de agentes
    populateAgents: (selectElement, agents) => {
        // Limpiar opciones existentes excepto el placeholder
        selectElement.innerHTML = '<option value="" disabled selected>Selecciona un agente</option>';
        
        agents.forEach(agent => {
            const option = document.createElement('option');
            option.value = agent.id;
            option.textContent = agent.name;
            selectElement.appendChild(option);
        });
    }
};

// Función de utilidad para alternar visibilidad
export const toggleVisibility = (element, show) => {
    element.classList.toggle('hidden', !show);
};