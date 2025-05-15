// conversation-page.js - Módulo para manejar la página de conversación
import { UIComponents } from './ui-components.js';
import { Storage, Navigation } from './storage.js';

export const ConversationPage = {
    init: () => {
        const chatMessages = document.getElementById('chat-messages');
        const backToHomeButton = document.getElementById('back-to-home');
        const backToFormButton = document.getElementById('back-to-form');
        const exportChatButton = document.getElementById('export-chat');

        if (chatMessages) {
            ConversationPage.renderMessages(chatMessages);
            ConversationPage.renderCustomerProfile();
        }

        // Configurar botones de navegación
        if (backToHomeButton) {
            backToHomeButton.addEventListener('click', Navigation.goHome);
        }

        if (backToFormButton) {
            backToFormButton.addEventListener('click', () => {
                // Marcar que se debe reanudar el formulario dinámico
                sessionStorage.setItem('resumeDynamicForm', 'true');
                window.location.href = '/';
            });
        }

        if (exportChatButton) {
            exportChatButton.addEventListener('click', ConversationPage.exportChat);
        }
    },

    renderMessages: (chatMessages) => {
        const messages = Storage.session.getConversationMessages();
        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            messageElement.classList.add(message.sender_type === 'AIMessage' ? 'message-ai' : 'message-human');
            
            // Crear el contenedor del emisor
            const senderElement = document.createElement('div');
            senderElement.classList.add('message-sender');
            senderElement.textContent = message.sender_type === 'AIMessage' ? 'Cliente' : 'Asistente';
            
            // Crear el contenido del mensaje
            const contentElement = document.createElement('div');
            contentElement.textContent = message.message;
            
            messageElement.appendChild(senderElement);
            messageElement.appendChild(contentElement);
            chatMessages.appendChild(messageElement);
        });
    },

    renderCustomerProfile: () => {
        const customerProfile = Storage.session.getCustomerProfile();
        const customerAttributes = Storage.session.getCustomerAttributes();
        
        if (customerProfile || customerAttributes) {
            const profileContainer = document.getElementById('customer-profile');
            if (profileContainer) {
                profileContainer.innerHTML = '<h2>Perfil del Cliente</h2>';
                
                const profileContent = document.createElement('div');
                profileContent.classList.add('profile-content');
                
                // Mostrar atributos elegidos y valores
                if (customerAttributes && typeof customerAttributes === 'object' && Object.keys(customerAttributes).length > 0) {
                    ConversationPage.renderAttributes(profileContent, customerAttributes);
                }
                
                // Mostrar el perfil generado
                if (customerProfile) {
                    ConversationPage.renderGeneratedProfile(profileContent, customerProfile);
                }
                
                profileContainer.appendChild(profileContent);
            }
        }
    },

    renderAttributes: (container, attributes) => {
        const attributesSection = document.createElement('div');
        attributesSection.classList.add('profile-section', 'attributes-section');
        
        const attrTitle = document.createElement('div');
        attrTitle.classList.add('profile-section-title');
        attrTitle.innerHTML = '📋 Atributos del Cliente';
        attributesSection.appendChild(attrTitle);
        
        const dlAttrs = document.createElement('dl');
        Object.entries(attributes).forEach(([key, value]) => {
            if (value) {
                const dt = document.createElement('dt');
                dt.textContent = key;
                const dd = document.createElement('dd');
                dd.textContent = value;
                dlAttrs.appendChild(dt);
                dlAttrs.appendChild(dd);
            }
        });
        
        attributesSection.appendChild(dlAttrs);
        container.appendChild(attributesSection);
    },

    renderGeneratedProfile: (container, profile) => {
        const generatedSection = document.createElement('div');
        generatedSection.classList.add('profile-section', 'generated-profile-section');
        
        const genTitle = document.createElement('div');
        genTitle.classList.add('profile-section-title');
        genTitle.innerHTML = '✨ Perfil Generado';
        generatedSection.appendChild(genTitle);
        
        if (typeof profile === 'string') {
            const textContainer = document.createElement('div');
            profile.split(/\r?\n/).forEach(line => {
                if (line.trim()) {
                    const p = document.createElement('p');
                    p.textContent = line;
                    textContainer.appendChild(p);
                }
            });
            generatedSection.appendChild(textContainer);
        } else if (typeof profile === 'object') {
            const dl = document.createElement('dl');
            Object.entries(profile).forEach(([key, value]) => {
                if (value) {
                    const dt = document.createElement('dt');
                    dt.textContent = key;
                    const dd = document.createElement('dd');
                    if (typeof value === 'string' && value.includes('\n')) {
                        value.split(/\r?\n/).forEach(line => {
                            if (line.trim()) {
                                const p = document.createElement('p');
                                p.textContent = line;
                                dd.appendChild(p);
                            }
                        });
                    } else {
                        dd.textContent = value;
                    }
                    dl.appendChild(dt);
                    dl.appendChild(dd);
                }
            });
            generatedSection.appendChild(dl);
        }
        
        container.appendChild(generatedSection);
    },

    exportChat: () => {
        const date = new Date();
        const formattedDate = date.toLocaleDateString('es-ES');
        const profile = Storage.session.getCustomerProfile() || {};
        const attributes = Storage.session.getCustomerAttributes() || {};
        
        // Preparar contenido
        let content = `FECHA: ${formattedDate}\n\n`;
        
        // Info del cliente
        content += "INFO CLIENTE:\n";
        Object.entries(attributes).forEach(([k, v]) => v && (content += `${k}: ${v}\n`));
        
        // Perfil
        content += "\nPERFIL:\n";
        if (typeof profile === 'string') {
            content += profile + "\n";
        } else if (typeof profile === 'object') {
            Object.entries(profile).forEach(([k, v]) => v && (content += `${k}: ${v}\n`));
        }
        
        // Conversación
        content += "\nCONVERSACIÓN:\n";
        Storage.session.getConversationMessages().forEach(msg => {
            const sender = msg.sender_type === 'AIMessage' ? "Cliente" : "Asistente";
            content += `${sender}: ${msg.message}\n\n`;
        });
        
        // Descargar
        const blob = new Blob([content], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `conversacion_${formattedDate.replace(/\//g, '-')}.txt`;
        link.click();
    }
};