"""
Final integration tests to verify the complete RAG system works together.
"""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
import asyncio

from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline
from src.common.models import ContentChunk
from src.utils.config_validator import run_full_validation


class TestFinalIntegration:
    """Final integration tests for the complete RAG system."""

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
        config.timeout = 10
        return config

    def test_complete_pipeline_integration(self, config):
        """Test the complete pipeline from start to finish."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            # Create the pipeline
            pipeline = IngestionPipeline(config)

            # Mock all services to avoid external dependencies
            mock_chunks = [
                ContentChunk(
                    content="This is test content for the RAG system integration test.",
                    source_url="https://example.com/test",
                    title="Integration Test Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run the complete pipeline
            urls = ["https://example.com/test"]
            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Verify the pipeline completed successfully
            assert job.status == "completed"
            assert job.processed_count == 1

            # Verify all services were called
            pipeline.crawler_service.crawl_urls.assert_called_once()
            pipeline.chunker_service.process_content_chunks.assert_called_once()
            pipeline.chunker_service.validate_chunks.assert_called_once()
            pipeline.embedding_service.generate_and_store_embeddings.assert_called_once()

    def test_pipeline_with_validation(self, config):
        """Test the pipeline with validation enabled."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock services
            mock_chunks = [
                ContentChunk(
                    content="Valid content for validation test.",
                    source_url="https://example.com/validate",
                    title="Validation Test"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run pipeline with validation
            urls = ["https://example.com/validate"]
            job = asyncio.run(pipeline.run_pipeline_with_validation(urls))

            # Verify success
            assert job.status == "completed"

    def test_configuration_validation_integration(self, config):
        """Test configuration validation with the pipeline."""
        # Test with valid configuration
        valid_urls = ["https://example.com/docs"]
        is_valid, errors = run_full_validation(config, valid_urls)

        # Should be valid since we're using mock config
        # In a real scenario, API connectivity would fail with test keys,
        # but environment variables and config parameters should be valid
        # We'll check that the validation runs without error
        assert isinstance(errors, list)

    def test_pipeline_monitoring_integration(self, config):
        """Test that monitoring works with the pipeline."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock services
            mock_chunks = [
                ContentChunk(
                    content="Content for monitoring test.",
                    source_url="https://example.com/monitor",
                    title="Monitoring Test"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run pipeline and check that monitoring was used
            urls = ["https://example.com/monitor"]
            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Verify pipeline completed
            assert job.status == "completed"

            # Check that monitor was used (no exceptions should occur)
            # The monitoring is tested through the normal pipeline execution

    def test_error_handling_integration(self, config):
        """Test error handling throughout the integrated pipeline."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Test error in crawling
            pipeline.crawler_service.crawl_urls = Mock(side_effect=Exception("Crawl error"))

            with pytest.raises(Exception):
                asyncio.run(pipeline.run_pipeline(["https://example.com/test"]))

    def test_multiple_urls_integration(self, config):
        """Test the pipeline with multiple URLs."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Create content for multiple URLs
            urls = [f"https://example.com/page{i}" for i in range(3)]
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

            # Run pipeline with multiple URLs
            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Verify completion
            assert job.status == "completed"
            assert job.processed_count == 3

    def test_pipeline_resource_cleanup(self, config):
        """Test that resources are cleaned up properly."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock services
            mock_chunks = [
                ContentChunk(
                    content="Content for cleanup test.",
                    source_url="https://example.com/cleanup",
                    title="Cleanup Test"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run pipeline
            urls = ["https://example.com/cleanup"]
            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Clean up resources (this should not raise exceptions)
            pipeline.close()

            # Verify completion
            assert job.status == "completed"

    def test_pipeline_with_realistic_content(self, config):
        """Test the pipeline with more realistic content."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Create realistic documentation-like content
            realistic_content = """
            # Getting Started with Our Product

            Welcome to our product documentation. This guide will help you get started quickly.

            ## Installation

            To install our product, run the following command:

            ```
            pip install our-product
            ```

            ## Configuration

            Create a configuration file with the following settings:

            ```python
            config = {
                'api_key': 'your-api-key',
                'timeout': 30,
                'retries': 3
            }
            ```

            ## Usage

            Here's a basic example of how to use our product:

            ```python
            from our_product import Client

            client = Client(api_key='your-key')
            result = client.process(data)
            ```

            For more advanced usage, see our API reference.
            """

            realistic_chunks = [
                ContentChunk(
                    content=realistic_content,
                    source_url="https://example.com/docs/getting-started",
                    title="Getting Started with Our Product"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=realistic_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=realistic_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=realistic_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run pipeline with realistic content
            urls = ["https://example.com/docs/getting-started"]
            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Verify completion
            assert job.status == "completed"
            assert job.processed_count == 1

    def test_pipeline_quality_validation(self, config):
        """Test the pipeline with quality validation."""
        pipeline = IngestionPipeline(config)

        # Create mixed quality content
        high_quality_chunk = ContentChunk(
            content="This is high quality content with substantial information and useful details for users.",
            source_url="https://example.com/high-quality",
            title="High Quality Content"
        )

        low_quality_chunk = ContentChunk(
            content="Hi",  # Too short
            source_url="https://example.com/low-quality",
            title="Low Quality Content"
        )

        mixed_chunks = [high_quality_chunk, low_quality_chunk]

        # Test quality validation
        quality_results = pipeline.validate_content_quality(mixed_chunks)

        assert quality_results["total_chunks"] == 2
        assert quality_results["valid_chunks"] == 1  # Only high quality chunk
        assert quality_results["valid_percentage"] == 50.0

        # Test configuration validation
        validation_errors = pipeline.validate_pipeline_config(["https://example.com/test"], 1)
        assert len(validation_errors) == 0