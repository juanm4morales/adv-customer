// storage.js - Módulo para manejar el almacenamiento local
export const Storage = {
    // LocalStorage
    local: {
        getBots: () => {
            const cachedBots = localStorage.getItem('bots');
            return cachedBots ? JSON.parse(cachedBots) : null;
        },
        
        setBots: (bots) => {
            localStorage.setItem('bots', JSON.stringify(bots));
        }
    },
    
    // SessionStorage
    session: {
        getConversationMessages: () => {
            const messages = sessionStorage.getItem('conversationMessages');
            return messages ? JSON.parse(messages) : [];
        },
        
        setConversationMessages: (messages) => {
            sessionStorage.setItem('conversationMessages', JSON.stringify(messages));
        },
        
        getCustomerProfile: () => {
            const profile = sessionStorage.getItem('customerProfile');
            return profile ? JSON.parse(profile) : null;
        },
        
        setCustomerProfile: (profile) => {
            sessionStorage.setItem('customerProfile', JSON.stringify(profile));
        },
        
        getCustomerAttributes: () => {
            const attributes = sessionStorage.getItem('customerAttributes');
            return attributes ? JSON.parse(attributes) : null;
        },
        
        setCustomerAttributes: (attributes) => {
            sessionStorage.setItem('customerAttributes', JSON.stringify(attributes));
        }
    }
};

// Navegación
export const Navigation = {
    redirectToConversationPage: (messages, customerProfile) => {
        Storage.session.setConversationMessages(messages);
        Storage.session.setCustomerProfile(customerProfile);
        window.location.href = '/conversation';
    },
    
    goHome: () => {
        window.location.href = '/';
    },
    
    goBack: () => {
        window.history.back();
    }
};