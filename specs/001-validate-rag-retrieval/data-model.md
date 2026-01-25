# Data Model: RAG Retrieval Validation

## Entities

### Retrieved Text Chunk
**Description**: A segment of content retrieved from the vector store, containing the actual text content and associated metadata
- **content**: string - The actual text content retrieved from the vector store
- **source_url**: string - The URL where the original content was sourced from
- **title**: string - The title of the source document
- **section**: string - The section of the document where this chunk originated
- **chunk_index**: integer - The position of this chunk within the original document
- **score**: float - The similarity score for this retrieval result

### Query Vector
**Description**: The embedding representation of a user query used for semantic similarity search
- **vector**: list[float] - The numerical embedding vector representation of the query
- **text**: string - The original text of the query
- **model**: string - The model used to generate the embedding

### Search Result
**Description**: The result of a top-k search operation
- **retrieved_chunks**: list[Retrieved Text Chunk] - The k most relevant chunks retrieved
- **query**: Query Vector - The query vector used for the search
- **execution_time**: float - Time taken to execute the search in seconds
- **total_candidates**: integer - Total number of vectors considered during search

### Validation Result
**Description**: The result of validation performed on retrieved content
- **is_valid**: boolean - Whether the validation passed
- **metadata_accuracy**: float - Percentage of chunks with accurate metadata
- **content_accuracy**: float - Percentage of chunks with accurate content
- **errors**: list[string] - List of validation errors encountered
- **warnings**: list[string] - List of validation warnings