# Quickstart: Floating Chatbot UI Implementation

## Overview
This guide provides the essential steps to implement the floating chatbot UI for the Physical AI & Humanoid Robotics book website.

## Prerequisites
- Node.js 18+ installed
- Docusaurus project set up and running
- Existing RAG backend API available for chat interactions
- Basic knowledge of React and TypeScript

## Step 1: Create Chatbot Components

### 1.1 Create the main Chatbot component
Create `ai-book/src/components/Chatbot/Chatbot.tsx`:

```tsx
import React, { useState, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { sendMessageToBackend } from './api'; // Your API integration

interface ChatbotProps {
  // Props for the chatbot component
}

const Chatbot: React.FC<ChatbotProps> = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (text: string) => {
    // Add user message to UI
    const userMessage = { id: Date.now().toString(), text, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);

    setIsLoading(true);
    try {
      // Call backend API
      const response = await sendMessageToBackend(text);
      // Add bot response to UI
      const botMessage = { id: (Date.now() + 1).toString(), text: response, sender: 'bot', timestamp: new Date() };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      // Handle error
      const errorMessage = { id: (Date.now() + 2).toString(), text: 'Sorry, I encountered an error.', sender: 'bot', timestamp: new Date() };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chat-messages">
        {messages.map(message => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {isLoading && <div className="loading-indicator">Thinking...</div>}
      </div>
      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
};

export default Chatbot;
```

### 1.2 Create ChatMessage component
Create `ai-book/src/components/Chatbot/ChatMessage.tsx`:

```tsx
import React from 'react';

interface ChatMessageProps {
  message: any; // Use proper type
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  return (
    <div className={`chat-message ${message.sender}`}>
      <div className="message-content">{message.text}</div>
      <div className="message-timestamp">{message.timestamp.toLocaleTimeString()}</div>
    </div>
  );
};

export default ChatMessage;
```

### 1.3 Create ChatInput component
Create `ai-book/src/components/Chatbot/ChatInput.tsx`:

```tsx
import React, { useState } from 'react';

interface ChatInputProps {
  onSendMessage: (text: string) => void;
  disabled: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled }) => {
  const [inputText, setInputText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputText.trim() && !disabled) {
      onSendMessage(inputText);
      setInputText('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="chat-input-form">
      <input
        type="text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Type your question..."
        disabled={disabled}
        aria-label="Type your message"
      />
      <button type="submit" disabled={inputText.trim() === '' || disabled}>
        Send
      </button>
    </form>
  );
};

export default ChatInput;
```

## Step 2: Integrate Floating Icon and Panel into Root Component

### 2.1 Update Root.tsx
Modify `ai-book/src/theme/Root.tsx` to include the floating chatbot UI:

```tsx
import React, { useState, useEffect } from 'react';
import Chatbot from '../components/Chatbot/Chatbot';

const Root = ({ children }: { children: React.ReactNode }) => {
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  const toggleChatbot = () => {
    setIsChatbotOpen(!isChatbotOpen);
  };

  // Handle escape key to close chatbot
  useEffect(() => {
    const handleEscKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isChatbotOpen) {
        setIsChatbotOpen(false);
      }
    };

    window.addEventListener('keydown', handleEscKey);
    return () => window.removeEventListener('keydown', handleEscKey);
  }, [isChatbotOpen]);

  return (
    <div style={{ position: 'relative' }}>
      {children}

      {/* Floating Chatbot Icon */}
      <button
        onClick={toggleChatbot}
        aria-label={isChatbotOpen ? "Close chatbot" : "Open chatbot"}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '24px',
          zIndex: 1000,
          boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
          transition: 'all 0.3s ease'
        }}
      >
        💬
      </button>

      {/* Sliding Chatbot Panel */}
      {isChatbotOpen && (
        <div
          style={{
            position: 'fixed',
            top: '0',
            right: '0',
            width: '400px',
            height: '100vh',
            backgroundColor: 'white',
            boxShadow: '-2px 0 10px rgba(0,0,0,0.1)',
            zIndex: 999,
            transition: 'transform 0.3s ease',
            transform: isChatbotOpen ? 'translateX(0)' : 'translateX(100%)',
            display: 'flex',
            flexDirection: 'column'
          }}
          role="dialog"
          aria-modal="true"
          aria-label="Chat with book assistant"
        >
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '15px',
            borderBottom: '1px solid #e0e0e0',
            backgroundColor: '#007bff',
            color: 'white'
          }}>
            <h3 style={{ margin: 0, fontSize: '1.2em' }}>Book Assistant</h3>
            <button
              onClick={toggleChatbot}
              style={{
                background: 'none',
                border: 'none',
                color: 'white',
                fontSize: '24px',
                cursor: 'pointer',
                padding: '0',
                width: '30px',
                height: '30px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
              aria-label="Close chatbot"
            >
              ×
            </button>
          </div>
          <div style={{ flex: 1, overflowY: 'auto', padding: '15px' }}>
            <Chatbot />
          </div>
        </div>
      )}

      {/* Background overlay */}
      {isChatbotOpen && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            zIndex: 998,
            transition: 'opacity 0.3s ease'
          }}
          onClick={toggleChatbot}
          aria-hidden="true"
        />
      )}
    </div>
  );
};

export default Root;
```

## Step 3: Add CSS Styling

Create or update `ai-book/src/components/Chatbot/Chatbot.css`:

```css
.chatbot-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-message {
  max-width: 80%;
  padding: 10px 15px;
  border-radius: 18px;
  margin-bottom: 10px;
  position: relative;
}

.chat-message.user {
  align-self: flex-end;
  background-color: #007bff;
  color: white;
  border-bottom-right-radius: 4px;
}

.chat-message.bot {
  align-self: flex-start;
  background-color: #f1f0f0;
  color: #333;
  border-bottom-left-radius: 4px;
}

.message-timestamp {
  font-size: 0.7em;
  opacity: 0.7;
  margin-top: 5px;
  text-align: right;
}

.chat-input-form {
  display: flex;
  padding: 15px;
  border-top: 1px solid #e0e0e0;
  background-color: white;
}

.chat-input-form input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  margin-right: 10px;
  outline: none;
}

.chat-input-form input:focus {
  border-color: #007bff;
}

.chat-input-form button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.chat-input-form button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.loading-indicator {
  align-self: flex-start;
  padding: 10px 15px;
  background-color: #f1f0f0;
  border-radius: 18px;
  font-style: italic;
  color: #666;
}
```

## Step 4: Responsive Design

Add media queries for mobile responsiveness:

```css
/* Mobile styles */
@media (max-width: 768px) {
  [data attribute for the chat panel] {
    width: 100vw;
    right: 0;
  }

  .chat-message {
    max-width: 90%;
  }
}
```

## Step 5: Testing

1. Start the Docusaurus development server: `npm run start`
2. Verify the floating icon appears at the bottom-right of all pages
3. Click the icon to open the chat panel
4. Test the slide-in animation
5. Verify the panel can be closed using the X button or overlay click
6. Test keyboard navigation (Tab, Enter, Escape)
7. Test on different screen sizes and orientations
8. Verify no interference with existing page functionality

## Troubleshooting

- If the floating icon doesn't appear, check that Root.tsx is properly integrated with Docusaurus
- If animations are janky, ensure CSS transitions are optimized for performance
- If the chat panel blocks content, verify z-index values are appropriate
- For accessibility issues, ensure all interactive elements have proper ARIA attributes