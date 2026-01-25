# Quickstart: RAG Agent with OpenAI SDK

## Prerequisites
- Python 3.11+
- OpenAI API key
- Qdrant Cloud account and API key
- Valid `.env` file with required credentials

## Setup
1. Ensure your `.env` file contains:
   ```
   OPENAI_API_KEY="your-openai-api-key"
   QDRANT_API_KEY="your-qdrant-api-key"
   QDRANT_URL="your-qdrant-url"
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install openai qdrant-client python-dotenv
   ```

## Usage
1. Run the agent:
   ```bash
   python agent.py
   ```

2. The agent will:
   - Initialize using the OpenAI Agent SDK
   - Integrate retrieval by calling existing Qdrant search logic
   - Respond using retrieved book content only
   - Validate that responses are grounded in retrieved content

## Custom Queries
To test with a custom query:
```bash
python agent.py --query "What is Gazebo physics simulation?"
```

## Expected Output
- OpenAI agent initialized successfully
- Retrieval tool connected to Qdrant
- Relevant content chunks retrieved for queries
- Responses grounded in book content with proper citations
- 95%+ accuracy in content grounding