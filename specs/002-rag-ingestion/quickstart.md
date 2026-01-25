# Quickstart: RAG System for Book Content Ingestion

## Prerequisites

- Python 3.11+
- uv package manager
- Cohere API key
- Qdrant Cloud account and API key

## Setup

1. **Create the backend directory:**
```bash
mkdir backend
cd backend
```

2. **Initialize the project with uv:**
```bash
uv init
```

3. **Create the project structure:**
```bash
mkdir -p src/{crawler,chunker,embedding,storage} config tests
touch pyproject.toml main.py .env.example
touch src/{crawler,chunker,embedding,storage}/{__init__.py,url_fetcher.py,text_chunker.py,cohere_embedder.py,qdrant_storage.py}
touch config/settings.py
touch tests/{__init__.py,test_crawler.py,test_chunker.py,test_embedding.py,test_storage.py}
```

4. **Add dependencies to pyproject.toml:**
```toml
[project]
name = "rag-ingestion"
version = "0.1.0"
description = "RAG system for book content ingestion and storage"
requires-python = ">=3.11"

dependencies = [
    "cohere>=5.0.0",
    "qdrant-client>=1.8.0",
    "beautifulsoup4>=4.12.0",
    "requests>=2.31.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.5.0",
    "pytest>=8.0.0",
]
```

5. **Set up environment variables (.env.example):**
```
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
DOCUSAURUS_URLS=https://your-docusaurus-site.com
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_CONCURRENT_REQUESTS=5
REQUEST_DELAY=1.0
TIMEOUT=30
```

## Running the Pipeline

1. **Install dependencies:**
```bash
uv sync
```

2. **Run the ingestion pipeline:**
```bash
uv run python main.py
```

## Main Pipeline Flow

The main.py orchestrates the complete ingestion pipeline:

1. **Crawling**: Fetch and parse Docusaurus documentation pages
2. **Cleaning**: Extract main content, remove navigation and headers
3. **Chunking**: Split content into appropriately sized segments
4. **Embedding**: Generate vector embeddings using Cohere
5. **Storage**: Store embeddings and metadata in Qdrant Cloud