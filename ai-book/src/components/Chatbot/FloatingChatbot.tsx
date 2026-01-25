import React, { useState } from 'react';
import Chatbot from './Chatbot';
import './css/floating-chatbot.css';

const FloatingChatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const closeChatbot = () => {
    setIsOpen(false);
  };

  return (
    <>
      {!isOpen && (
        <div className="floating-chatbot">
          <button
            className="chatbot-icon"
            onClick={toggleChatbot}
            aria-label="Open chatbot"
          >
            <img
              src="/img/robot.png"
              alt="Chatbot"
              className="chatbot-icon-image"
              onError={(e) => {
                // Fallback to SVG if image fails to load
                const target = e.target as HTMLImageElement;
                target.style.display = 'none';
                const svg = target.parentElement?.querySelector('.chatbot-icon-svg');
                if (svg) svg.style.display = 'block';
              }}
            />
            {/* <svg
              xmlns="http://www.w3.org/2000/svg"
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="white"
              className="chatbot-icon-svg"
              style={{ display: 'none' }}
            >
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg> */}
          </button>
        </div>
      )}

      <div className={`chatbot-window-container ${isOpen ? 'open' : ''}`}>
        <div className="chatbot-header">
          <h3>Book Assistant</h3>
          <button
            className="close-chatbot-button"
            onClick={closeChatbot}
            aria-label="Close chatbot"
          >
            ×
          </button>
        </div>
        <div className="chat-messages-container">
          <Chatbot />
        </div>
      </div>
    </>
  );
};

export default FloatingChatbot;