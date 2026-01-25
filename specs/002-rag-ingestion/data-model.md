# Data Model: RAG System for Book Content Ingestion and Storage

## Entity: ContentChunk

**Description**: Represents a segment of text extracted from a Docusaurus page

**Fields**:
- `id` (str): Unique identifier for the chunk (UUID)
- `content` (str): The actual text content of the chunk
- `source_url` (str): Original URL where the content was found
- `title` (str): Title of the page where content was found
- `section` (str): Section/heading context where content appears
- `chunk_index` (int): Position of this chunk within the original document
- `created_at` (datetime): Timestamp when chunk was created
- `embedding` (List[float]): Vector embedding of the content (optional, added after processing)

**Validation Rules**:
- `content` must not be empty
- `source_url` must be a valid URL
- `chunk_index` must be non-negative

## Entity: EmbeddingRecord

**Description**: A vector representation of content chunk stored in Qdrant with associated metadata

**Fields**:
- `id` (str): Unique identifier matching the ContentChunk
- `vector` (List[float]): The embedding vector (dimension depends on Cohere model)
- `metadata` (Dict[str, Any]): Metadata including source_url, title, section
- `created_at` (datetime): Timestamp when embedding was generated

**Validation Rules**:
- `vector` must have consistent dimensions
- `metadata` must include required fields (source_url, title)

## Entity: CrawlJob

**Description**: Represents a single ingestion process that includes configuration, status, and results

**Fields**:
- `id` (str): Unique identifier for the crawl job (UUID)
- `urls` (List[str]): List of URLs to crawl
- `status` (str): Current status (pending, in_progress, completed, failed)
- `start_time` (datetime): When the job started
- `end_time` (datetime): When the job completed/failed
- `processed_count` (int): Number of URLs successfully processed
- `failed_count` (int): Number of URLs that failed
- `error_details` (List[Dict]): Details of any errors encountered
- `config` (Dict[str, Any]): Configuration used for this crawl job

**Validation Rules**:
- `urls` must not be empty
- `status` must be one of the allowed values
- `processed_count` and `failed_count` must be non-negative

## Entity: ProcessingConfig

**Description**: Configuration parameters for the ingestion pipeline

**Fields**:
- `cohere_api_key` (str): API key for Cohere embedding service
- `qdrant_url` (str): URL for Qdrant vector database
- `qdrant_api_key` (str): API key for Qdrant database
- `chunk_size` (int): Maximum size of text chunks (default: 1000 characters)
- `chunk_overlap` (int): Overlap between chunks (default: 200 characters)
- `max_concurrent_requests` (int): Maximum concurrent HTTP requests (default: 5)
- `request_delay` (float): Delay between requests to avoid rate limiting (default: 1.0 seconds)
- `timeout` (int): HTTP request timeout in seconds (default: 30)

**Validation Rules**:
- `chunk_size` must be positive
- `chunk_overlap` must be non-negative and less than chunk_size
- `max_concurrent_requests` must be positive
- `request_delay` must be non-negative
- `timeout` must be positive