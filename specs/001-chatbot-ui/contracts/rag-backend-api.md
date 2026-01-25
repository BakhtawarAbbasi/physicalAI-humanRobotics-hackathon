# API Contract: RAG Backend Integration

## Overview
This document specifies the API contract between the chatbot UI and the RAG backend service. The frontend will make HTTP requests to the backend to process user queries and receive contextual responses.

## Base Configuration
- **Base URL**: `http://localhost:8000` (development) or production backend URL
- **Content-Type**: `application/json`
- **Authentication**: None required (public API for book content)
- **Timeout**: 30 seconds recommended

## Endpoints

### POST /query
Process a user query against the RAG system and return a contextual response.

#### Request
```json
{
  "query": "What is Gazebo physics simulation?",
  "top_k": 3
}
```

**Request Fields:**
- `query` (string, required): The user's question, minimum 3 characters, maximum 1000 characters
- `top_k` (integer, optional): Number of source documents to retrieve, default 3, range 1-10

#### Response
```json
{
  "answer": "Gazebo physics simulation is a powerful tool that provides realistic simulation of robots within 3D environments...",
  "sources": [
    {
      "id": "doc-123",
      "title": "Gazebo Physics Chapter",
      "url": "https://book-site.com/docs/module-02/chapter-1-gazebo-physics",
      "snippet": "Gazebo provides realistic physics simulation...",
      "score": 0.85
    }
  ],
  "retrieved_chunks": [
    {
      "content": "Gazebo physics simulation is a powerful tool...",
      "source_url": "https://book-site.com/docs/module-02/chapter-1-gazebo-physics",
      "title": "Gazebo Physics Chapter",
      "score": 0.85,
      "chunk_index": 0
    }
  ],
  "success": true,
  "error_message": null
}
```

**Response Fields:**
- `answer` (string): The generated response to the user's query
- `sources` (array): Array of source references used in the response
- `retrieved_chunks` (array): Array of content chunks retrieved from the knowledge base
- `success` (boolean): Whether the query was processed successfully
- `error_message` (string, optional): Error message if success is false

#### Error Responses
- **400 Bad Request**: Invalid request format
- **408 Request Timeout**: Query took too long to process
- **500 Internal Server Error**: Backend processing error

### GET /health
Check the health status of the RAG backend.

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2025-12-28T15:30:00.000Z"
}
```

## Error Handling

### Client-Side Error Mapping
| HTTP Status | User Message | Action |
|-------------|--------------|---------|
| 400 | "Invalid query format. Please try rephrasing your question." | Allow user to retry with different query |
| 408 | "The query is taking longer than expected. Please try again." | Allow user to retry |
| 500 | "The service is temporarily unavailable. Please try again later." | Allow user to retry after delay |
| Network Error | "Unable to connect to the service. Please check your connection." | Allow user to retry |

### Validation Requirements
- All requests must include valid JSON with required fields
- Query strings must be properly sanitized to prevent injection attacks
- Responses must be validated against the expected schema before processing

## Performance Requirements
- API response time should be under 5 seconds for 95% of requests
- The frontend should show loading indicators during requests
- Timeouts should be handled gracefully with appropriate user feedback

## Security Considerations
- All communication should use HTTPS in production
- Input validation should prevent injection attacks
- No sensitive user data should be sent to the backend (queries are public book content)
- Responses should be sanitized before rendering to prevent XSS