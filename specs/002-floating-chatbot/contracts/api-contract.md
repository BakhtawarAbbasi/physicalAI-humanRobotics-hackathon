# API Contract: Chatbot Backend Integration

## Overview
This document defines the API contract between the floating chatbot UI and the backend RAG system.

## Base URL
`/api/chat` (or as configured in environment)

## Endpoints

### POST /api/chat/send
Send a message to the chatbot and receive a response.

#### Request
```json
{
  "message": "User's question or message",
  "sessionId": "Optional session identifier",
  "context": {
    "currentPage": "Current page URL or identifier",
    "bookSection": "Optional book section reference"
  }
}
```

#### Response
```json
{
  "success": true,
  "response": "Bot's response to the user",
  "sessionId": "Session identifier (new or existing)",
  "sources": ["Array of source references for RAG responses"],
  "timestamp": "ISO timestamp of response"
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Error message describing the issue",
  "timestamp": "ISO timestamp of error"
}
```

## Message Format
- **message**: String, required, maximum 1000 characters
- **sessionId**: String, optional, 36 characters (UUID format)
- **context**: Object, optional, contains page context information

## Response Format
- **success**: Boolean, indicates if request was successful
- **response**: String, the bot's response text
- **sessionId**: String, unique identifier for the conversation session
- **sources**: Array of strings, references to source material used in response
- **timestamp**: ISO 8601 formatted timestamp

## Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Authentication
Bearer token authentication may be required (as configured in the system).

## Rate Limiting
- Maximum 10 requests per minute per session
- Responses cached for 5 minutes to prevent duplicate processing