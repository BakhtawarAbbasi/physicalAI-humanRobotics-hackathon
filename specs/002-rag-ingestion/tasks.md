# Tasks: RAG System for Book Content Ingestion and Storage

**Feature**: RAG System for Book Content Ingestion and Storage
**Branch**: `002-rag-ingestion`
**Created**: 2025-12-25
**Spec**: specs/002-rag-ingestion/spec.md
**Plan**: specs/002-rag-ingestion/plan.md

## Phase 1: Setup

**Goal**: Initialize project structure and dependencies

- [X] T001 Create backend directory structure
- [X] T002 Initialize Python project with uv and create pyproject.toml
- [X] T003 Add dependencies to pyproject.toml (cohere, qdrant-client, beautifulsoup4, requests, python-dotenv, pydantic, pytest)
- [X] T004 Create .env.example file with required environment variables
- [X] T005 Create main.py entry point file
- [X] T006 Create configuration module at config/settings.py
- [X] T007 Create module __init__.py files in src/{crawler,chunker,embedding,storage}/__init__.py
- [X] T008 Create test directory structure with __init__.py files

## Phase 2: Foundational Components

**Goal**: Implement core infrastructure and configuration management

- [X] T009 [P] Implement configuration management in config/settings.py with Pydantic
- [X] T010 [P] Create ProcessingConfig model with validation rules
- [X] T011 [P] Create ContentChunk data model with validation rules
- [X] T012 [P] Create EmbeddingRecord data model with validation rules
- [X] T013 [P] Create CrawlJob data model with validation rules
- [X] T014 [P] Implement logging configuration for the application
- [X] T015 [P] Create error handling base classes and exceptions

## Phase 3: User Story 1 - Content Ingestion Pipeline

**Goal**: Implement URL crawling and HTML parsing functionality

**Independent Test**: Run the ingestion pipeline on a sample Docusaurus site and verify that content is properly crawled, cleaned, and stored as embeddings in Qdrant.

**Acceptance Scenarios**:
1. Given a deployed Docusaurus site URL, when the ingestion pipeline runs, then all public pages are crawled and text content is extracted without HTML tags or navigation elements
2. Given crawled content, when the text cleaning process runs, then only main content is retained while removing headers, footers, and navigation elements

- [X] T016 [P] [US1] Implement URL fetching in src/crawler/url_fetcher.py with rate limiting and error handling
- [X] T017 [P] [US1] Implement HTML parsing and cleaning in src/crawler/html_parser.py with BeautifulSoup
- [X] T018 [P] [US1] Create URL crawler service that coordinates fetching and parsing
- [X] T019 [P] [US1] Implement Docusaurus-specific HTML extraction to get main content only
- [X] T020 [US1] Add support for following links within the same domain
- [X] T021 [US1] Implement URL validation and filtering to avoid external links
- [X] T022 [US1] Add error handling for network timeouts and invalid URLs
- [ ] T023 [US1] Create basic test for URL fetching functionality
- [ ] T024 [US1] Create test for HTML parsing and cleaning

## Phase 4: User Story 3 - Content Chunking and Metadata Management

**Goal**: Implement text chunking and metadata preservation functionality

**Independent Test**: Verify that content is properly chunked with appropriate overlap and metadata is preserved for each chunk.

**Acceptance Scenarios**:
1. Given long text content, when chunking algorithm processes it, then content is divided into appropriately sized chunks with minimal semantic disruption
2. Given content chunks, when they are stored in Qdrant, then metadata including source URL, section, and context are preserved

- [X] T025 [P] [US3] Implement text chunking algorithm in src/chunker/text_chunker.py
- [X] T026 [P] [US3] Add chunk overlap functionality to preserve semantic context
- [X] T027 [P] [US3] Implement metadata extraction and preservation for chunks
- [X] T028 [US3] Add chunk validation to ensure content quality
- [X] T029 [US3] Create chunking service that coordinates chunking operations
- [X] T030 [US3] Implement chunk size and overlap configuration
- [ ] T031 [US3] Create test for text chunking functionality
- [ ] T032 [US3] Create test for metadata preservation

## Phase 5: User Story 2 - Text Embedding and Storage

**Goal**: Implement Cohere embedding generation and Qdrant storage functionality

**Independent Test**: Provide text chunks to the embedding system and verify that vectors are properly generated and stored in Qdrant.

**Acceptance Scenarios**:
1. Given cleaned text content, when Cohere embedding model processes it, then vector embeddings are generated with consistent dimensions and stored in Qdrant
2. Given stored embeddings in Qdrant, when a search is performed, then relevant content chunks can be retrieved based on semantic similarity

- [ ] T033 [P] [US2] Implement Cohere embedding client in src/embedding/cohere_embedder.py
- [ ] T034 [P] [US2] Create Qdrant storage client in src/storage/qdrant_storage.py
- [ ] T035 [P] [US2] Implement embedding generation and storage service
- [ ] T036 [US2] Add vector dimension validation and consistency checks
- [ ] T037 [US2] Implement Qdrant collection setup and indexing
- [ ] T038 [US2] Add metadata storage with embeddings in Qdrant
- [ ] T039 [US2] Implement error handling for API rate limits and failures
- [ ] T040 [US2] Create test for embedding generation
- [ ] T041 [US2] Create test for Qdrant storage operations

## Phase 6: Main Pipeline Integration

**Goal**: Integrate all components into a cohesive ingestion pipeline

- [ ] T042 [P] Create main ingestion pipeline service that orchestrates all components
- [ ] T043 [P] Implement CrawlJob management and status tracking
- [ ] T044 [P] Add progress reporting and monitoring to the pipeline
- [ ] T045 Integrate URL crawling with text chunking
- [ ] T046 Integrate text chunking with embedding generation
- [ ] T047 Integrate embedding generation with Qdrant storage
- [ ] T048 Add comprehensive error handling across the entire pipeline
- [ ] T049 Implement pipeline configuration and command-line interface
- [ ] T050 Add pipeline validation and quality checks

## Phase 7: Testing and Validation

**Goal**: Implement comprehensive tests and validate the complete pipeline

- [ ] T051 Create integration tests for the complete ingestion pipeline
- [ ] T052 Add performance tests to ensure processing goals are met
- [ ] T053 Implement end-to-end tests with sample Docusaurus sites
- [ ] T054 Add edge case testing for error conditions and rate limits
- [ ] T055 Create validation tests for success criteria (95% crawl success, etc.)

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Finalize the implementation with proper documentation and deployment readiness

- [ ] T056 Add comprehensive documentation to all modules
- [ ] T057 Create README with setup and usage instructions
- [ ] T058 Add configuration validation and environment setup checks
- [ ] T059 Implement graceful shutdown and cleanup procedures
- [ ] T060 Add monitoring and metrics collection
- [ ] T061 Create deployment configuration and scripts
- [ ] T062 Perform final integration testing with real Docusaurus sites

## Dependencies

- **US1 (P1)**: Content Ingestion Pipeline - Foundation for all other stories
- **US3 (P2)**: Content Chunking - Depends on US1 (needs crawled content)
- **US2 (P1)**: Text Embedding and Storage - Depends on US3 (needs chunks)

## Parallel Execution Examples

**Within US1**: T016 (URL fetching) and T017 (HTML parsing) can run in parallel as they are in different modules.

**Within US2**: T033 (Cohere embedder) and T034 (Qdrant storage) can be developed in parallel as they are separate services.

**Across stories**: T016-T017 (US1), T025-T027 (US3), and T033-T034 (US2) can be developed in parallel since foundational components are in place.

## Implementation Strategy

**MVP Scope**: Focus on US1 (Content Ingestion) and basic US2 (Embedding) for initial working version.
**Incremental Delivery**:
1. Complete Phase 1-2 (Setup + Foundation)
2. Complete US1 (Crawling)
3. Complete US3 (Chunking)
4. Complete US2 (Embedding + Storage)
5. Complete integration and testing