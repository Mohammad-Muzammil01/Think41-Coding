// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { ChatProvider } from './context/ChatContext'; // ✅ Import

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ChatProvider> {/* ✅ Wrap App */}
      <App />
    </ChatProvider>
  </React.StrictMode>
);

reportWebVitals();
