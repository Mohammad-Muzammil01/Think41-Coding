// src/components/ChatWindow.js
import React from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import ConversationHistory from './ConversationHistory';
import './ChatWindow.css';

const ChatWindow = () => {
  return (
    <div className="chat-container">
      <ConversationHistory />
      <div className="chat-window">
        <div className="chat-header">🧠 AI Chatbot</div>
        <MessageList />
        <UserInput />
      </div>
    </div>
  );
};

export default ChatWindow;
