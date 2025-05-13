import { createMessageElement } from './dom-utils.js';

export function initChat() {
    const chatMessages = document.getElementById('chat-messages');
    const backToHomeButton = document.getElementById('back-to-home');
    const backToFormButton = document.getElementById('back-to-form');
    const exportChatButton = document.getElementById('export-chat');

    if (chatMessages) {
        const messages = JSON.parse(sessionStorage.getItem('conversationMessages')) || [];
        messages.forEach(msg => {
            chatMessages.appendChild(createMessageElement(msg.message, msg.sender_type));
        });
    }

    backToHomeButton?.addEventListener('click', () => window.location.href = '/');
    backToFormButton?.addEventListener('click', () => window.history.back());

    exportChatButton?.addEventListener('click', () => {
        const messages = Array.from(chatMessages.children).map(el => el.textContent);
        const blob = new Blob([messages.join('\n\n')], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'conversacion.txt';
        link.click();
    });
}
