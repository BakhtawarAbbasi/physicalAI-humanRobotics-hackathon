# Data Model: FastAPI RAG Integration

## Entities

### QueryRequest
**Description**: The request payload sent from the frontend to the RAG agent API
- **query**: string - The question or query text from the user
- **top_k**: integer (optional) - Number of top results to retrieve (default: 5)

### QueryResponse
**Description**: The response payload returned from the RAG agent API to the frontend
- **answer**: string - The agent's response to the user's query
- **sources**: list[string] - List of source URLs for the retrieved content used in the response
- **retrieved_chunks**: list[RetrievedChunk] - Details about the content chunks that informed the response
- **success**: boolean - Whether the request was processed successfully
- **error_message**: string (optional) - Error message if request failed

### RetrievedChunk
**Description**: A segment of content retrieved from the vector store with metadata
- **content**: string - The actual text content retrieved from the vector store
- **source_url**: string - The URL where the original content was sourced from
- **title**: string - The title of the source document
- **score**: float - The similarity score for this retrieval result
- **chunk_index**: integer - The position of this chunk within the original document

### AgentResponse
**Description**: The internal response structure from the RAG agent before formatting
- **content**: string - The agent's answer content
- **retrieved_chunks**: list[RetrievedChunk] - The chunks that informed the response
- **metadata**: dict - Additional metadata about the response generation
- **processing_time**: float - Time taken to process the query in seconds

### ErrorResponse
**Description**: The response structure for API errors
- **error**: string - The error message
- **type**: string - The error type (e.g., "query_processing_error", "service_unavailable")
- **status_code**: integer - The HTTP status code to return
- **details**: dict (optional) - Additional error details for debugging