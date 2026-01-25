# Quickstart: RAG Retrieval Validation

## Prerequisites
- Python 3.11+
- Qdrant Cloud account and API key
- Cohere API key
- Valid `.env` file with required credentials

## Setup
1. Ensure your `.env` file contains:
   ```
   QDRANT_API_KEY="your-qdrant-api-key"
   QDRANT_URL="your-qdrant-url"
   COHERE_API_KEY="your-cohere-api-key"
   ```

2. Install dependencies:
   ```bash
   cd backend
   uv venv
   source .venv/Scripts/activate  # On Windows
   uv pip install -e .
   ```

## Usage
1. Run the retrieval validation script:
   ```bash
   python retrieve.py
   ```

2. The script will:
   - Connect to Qdrant using your credentials
   - Load existing vector collections
   - Execute test queries against the stored embeddings
   - Perform top-k similarity searches
   - Validate results using returned text, metadata, and source URLs

## Custom Queries
To test a custom query, modify the test queries in the script or pass as a command-line argument:
```bash
python retrieve.py --query "What is Gazebo physics simulation?"
```

## Expected Output
- Connection to Qdrant established successfully
- Vector collection information retrieved
- Test queries executed with relevant results
- Metadata validation passed (95%+ accuracy)
- All validation tests passed