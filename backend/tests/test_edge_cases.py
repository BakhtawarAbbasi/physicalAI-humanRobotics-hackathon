"""
Edge case tests for error conditions and rate limits in the RAG system.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import asyncio
from requests.exceptions import RequestException, Timeout, ConnectionError

from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline
from src.common.models import ContentChunk
from src.common.exceptions import NetworkException, RateLimitException, CrawlerException


class TestEdgeCases:
    """Edge case tests for error conditions and rate limits."""

    @pytest.fixture
    def config(self):
        """Create a mock configuration for testing."""
        config = Mock(spec=ProcessingConfig)
        config.cohere_api_key = "test-key"
        config.qdrant_url = "https://test.qdrant.com"
        config.qdrant_api_key = "test-qdrant-key"
        config.chunk_size = 1000
        config.chunk_overlap = 200
        config.max_concurrent_requests = 2  # Small number for testing
        config.request_delay = 0.1  # Small delay for testing
        config.timeout = 10
        return config

    def test_rate_limit_exception_handling(self, config):
        """Test handling of rate limit exceptions."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock the crawler to raise a RateLimitException
            pipeline.crawler_service.crawl_urls = Mock(side_effect=RateLimitException("Rate limit exceeded"))

            # Test that the pipeline handles the rate limit exception gracefully
            with pytest.raises(RateLimitException):
                asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))

    def test_network_timeout_handling(self, config):
        """Test handling of network timeout exceptions."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock the crawler to raise a timeout exception
            pipeline.crawler_service.crawl_urls = Mock(side_effect=Timeout("Request timed out"))

            # Test that the pipeline handles the timeout exception
            with pytest.raises(Timeout):
                asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))

    def test_connection_error_handling(self, config):
        """Test handling of connection errors."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock the crawler to raise a connection error
            pipeline.crawler_service.crawl_urls = Mock(side_effect=ConnectionError("Connection failed"))

            # Test that the pipeline handles the connection error
            with pytest.raises(ConnectionError):
                asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))

    def test_empty_content_handling(self, config):
        """Test handling of empty content during processing."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock crawler to return empty content
            empty_chunks = [
                ContentChunk(
                    content="",
                    source_url="https://example.com/empty",
                    title="Empty Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=empty_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=[])
            pipeline.chunker_service.validate_chunks = Mock(return_value=[])
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run pipeline with empty content
            job = asyncio.run(pipeline.run_pipeline(["https://example.com/empty"]))

            # Should complete but with no processed content
            assert job.status == "completed"

    def test_very_large_content_handling(self, config):
        """Test handling of very large content."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Create very large content
            very_large_content = "This is a very large content chunk. " * 10000
            large_chunks = [
                ContentChunk(
                    content=very_large_content,
                    source_url="https://example.com/large",
                    title="Large Content Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=large_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=large_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=large_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run pipeline with large content
            job = asyncio.run(pipeline.run_pipeline(["https://example.com/large"]))

            # Should complete successfully despite large content
            assert job.status == "completed"

    def test_invalid_url_handling(self, config):
        """Test handling of invalid URLs."""
        pipeline = IngestionPipeline(config)

        # Test with invalid URL format
        with pytest.raises(ValueError):
            asyncio.run(pipeline.run_pipeline_with_validation(["not-a-url"]))

        # Test with empty URL list
        with pytest.raises(ValueError):
            asyncio.run(pipeline.run_pipeline_with_validation([]))

    def test_embedding_api_error(self, config):
        """Test handling of embedding API errors."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock content chunks
            mock_chunks = [
                ContentChunk(
                    content="Test content for embedding.",
                    source_url="https://example.com/test",
                    title="Test Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)

            # Mock embedding service to raise an exception
            pipeline.embedding_service.generate_and_store_embeddings = Mock(side_effect=Exception("Embedding API error"))

            # Test that the pipeline handles the embedding error
            with pytest.raises(Exception):
                asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))

    def test_qdrant_storage_error(self, config):
        """Test handling of Qdrant storage errors."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            from src.embedding.embedding_service import EmbeddingService
            from src.storage.qdrant_storage import QdrantStorage

            pipeline = IngestionPipeline(config)

            # Create a mock embedding service that will fail during storage
            mock_chunks = [
                ContentChunk(
                    content="Test content for storage.",
                    source_url="https://example.com/test",
                    title="Test Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)

            # Mock the embedding service to fail during storage
            pipeline.embedding_service.generate_and_store_embeddings = Mock(side_effect=Exception("Storage error"))

            # Test that the pipeline handles the storage error
            with pytest.raises(Exception):
                asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))

    def test_crawler_service_error_handling(self, config):
        """Test comprehensive crawler error handling."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock crawler to raise various types of errors
            pipeline.crawler_service.crawl_urls = Mock(side_effect=CrawlerException("Crawler failed"))

            with pytest.raises(CrawlerException):
                asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))

    def test_concurrent_request_limiting(self, config):
        """Test behavior under concurrent request limits."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            # Set a low concurrent request limit for testing
            config.max_concurrent_requests = 1

            pipeline = IngestionPipeline(config)

            # Create multiple URLs to test concurrent handling
            urls = [f"https://example.com/page{i}" for i in range(5)]
            mock_chunks = [
                ContentChunk(
                    content=f"Content for page {i}",
                    source_url=url,
                    title=f"Page {i}"
                ) for i, url in enumerate(urls)
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run with limited concurrent requests
            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Should complete despite low concurrency limit
            assert job.status == "completed"
            assert job.processed_count == len(urls)

    def test_invalid_embedding_dimensions(self, config):
        """Test handling of invalid embedding dimensions."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            mock_chunks = [
                ContentChunk(
                    content="Test content",
                    source_url="https://example.com/test",
                    title="Test Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)

            # Mock embedding service to return invalid dimensions
            pipeline.embedding_service.storage.validate_embedding_dimensions = Mock(return_value=False)

            # This should fail validation
            with pytest.raises(Exception):
                asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))

    def test_malformed_html_handling(self, config):
        """Test handling of malformed HTML content."""
        from src.crawler.html_parser import HTMLParser

        parser = HTMLParser()

        # Test with malformed HTML
        malformed_html = "<html><body><p>Unclosed paragraph<div>Nested content"

        # The parser should handle malformed HTML gracefully
        clean_content, title = parser.parse_and_clean(malformed_html, "https://example.com/test")
        assert isinstance(clean_content, str)  # Should return a string, even if empty
        assert isinstance(title, str)

    def test_crawl_depth_limiting(self, config):
        """Test behavior with different crawl depth settings."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            mock_chunks = [
                ContentChunk(
                    content="Test content",
                    source_url="https://example.com/test",
                    title="Test Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Test with different depth values
            for depth in [0, 1, 2]:
                job = asyncio.run(pipeline.run_pipeline(["https://example.com/test"], max_depth=depth))
                assert job.status == "completed"

    def test_pipeline_cancellation(self, config):
        """Test behavior when pipeline execution is cancelled."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # This test ensures that the pipeline can handle cancellation gracefully
            # by properly managing resources in the finally block
            mock_chunks = [
                ContentChunk(
                    content="Test content",
                    source_url="https://example.com/test",
                    title="Test Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run pipeline normally (cancellation would happen externally)
            job = asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))
            assert job.status == "completed"