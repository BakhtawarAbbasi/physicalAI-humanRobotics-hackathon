// Mock API service for chat functionality
import { SendMessageRequest, SendMessageResponse, ChatContext } from './types';

// Mock API service for chat functionality
export const sendMessageToBackend = async (request: SendMessageRequest): Promise<SendMessageResponse> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));

  // In a real implementation, this would call the actual backend API
  // For now, we'll return mock responses based on the input
  const mockResponses: Record<string, string> = {
    'hello': 'Hello! I\'m your Book Assistant. How can I help you with the Physical AI & Humanoid Robotics content today?',
    'hi': 'Hi there! I\'m here to help you with questions about Physical AI & Humanoid Robotics. What would you like to know?',
    'help': 'I can help you understand concepts about Physical AI & Humanoid Robotics. Ask me about specific topics, chapters, or concepts from the book.',
    'test': 'This is a test response from the Book Assistant. The chat functionality is working correctly.',
    'default': 'Thank you for your question! Based on the Physical AI & Humanoid Robotics book content, I can provide detailed information about various topics. Could you please ask a more specific question?'
  };

  // Simple keyword matching for demo purposes
  const messageLower = request.message.toLowerCase();
  let responseText = mockResponses.default;

  for (const [keyword, response] of Object.entries(mockResponses)) {
    if (messageLower.includes(keyword)) {
      responseText = response;
      break;
    }
  }

  // For demo purposes, include some mock sources
  const sources = messageLower.includes('robotics') || messageLower.includes('ai')
    ? ['Chapter 3: Introduction to Robotics', 'Chapter 5: AI in Physical Systems']
    : [];

  return {
    success: true,
    response: responseText,
    sessionId: request.sessionId || `session_${Date.now()}`,
    sources: sources,
    timestamp: new Date().toISOString()
  };
};

// Mock function to get current page context
export const getCurrentPageContext = (): ChatContext => {
  return {
    currentPage: typeof window !== 'undefined' ? window.location.pathname : '',
    pageSection: '', // Could be populated based on scroll position or headings
    bookSection: '' // Could be populated based on the current book section
  };
};

// Mock function to save chat session to localStorage (if needed)
export const saveChatSession = (sessionId: string, messages: any[]) => {
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const sessionData = {
        id: sessionId,
        messages,
        lastActive: Date.now(),
        pageContext: typeof window !== 'undefined' ? window.location.pathname : ''
      };
      window.localStorage.setItem(`chat_session_${sessionId}`, JSON.stringify(sessionData));
    } catch (error) {
      console.warn('Could not save chat session to localStorage:', error);
    }
  }
};

// Mock function to load chat session from localStorage (if needed)
export const loadChatSession = (sessionId: string) => {
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const sessionData = window.localStorage.getItem(`chat_session_${sessionId}`);
      if (sessionData) {
        return JSON.parse(sessionData);
      }
    } catch (error) {
      console.warn('Could not load chat session from localStorage:', error);
    }
  }
  return null;
};