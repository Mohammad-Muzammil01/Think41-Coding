// src/components/ConversationHistory.js
import React from 'react';
import { useChat } from '../context/ChatContext';
import './ConversationHistory.css';

const ConversationHistory = () => {
  const { conversations, switchSession, currentSessionId } = useChat();

  return (
    <div className="conversation-history">
      <h4>🕒 History</h4>
      <ul>
        {Object.keys(conversations).map((sessionId) => (
          <li
            key={sessionId}
            className={sessionId === currentSessionId ? 'active' : ''}
            onClick={() => switchSession(sessionId)}
          >
            {sessionId}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ConversationHistory;
