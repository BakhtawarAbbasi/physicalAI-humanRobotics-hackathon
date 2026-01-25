"""
Performance tests for the RAG system to ensure processing goals are met.
"""
import time
import pytest
from unittest.mock import Mock, patch
import asyncio

from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline
from src.common.models import ContentChunk


class TestPerformance:
    """Performance tests for the RAG system."""

    @pytest.fixture
    def config(self):
        """Create a mock configuration for testing."""
        config = Mock(spec=ProcessingConfig)
        config.cohere_api_key = "test-key"
        config.qdrant_url = "https://test.qdrant.com"
        config.qdrant_api_key = "test-qdrant-key"
        config.chunk_size = 1000
        config.chunk_overlap = 200
        config.max_concurrent_requests = 5
        config.request_delay = 0.1  # Reduced for testing
        config.timeout = 30
        return config

    def test_pipeline_processing_time_small_content(self, config):
        """Test processing time for small content set."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.CohereEmbedder'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock services to avoid external calls
            mock_chunks = [
                ContentChunk(
                    content="This is a test content chunk for performance testing. " * 10,
                    source_url="https://example.com/test",
                    title="Test Page"
                )
            ]
            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Measure processing time
            start_time = time.time()
            job = asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))
            end_time = time.time()

            processing_time = end_time - start_time

            # Performance goal: Small content should process quickly (under 5 seconds)
            assert processing_time < 5.0, f"Processing took {processing_time:.2f}s, expected < 5s"
            assert job.status == "completed"

    def test_pipeline_processing_time_medium_content(self, config):
        """Test processing time for medium content set."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.CohereEmbedder'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Create medium-sized content (more chunks)
            mock_chunks = []
            for i in range(10):
                mock_chunks.append(
                    ContentChunk(
                        content=f"This is test content chunk {i} for performance testing. " * 20,
                        source_url=f"https://example.com/test{i}",
                        title=f"Test Page {i}"
                    )
                )

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Measure processing time
            start_time = time.time()
            job = asyncio.run(pipeline.run_pipeline([f"https://example.com/test{i}" for i in range(10)]))
            end_time = time.time()

            processing_time = end_time - start_time

            # Performance goal: Medium content should process in reasonable time (under 30 seconds)
            assert processing_time < 30.0, f"Processing took {processing_time:.2f}s, expected < 30s"
            assert job.status == "completed"

    def test_memory_usage_during_processing(self, config):
        """Test memory usage during processing (conceptual test)."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.CohereEmbedder'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Create content that would normally use significant memory
            large_content = "This is a large content chunk for memory testing. " * 1000
            mock_chunks = [
                ContentChunk(
                    content=large_content,
                    source_url="https://example.com/large",
                    title="Large Content Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # For this test, we're just ensuring the pipeline doesn't crash with large content
            job = asyncio.run(pipeline.run_pipeline(["https://example.com/large"]))
            assert job.status == "completed"

    def test_concurrent_processing_efficiency(self, config):
        """Test efficiency of concurrent processing."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.CohereEmbedder'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            # Test with different concurrent request settings
            config.max_concurrent_requests = 10

            pipeline = IngestionPipeline(config)

            # Create multiple URLs to test concurrent processing
            urls = [f"https://example.com/test{i}" for i in range(5)]
            mock_chunks = []
            for i, url in enumerate(urls):
                mock_chunks.append(
                    ContentChunk(
                        content=f"Content for page {i}",
                        source_url=url,
                        title=f"Page {i}"
                    )
                )

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            start_time = time.time()
            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))  # No depth following for this test
            end_time = time.time()

            processing_time = end_time - start_time

            # With concurrent processing, multiple URLs should be handled efficiently
            assert processing_time < 10.0, f"Concurrent processing took too long: {processing_time:.2f}s"
            assert job.status == "completed"
            assert job.processed_count == len(urls)

    def test_chunking_performance(self, config):
        """Test performance of the chunking process."""
        from src.chunker.chunker_service import ChunkerService

        chunker_service = ChunkerService(config)

        # Create large content to test chunking performance
        large_content = "This is a large content chunk for performance testing. " * 1000
        test_chunk = ContentChunk(
            content=large_content,
            source_url="https://example.com/large",
            title="Large Content Page"
        )

        start_time = time.time()
        chunks = chunker_service.process_content_chunks([test_chunk])
        end_time = time.time()

        processing_time = end_time - start_time

        # Verify chunks were created properly
        assert len(chunks) > 0
        assert all(len(chunk.content) <= config.chunk_size for chunk in chunks)

        # Performance goal: Large content should be chunked efficiently (under 5 seconds)
        assert processing_time < 5.0, f"Chunking took {processing_time:.2f}s, expected < 5s"

    def test_embedding_generation_performance(self, config):
        """Test performance of embedding generation."""
        with patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            from src.embedding.embedding_service import EmbeddingService

            embedding_service = EmbeddingService(config)

            # Mock the embedder to return embeddings quickly
            embedding_service.embedder = Mock()
            mock_embeddings = []
            for i in range(5):  # 5 chunks
                mock_embeddings.append([0.1] * 1024)  # Mock 1024-dim embeddings

            embedding_service.embedder.generate_embeddings = Mock(return_value=mock_embeddings)
            embedding_service.embedder.embed_content_chunks = Mock(return_value=[
                ContentChunk(
                    content=f"Content chunk {i}",
                    source_url="https://example.com/test",
                    title="Test Page"
                ) for i in range(5)
            ])
            embedding_service.storage.validate_embedding_dimensions = Mock(return_value=True)
            embedding_service.storage.store_embeddings = Mock(return_value=True)

            # Create test content chunks
            test_chunks = [
                ContentChunk(
                    content=f"This is test content chunk {i} for embedding performance testing.",
                    source_url="https://example.com/test",
                    title="Test Page"
                ) for i in range(5)
            ]

            start_time = time.time()
            success = embedding_service.generate_and_store_embeddings(test_chunks)
            end_time = time.time()

            processing_time = end_time - start_time

            # Verify the process was successful
            assert success is True
            # Performance goal: Embedding 5 chunks should be efficient (under 10 seconds)
            assert processing_time < 10.0, f"Embedding generation took {processing_time:.2f}s, expected < 10s"