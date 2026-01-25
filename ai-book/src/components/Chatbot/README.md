# Chatbot Component

A production-ready chatbot UI component integrated with the RAG backend API for the book website.

## Overview

This component provides a chat interface that allows users to ask questions about book content and receive contextual answers from the RAG backend system. The component handles message display, user input, API communication, and error handling.

## Features

- Responsive chat interface with message history
- Real-time interaction with the RAG backend
- Markdown rendering for responses
- Source citations with clickable links
- Auto-scrolling to latest messages
- Message timestamps
- Loading indicators
- Error handling and retry functionality
- Conversation history clearing
- Accessibility support

## Usage

```tsx
import Chatbot from './components/Chatbot/Chatbot';

function App() {
  return (
    <div className="app">
      <Chatbot />
    </div>
  );
}
```

## Environment Variables

- `REACT_APP_RAG_API_URL` - The URL of the RAG backend API (default: http://localhost:8000)

## Component Structure

- `Chatbot.tsx` - Main chatbot component with state management
- `ChatWindow.tsx` - Component for displaying message history
- `MessageInput.tsx` - Component for user input with send button
- `MessageBubble.tsx` - Component for displaying individual messages
- `LoadingIndicator.tsx` - Component for loading state visualization
- `types.ts` - TypeScript interfaces for data structures
- `services/apiService.ts` - API communication logic
- `utils/validation.ts` - Input validation utilities
- `css/chatbot.css` - Component styling

## API Integration

The component communicates with the RAG backend API at the following endpoints:

- `POST /query` - Submit a query and receive a response
- `GET /health` - Check the health status of the backend

## Security

- Input sanitization to prevent XSS attacks
- Validation of all user inputs
- Proper encoding of content before display

## Accessibility

- ARIA labels for screen readers
- Keyboard navigation support
- Focus indicators
- Reduced motion support for animations