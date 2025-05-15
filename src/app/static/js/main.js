// main.js - Punto de entrada principal
import { FormHandler } from './form-handler.js';
import { ConversationPage } from './conversation-page.js';
import { UIComponents } from './ui-components.js';

// Inicializar Select2
function initializeSelect2() {
    if (typeof $ !== 'undefined' && $.fn.select2) {
        $('#bot-id, #agent-id').select2({
            placeholder: function() {
                return $(this).data('placeholder');
            },
            allowClear: true
        });
    }
}

// Hacer accesible createMessageElement globalmente para compatibilidad
window.createMessageElement = UIComponents.createMessageElement;

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    // Determinar qué página estamos cargando
    const path = window.location.pathname;
    
    if (path === '/' || path === '/index.html') {
        // Página principal
        FormHandler.init();
        initializeSelect2();

        // Solo reanudar el formulario dinámico si el flag viene de "volver al formulario"
        if (sessionStorage.getItem('resumeDynamicForm') === 'true') {
            sessionStorage.removeItem('resumeDynamicForm');
            const botId = sessionStorage.getItem('botId');
            const agentId = sessionStorage.getItem('agentId');
            const customerAttributes = sessionStorage.getItem('customerAttributes');
            if (botId && agentId && customerAttributes) {
                // Ocultar formulario inicial
                const initialFormContainer = document.getElementById('initial-form-container');
                if (initialFormContainer) initialFormContainer.classList.add('hidden');
                // Mostrar formulario dinámico con los atributos previos
                const dynamicFormContainer = document.getElementById('dynamic-form-container');
                const attributes = Object.keys(JSON.parse(customerAttributes));
                const dynamicForm = UIComponents.createDynamicForm(attributes);
                // Rellenar los valores previos
                const values = JSON.parse(customerAttributes);
                setTimeout(() => {
                    attributes.forEach(attr => {
                        const input = dynamicForm.querySelector(`[name="${attr}"]`);
                        if (input) input.value = values[attr];
                    });
                }, 0);
                dynamicFormContainer.appendChild(dynamicForm);
                dynamicFormContainer.classList.remove('hidden');
                // Configurar envío del formulario dinámico
                dynamicForm.addEventListener('submit', (event) => {
                    event.preventDefault();
                    FormHandler.handleDynamicFormSubmit(event, botId, agentId);
                });
            }
        }
    } else if (path === '/conversation' || path === '/conversation.html') {
        // Página de conversación
        ConversationPage.init();
    }
});