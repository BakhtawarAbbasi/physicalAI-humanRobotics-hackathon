// TypeScript interfaces for the Floating Chatbot UI

// Existing interfaces from the project
export interface Message {
  id: string;                    // Unique identifier for the message
  content: string;              // The text content of the message
  role: 'user' | 'assistant';   // The role of the message sender
  timestamp: Date;              // When the message was created/sent
  sources?: SourceReference[];  // Optional source citations for assistant responses
  status?: 'pending' | 'sent' | 'error'; // Status for user messages
}

export interface SourceReference {
  id: string;           // Unique identifier for the source
  title: string;        // Title of the source document/chapter
  url: string;          // URL to the original content
  snippet: string;      // Relevant excerpt from the source
  score: number;        // Relevance score (0-1)
}

export interface Conversation {
  id: string;                    // Unique identifier for the conversation
  messages: Message[];          // Array of messages in the conversation
  createdAt: Date;             // When the conversation was started
  lastActiveAt: Date;          // When the last message was sent
  isActive: boolean;           // Whether this is the current active conversation
}

export interface ChatState {
  conversation: Conversation;    // Current conversation data
  isLoading: boolean;           // Whether a response is being loaded
  error: string | null;         // Any current error message
  isInputEnabled: boolean;      // Whether the input field should be enabled
  shouldAutoScroll: boolean;    // Whether to auto-scroll to new messages
}

// API Request/Response Models
export interface QueryRequest {
  query: string;        // The user's question
  top_k?: number;       // Number of results to retrieve (default: 3)
  conversation_id?: string; // Optional conversation context identifier
}

export interface QueryResponse {
  answer: string;               // The answer text
  sources: SourceReference[];   // Source citations
  retrieved_chunks: RetrievedChunk[]; // Retrieved content chunks
  success: boolean;             // Whether the query was successful
  error_message?: string;       // Error message if success is false
}

export interface RetrievedChunk {
  content: string;              // The retrieved content chunk
  source_url: string;           // URL of the source
  title: string;                // Title of the source
  score: number;                // Relevance score
  chunk_index: number;          // Index of the chunk
}

// New interfaces required for the Floating Chatbot UI
export interface ChatbotUIState {
  isOpen: boolean;           // Whether the chat panel is open/closed
  isVisible: boolean;        // Whether the floating icon is visible
  isMinimized?: boolean;     // Whether the chat panel is minimized (if applicable)
}

export interface ChatSession {
  id: string;                // Unique session identifier
  messages: ChatMessage[];   // Array of messages in the conversation
  createdAt: Date;           // Session creation timestamp
  lastActive: Date;          // Last interaction timestamp
  context: ChatContext;      // Current page/context information
}

export interface ChatMessage {
  id: string;                // Unique message identifier
  content: string;           // Message text content
  sender: 'user' | 'bot';    // Message sender type
  timestamp: Date;           // Message timestamp
  status: 'sent' | 'pending' | 'error'; // Message sending status
}

export interface ChatContext {
  currentPage: string;       // Current page URL or identifier
  pageSection?: string;      // Current section within page (optional)
  bookSection?: string;      // Book section reference (if applicable)
}

// API Contract Types for Floating Chatbot
export interface SendMessageRequest {
  message: string;           // User's message text
  sessionId?: string;        // Existing session identifier (optional for new sessions)
  context?: ChatContext;     // Context information for RAG
}

export interface SendMessageResponse {
  success: boolean;          // Whether the request was successful
  response: string;          // Bot's response text
  sessionId: string;         // Session identifier (new or existing)
  sources?: string[];        // Source references for RAG responses
  timestamp: string;         // ISO timestamp of response
  error?: string;            // Error message if success is false
}

export interface StoredChatSession {
  id: string;
  messages: ChatMessage[];
  lastActive: number;        // Unix timestamp
  pageContext: string;       // Last page where chat was used
}