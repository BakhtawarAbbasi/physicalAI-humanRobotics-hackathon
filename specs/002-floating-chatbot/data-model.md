# Data Model: Floating Chatbot UI

## Overview
The Floating Chatbot UI has minimal data requirements as it's primarily a presentation layer. The data model focuses on the state management and message structure for the chat functionality.

## State Management

### UI State
```typescript
interface ChatbotUIState {
  isOpen: boolean;           // Whether the chat panel is open/closed
  isVisible: boolean;        // Whether the floating icon is visible
  isMinimized: boolean;      // Whether the chat panel is minimized (if applicable)
}
```

### Chat Session State
```typescript
interface ChatSession {
  id: string;                // Unique session identifier
  messages: ChatMessage[];   // Array of messages in the conversation
  createdAt: Date;           // Session creation timestamp
  lastActive: Date;          // Last interaction timestamp
  context: ChatContext;      // Current page/context information
}

interface ChatMessage {
  id: string;                // Unique message identifier
  content: string;           // Message text content
  sender: 'user' | 'bot';    // Message sender type
  timestamp: Date;           // Message timestamp
  status: 'sent' | 'pending' | 'error'; // Message sending status
}

interface ChatContext {
  currentPage: string;       // Current page URL or identifier
  pageSection?: string;      // Current section within page (optional)
  bookSection?: string;      // Book section reference (if applicable)
}
```

## Component Data Flow

### FloatingIcon Component
- **Inputs**:
  - `isOpen` (boolean) - Current open state
  - `onClick` (function) - Handler for icon click
  - `isVisible` (boolean) - Whether icon should be displayed
- **State**: None (mostly presentational)
- **Outputs**: Click events to toggle chat panel

### ChatPanel Component
- **Inputs**:
  - `isOpen` (boolean) - Whether panel should be visible
  - `onClose` (function) - Handler for close button
  - `messages` (ChatMessage[]) - Current conversation messages
  - `onSendMessage` (function) - Handler for sending new messages
- **State**:
  - Current input text
  - Loading states for message sending
  - Scroll position for message history
- **Outputs**: New messages, close events

### ChatMessage Component
- **Inputs**:
  - `message` (ChatMessage) - The message to display
  - `isUserMessage` (boolean) - Whether this is a user or bot message
- **State**: None (presentational component)
- **Outputs**: None

### ChatInput Component
- **Inputs**:
  - `onSendMessage` (function) - Handler for sending messages
  - `disabled` (boolean) - Whether input is disabled
- **State**:
  - Current input text
  - Input focus state
- **Outputs**: New message text

## API Contracts (for backend integration)

### Message Exchange
```typescript
interface SendMessageRequest {
  message: string;           // User's message text
  sessionId?: string;        // Existing session ID (optional for new sessions)
  context?: ChatContext;     // Context information for RAG
}

interface SendMessageResponse {
  response: string;          // Bot's response text
  sessionId: string;         // Session ID (new or existing)
  sources?: string[];        // Source references for RAG responses
  status: 'success' | 'error';
  error?: string;            // Error message if status is 'error'
}
```

## Local Storage (if needed for persistence)

### Session Persistence
```typescript
interface StoredChatSession {
  id: string;
  messages: ChatMessage[];
  lastActive: number;        // Unix timestamp
  pageContext: string;       // Last page where chat was used
}
```

## Animation State
- Open/close transition states
- Loading indicators
- Message sending/receiving states