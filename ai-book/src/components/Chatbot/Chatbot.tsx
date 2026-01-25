import React, { useState, useEffect, useRef } from 'react';
import ChatWindow from './ChatWindow';
import MessageInput from './MessageInput';
import { ChatState, Conversation, Message, QueryResponse } from './types';
import { apiService } from './services/apiService';
import { validateMessageContent } from './utils/validation';
import './css/chatbot.css';

const Chatbot: React.FC = () => {
  const [chatState, setChatState] = useState<ChatState>({
    conversation: {
      id: 'conv-' + Date.now(),
      messages: [],
      createdAt: new Date(),
      lastActiveAt: new Date(),
      isActive: true,
    },
    isLoading: false,
    error: null,
    isInputEnabled: true,
    shouldAutoScroll: true,
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (chatState.shouldAutoScroll) {
      scrollToBottom();
    }
  }, [chatState.conversation.messages, chatState.isLoading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Clear the conversation history
  const handleClearConversation = () => {
    setChatState(prev => ({
      ...prev,
      conversation: {
        id: 'conv-' + Date.now(),
        messages: [],
        createdAt: new Date(),
        lastActiveAt: new Date(),
        isActive: true,
      },
      error: null
    }));
  };

  // Sanitize input to prevent XSS
  const sanitizeInput = (input: string): string => {
    // Basic XSS prevention - remove potentially dangerous tags
    return input
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/javascript:/gi, '')
      .replace(/on\w+="[^"]*"/gi, '');
  };

  const handleSendMessage = async (messageText: string) => {
    // Sanitize input
    const sanitizedMessage = sanitizeInput(messageText);

    // Validate the message
    const validation = validateMessageContent(sanitizedMessage);
    if (!validation.isValid) {
      setChatState(prev => ({
        ...prev,
        error: validation.error
      }));
      return;
    }

    // Create user message
    const userMessage: Message = {
      id: 'msg-' + Date.now(),
      content: sanitizedMessage,
      role: 'user',
      timestamp: new Date(),
      status: 'pending'
    };

    // Add user message to conversation
    setChatState(prev => ({
      ...prev,
      conversation: {
        ...prev.conversation,
        messages: [...prev.conversation.messages, userMessage],
        lastActiveAt: new Date()
      },
      isLoading: true,
      error: null
    }));

    try {
      // Call the RAG backend API
      const response = await apiService.queryRagBackend({
        query: sanitizedMessage,
        top_k: 3
      });

      // Create assistant message based on API response
      const assistantMessage: Message = {
        id: 'msg-' + Date.now(),
        content: response.answer,
        role: 'assistant',
        timestamp: new Date(),
        sources: response.sources
      };

      // Update chat state with assistant response
      setChatState(prev => ({
        ...prev,
        conversation: {
          ...prev.conversation,
          messages: [...prev.conversation.messages, assistantMessage],
          lastActiveAt: new Date()
        },
        isLoading: false,
        error: response.success ? null : response.error_message || 'Unknown error occurred'
      }));
    } catch (error: any) {
      // Handle error
      setChatState(prev => ({
        ...prev,
        isLoading: false,
        error: error.message || 'An error occurred while processing your request'
      }));
    }
  };

  // Retry failed request
  const handleRetry = async () => {
    if (chatState.error) {
      // If there was an error, clear it and reset input enabled state
      setChatState(prev => ({
        ...prev,
        error: null,
        isInputEnabled: true
      }));
    }
  };

  return (
    <>
      <ChatWindow
        messages={chatState.conversation.messages}
        isLoading={chatState.isLoading}
      />
      <div ref={messagesEndRef} />
      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={chatState.isLoading || !chatState.isInputEnabled}
      />
      {chatState.error && (
        <div className="chat-error">
          {chatState.error}
          <button onClick={handleRetry} className="retry-button">Retry</button>
        </div>
      )}
    </>
  );
};

export default Chatbot;