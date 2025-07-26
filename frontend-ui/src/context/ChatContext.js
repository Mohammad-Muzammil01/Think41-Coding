// src/context/ChatContext.js
import React, { createContext, useContext, useState } from 'react';

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [conversations, setConversations] = useState({
    session1: [{ sender: 'user', text: 'Hello!' }, { sender: 'bot', text: 'Hi!' }],
    session2: [{ sender: 'user', text: 'How are you?' }, { sender: 'bot', text: 'Doing great!' }],
  });
  const [currentSessionId, setCurrentSessionId] = useState('session1');
  const [inputValue, setInputValue] = useState('');

  const addMessage = (message) => {
    const updated = [...(conversations[currentSessionId] || []), message];
    setConversations({ ...conversations, [currentSessionId]: updated });
  };

  const switchSession = (sessionId) => {
    setCurrentSessionId(sessionId);
  };

  return (
    <ChatContext.Provider
      value={{
        inputValue,
        setInputValue,
        messages: conversations[currentSessionId] || [],
        addMessage,
        conversations,
        switchSession,
        currentSessionId,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => useContext(ChatContext);
