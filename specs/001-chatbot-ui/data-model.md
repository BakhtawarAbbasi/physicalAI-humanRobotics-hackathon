# Data Model: Chatbot UI

## Core Data Structures

### Message
Represents a single message in the chat conversation.

```typescript
interface Message {
  id: string;                    // Unique identifier for the message
  content: string;              // The text content of the message
  role: 'user' | 'assistant';   // The role of the message sender
  timestamp: Date;              // When the message was created/sent
  sources?: SourceReference[];  // Optional source citations for assistant responses
  status?: 'pending' | 'sent' | 'error'; // Status for user messages
}
```

### SourceReference
Represents a citation to the source content that was used in an assistant response.

```typescript
interface SourceReference {
  id: string;           // Unique identifier for the source
  title: string;        // Title of the source document/chapter
  url: string;          // URL to the original content
  snippet: string;      // Relevant excerpt from the source
  score: number;        // Relevance score (0-1)
}
```

### Conversation
Represents a complete conversation session with message history.

```typescript
interface Conversation {
  id: string;                    // Unique identifier for the conversation
  messages: Message[];          // Array of messages in the conversation
  createdAt: Date;             // When the conversation was started
  lastActiveAt: Date;          // When the last message was sent
  isActive: boolean;           // Whether this is the current active conversation
}
```

### ChatState
Represents the current state of the chat interface.

```typescript
interface ChatState {
  conversation: Conversation;    // Current conversation data
  isLoading: boolean;           // Whether a response is being loaded
  error: string | null;         // Any current error message
  isInputEnabled: boolean;      // Whether the input field should be enabled
  shouldAutoScroll: boolean;    // Whether to auto-scroll to new messages
}
```

### API Request/Response Models

#### Query Request
Sent to the RAG backend API when a user submits a question.

```typescript
interface QueryRequest {
  query: string;        // The user's question
  top_k?: number;       // Number of results to retrieve (default: 3)
  conversation_id?: string; // Optional conversation context identifier
}
```

#### Query Response
Received from the RAG backend API when a response is ready.

```typescript
interface QueryResponse {
  answer: string;               // The answer text
  sources: SourceReference[];   // Source citations
  retrieved_chunks: RetrievedChunk[]; // Retrieved content chunks
  success: boolean;             // Whether the query was successful
  error_message?: string;       // Error message if success is false
}

interface RetrievedChunk {
  content: string;              // The retrieved content chunk
  source_url: string;           // URL of the source
  title: string;                // Title of the source
  score: number;                // Relevance score
  chunk_index: number;          // Index of the chunk
}
```

## Validation Rules

### Message Validation
- `content` must be non-empty string with maximum length of 2000 characters
- `role` must be either 'user' or 'assistant'
- `timestamp` must be a valid date/time
- For assistant messages with sources, all source fields must be properly formatted

### SourceReference Validation
- `url` must be a valid URL format
- `title` must be non-empty string with maximum 200 characters
- `snippet` must be non-empty string with maximum 500 characters
- `score` must be between 0 and 1

### QueryRequest Validation
- `query` must be non-empty string with minimum 3 characters and maximum 1000 characters
- `top_k` must be between 1 and 10 if provided
- `conversation_id` must be a valid UUID format if provided

### QueryResponse Validation
- `answer` must be non-empty string if success is true
- `sources` must be an array of valid SourceReference objects
- `success` must be a boolean value

## State Transitions

### Message Status Transitions
```
'pending' → 'sent' (on successful API response)
'pending' → 'error' (on API error or timeout)
```

### ChatState Transitions
```
Initial → Ready (when component mounts)
Ready → Loading (when user submits message)
Loading → Ready (when API response received)
Loading → Error (when API error occurs)
Error → Ready (when user dismisses error or sends new message)
```