# Quickstart: FastAPI RAG Integration

## Prerequisites
- Python 3.11+
- Valid `.env` file with required credentials in root directory
- Running Qdrant Cloud instance with content embeddings
- OpenRouter API key for agent responses

## Setup
1. Ensure your `.env` file contains:
   ```
   QDRANT_API_KEY="your-qdrant-api-key"
   QDRANT_URL="your-qdrant-url"
   COHERE_API_KEY="your-cohere-api-key"
   OPENROUTER_API_KEY="your-openrouter-api-key"
   ```

2. Install dependencies:
   ```bash
   cd backend
   uv venv
   source .venv/Scripts/activate  # On Windows
   uv pip install fastapi uvicorn python-dotenv
   ```

## Running the API Server
1. Start the FastAPI server:
   ```bash
   cd backend
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

2. Or run directly:
   ```bash
   python api.py
   ```

## API Usage
1. Send a query to the endpoint:
   ```bash
   curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is Gazebo physics simulation?", "top_k": 5}'
   ```

2. The API will:
   - Receive the query from the frontend
   - Process it through the RAG agent using existing retrieval pipeline
   - Retrieve relevant content from Qdrant
   - Generate a response using OpenRouter API
   - Return a JSON response with the answer and sources

## Expected Response Format
```json
{
  "answer": "Gazebo physics simulation is...",
  "sources": [
    "https://example.com/docs/module-02/chapter-1-gazebo-physics"
  ],
  "retrieved_chunks": [
    {
      "content": "Gazebo provides realistic physics simulation...",
      "source_url": "https://example.com/docs/module-02/chapter-1-gazebo-physics",
      "title": "Chapter 1 - Gazebo Physics Simulation",
      "score": 0.85,
      "chunk_index": 0
    }
  ],
  "success": true
}
```

## Testing
- API documentation available at: `http://localhost:8000/docs`
- Health check endpoint: `GET /health`
- Test query endpoint: `POST /query`