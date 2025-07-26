import React, { useState } from 'react';
import UserInput from './UserInput';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);

  const sendMessage = async (userMessage) => {
    // Add user message
    const newUserMessage = { sender: 'user', text: userMessage };
    setMessages((prev) => [...prev, newUserMessage]);

    try {
      const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: userMessage,
          conversation_id: conversationId
        })
      });

      const data = await response.json();
      const aiMessage = { sender: 'ai', text: data.response };

      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error("API error:", err);
      setMessages((prev) => [...prev, { sender: 'ai', text: 'Error contacting AI server.' }]);
    }
  };

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <UserInput onSend={sendMessage} />
    </div>
  );
};

export default ChatWindow;
