// form-handler.js - Módulo para manejar formularios
import { ApiClient } from './api.js';
import { UIComponents, toggleVisibility } from './ui-components.js';
import { Storage, Navigation } from './storage.js';

export const FormHandler = {
    init: () => {
        const initialForm = document.getElementById('initial-form');
        const botSelect = document.getElementById('bot-id');
        const agentSelect = document.getElementById('agent-id');

        // Inicializar dropdowns de bots
        FormHandler.initializeBots(botSelect);

        // Configurar evento de selección de bot
        $('#bot-id').on('select2:select', (event) => {
            const botId = event.params.data.id;
            FormHandler.handleBotSelection(botId, agentSelect);
        });

        // Configurar envío del formulario inicial
        if (initialForm) {
            initialForm.addEventListener('submit', (event) => {
                event.preventDefault();
                FormHandler.handleInitialFormSubmit(event);
            });
        }
    },

    initializeBots: async (botSelect) => {
        // Verificar si ya se cargaron los bots en el almacenamiento local
        const cachedBots = Storage.local.getBots();
        
        if (cachedBots) {
            UIComponents.populateBots(botSelect, cachedBots);
        } else {
            try {
                const bots = await ApiClient.getBots();
                Storage.local.setBots(bots);
                UIComponents.populateBots(botSelect, bots);
            } catch (error) {
                console.error('Error al obtener la lista de bots:', error);
            }
        }
    },

    handleBotSelection: async (botId, agentSelect) => {
        try {
            const agents = await ApiClient.getAgents(botId);
            
            if (!Array.isArray(agents)) {
                throw new Error('La respuesta del servidor no contiene una lista de agentes válida.');
            }
            
            UIComponents.populateAgents(agentSelect, agents);
        } catch (error) {
            console.error('Error al obtener la lista de agentes:', error);
        }
    },

    handleInitialFormSubmit: async (event) => {
        const initialForm = event.target;
        const botSelect = document.getElementById('bot-id');
        const agentSelect = document.getElementById('agent-id');
        const botId = botSelect.value;
        const agentId = agentSelect.value;
        
        // Guardar botId y agentId en sessionStorage para restaurar el formulario dinámico si es necesario
        sessionStorage.setItem('botId', botId);
        sessionStorage.setItem('agentId', agentId);
        
        const initialSubmitButton = initialForm.querySelector('button[type="submit"]');
        initialSubmitButton.disabled = true;

        // Mostrar animación de carga
        const loadingContainer = UIComponents.createLoadingContainer('Obteniendo atributos');
        initialForm.parentElement.appendChild(loadingContainer);

        try {
            const data = await ApiClient.getCustomerAttributes(botId, agentId);
            
            initialSubmitButton.disabled = false;
            loadingContainer.remove();

            toggleVisibility(initialForm, false);
            
            // Crear y mostrar formulario dinámico
            const dynamicFormContainer = document.getElementById('dynamic-form-container');
            const dynamicForm = UIComponents.createDynamicForm(data.attributes);
            
            dynamicFormContainer.appendChild(dynamicForm);
            toggleVisibility(dynamicFormContainer, true);

            // Configurar envío del formulario dinámico
            dynamicForm.addEventListener('submit', (event) => {
                event.preventDefault();
                FormHandler.handleDynamicFormSubmit(event, botId, agentId);
            });
            
        } catch (error) {
            initialSubmitButton.disabled = false;
            loadingContainer.remove();
            console.error('Error:', error);
            
            const resultContainer = document.getElementById('result-container');
            const errorMessage = UIComponents.createErrorMessage('Ocurrió un error al obtener los atributos. Por favor intenta nuevamente.');
            resultContainer.appendChild(errorMessage);
            toggleVisibility(resultContainer, true);
        }
    },

    handleDynamicFormSubmit: async (event, botId, agentId) => {
        const dynamicForm = event.target;
        const formData = new FormData(dynamicForm);
        const customerInfo = {};
        
        formData.forEach((value, key) => {
            customerInfo[key] = value;
        });

        // Guardar los atributos y valores elegidos en sessionStorage
        Storage.session.setCustomerAttributes(customerInfo);

        const dynamicSubmitButton = dynamicForm.querySelector('button[type="submit"]');
        dynamicSubmitButton.disabled = true;

        // Crear y mostrar el contenedor de carga
        const loadingContainer = UIComponents.createLoadingContainer(
            'Generando conversación',
            'Por favor espera un momento'
        );

        const dynamicFormContainer = document.getElementById('dynamic-form-container');
        const resultContainer = document.getElementById('result-container');
        
        dynamicFormContainer.style.display = 'none';
        resultContainer.appendChild(loadingContainer);
        toggleVisibility(resultContainer, true);

        try {
            const result = await ApiClient.generateConversation(
                botId,
                agentId,
                Date.now().toString(),
                customerInfo
            );
            
            dynamicSubmitButton.disabled = false;
            loadingContainer.remove();
            Navigation.redirectToConversationPage(result.messages, result.customer_profile);
            
        } catch (error) {
            dynamicSubmitButton.disabled = false;
            loadingContainer.remove();
            dynamicFormContainer.style.display = 'block';
            
            console.error('Error:', error);
            const errorMessage = UIComponents.createErrorMessage('Ocurrió un error al generar la conversación. Por favor intenta nuevamente.');
            resultContainer.innerHTML = '';
            resultContainer.appendChild(errorMessage);
        }
    }
};