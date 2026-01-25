# RAG System for Book Content Ingestion and Storage

A comprehensive Retrieval-Augmented Generation (RAG) system designed for ingesting and storing book content and documentation from Docusaurus sites. The system provides a complete pipeline for crawling, processing, embedding, and storing content for semantic search and retrieval.

## Features

- **URL Crawling**: Efficiently crawl Docusaurus documentation sites with configurable depth
- **Content Extraction**: Extract clean text content while preserving important metadata
- **Text Chunking**: Smart chunking with overlap to maintain semantic context
- **Embedding Generation**: Generate high-quality embeddings using Cohere API
- **Vector Storage**: Store embeddings in Qdrant Cloud for fast semantic search
- **Job Management**: Track and monitor pipeline jobs with detailed status reporting
- **Error Handling**: Comprehensive error handling and retry mechanisms
- **CLI Interface**: Command-line interface for easy pipeline execution

## Architecture

The system is organized into several key components:

- `src/crawler/`: URL fetching, HTML parsing, and content extraction
- `src/chunker/`: Text chunking with overlap and validation
- `src/embedding/`: Embedding generation using Cohere API
- `src/storage/`: Vector storage in Qdrant Cloud
- `src/pipeline/`: Main orchestration and job management
- `config/`: Configuration management with Pydantic validation

## Prerequisites

- Python 3.11+
- Cohere API key
- Qdrant Cloud account and API key
- uv package manager (recommended) or pip

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Environment variables:**
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant Cloud cluster URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `DOCUSAURUS_URLS`: URLs to crawl (comma-separated)
   - `CHUNK_SIZE`: Size of text chunks (default: 1000)
   - `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
   - `MAX_CONCURRENT_REQUESTS`: Max concurrent requests (default: 5)
   - `REQUEST_DELAY`: Delay between requests in seconds (default: 1.0)
   - `TIMEOUT`: Request timeout in seconds (default: 30)

## Usage

### Command Line Interface

Run the ingestion pipeline using the CLI:

```bash
# Basic usage
python cli.py --urls https://example.com/docs

# With custom parameters
python cli.py --urls https://example.com/docs --depth 2 --chunk-size 1500 --chunk-overlap 300

# Multiple URLs
python cli.py --urls https://example.com/docs https://example.com/api --max-concurrent 10

# Verbose output
python cli.py --urls https://example.com/docs --verbose
```

### Programmatic Usage

Run the pipeline programmatically:

```python
import asyncio
from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline

async def main():
    config = ProcessingConfig()
    pipeline = IngestionPipeline(config)

    urls = ["https://example.com/docs"]
    job = await pipeline.run_pipeline(urls, max_depth=1)

    print(f"Pipeline completed with status: {job.status}")
    print(f"Processed {job.processed_count} content chunks")

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

The system uses Pydantic for configuration validation. Configuration can be provided via:

1. Environment variables (highest priority)
2. `.env` file
3. Default values

Key configuration parameters:

- `chunk_size`: Size of text chunks (default: 1000)
- `chunk_overlap`: Overlap between chunks (default: 200)
- `max_concurrent_requests`: Maximum concurrent requests (default: 5)
- `request_delay`: Delay between requests (default: 1.0s)
- `timeout`: Request timeout (default: 30s)

## Pipeline Flow

1. **Crawling**: Fetch URLs and extract clean text content
2. **Chunking**: Split content into appropriately sized chunks with overlap
3. **Validation**: Validate chunk quality and content
4. **Embedding**: Generate vector embeddings using Cohere
5. **Storage**: Store embeddings in Qdrant with metadata
6. **Tracking**: Monitor job progress and status

## Job Management

The system provides comprehensive job management:

- **Job Creation**: Create jobs with specified URLs and configuration
- **Status Tracking**: Monitor job progress (pending, in_progress, completed, failed)
- **Progress Reporting**: Track processed vs failed items
- **Error Tracking**: Detailed error logging with timestamps
- **Job Listing**: List all jobs and their status

## Error Handling

The system includes robust error handling:

- Network timeout and connection error handling
- Rate limit detection and backoff
- Content validation and quality checks
- Graceful degradation on partial failures
- Comprehensive error logging and reporting

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_integration_pipeline.py

# Run with coverage
pytest --cov=src
```

## Performance

The system is optimized for:

- Concurrent URL fetching with configurable limits
- Efficient text chunking algorithms
- Batched embedding generation
- Optimized vector storage operations
- Memory-efficient processing of large content

## Security

- API keys stored in environment variables
- Input validation and sanitization
- Rate limiting to prevent API abuse
- Secure connection to external services

## Monitoring

The system provides:

- Detailed logging with configurable levels
- Job progress tracking
- Performance metrics
- Error rate monitoring
- Content quality metrics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

[Specify your license here]

## Support

For support, please open an issue in the repository or contact [contact information].