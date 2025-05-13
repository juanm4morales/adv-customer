export function toggleVisibility(element, show) {
    element.classList.toggle('hidden', !show);
}

export function createMessageElement(message, senderType) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', senderType === 'AIMessage' ? 'message-ai' : 'message-human');
    messageElement.textContent = senderType === 'AIMessage' 
        ? `Cliente: ${message}` 
        : `Asistente: ${message}`;
    return messageElement;
}
