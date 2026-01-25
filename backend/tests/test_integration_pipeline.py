"""
Integration tests for the complete ingestion pipeline.
"""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline
from src.common.models import ContentChunk


class TestIngestionPipelineIntegration:
    """Integration tests for the complete ingestion pipeline."""

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
        config.request_delay = 1.0
        config.timeout = 30
        return config

    @pytest.fixture
    def sample_urls(self):
        """Sample URLs for testing."""
        return ["https://example.com/test"]

    @pytest.fixture
    def pipeline_with_mocks(self, config):
        """Create a pipeline instance with mocked external services."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.CohereEmbedder'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            # Create the pipeline
            pipeline = IngestionPipeline(config)

            # Mock the services to avoid external API calls
            pipeline.crawler_service.url_fetcher = Mock()
            pipeline.crawler_service.html_parser = Mock()
            pipeline.chunker_service.text_chunker = Mock()
            pipeline.embedding_service.embedder = Mock()
            pipeline.embedding_service.storage = Mock()

            return pipeline

    def test_pipeline_end_to_end_success(self, pipeline_with_mocks, sample_urls):
        """Test the complete pipeline from start to finish with success."""
        # Mock the crawler service to return content chunks
        mock_chunks = [
            ContentChunk(
                content="This is test content for integration testing.",
                source_url="https://example.com/test",
                title="Test Page"
            )
        ]
        pipeline_with_mocks.crawler_service.crawl_urls = Mock(return_value=mock_chunks)

        # Mock the chunker service
        pipeline_with_mocks.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
        pipeline_with_mocks.chunker_service.validate_chunks = Mock(return_value=mock_chunks)

        # Mock the embedding service
        pipeline_with_mocks.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

        # Run the pipeline
        import asyncio
        job = asyncio.run(pipeline_with_mocks.run_pipeline(sample_urls))

        # Verify the job completed successfully
        assert job.status == "completed"
        assert job.processed_count == len(mock_chunks)

    def test_pipeline_with_validation_success(self, pipeline_with_mocks, sample_urls):
        """Test the pipeline with validation enabled."""
        # Mock the services
        mock_chunks = [
            ContentChunk(
                content="This is test content for validation testing.",
                source_url="https://example.com/test",
                title="Test Page"
            )
        ]
        pipeline_with_mocks.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
        pipeline_with_mocks.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
        pipeline_with_mocks.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
        pipeline_with_mocks.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

        # Run the pipeline with validation
        import asyncio
        job = asyncio.run(pipeline_with_mocks.run_pipeline_with_validation(sample_urls))

        # Verify the job completed successfully
        assert job.status == "completed"

    def test_pipeline_validation_fails_with_invalid_urls(self, pipeline_with_mocks):
        """Test that validation catches invalid URLs."""
        # Test with empty URLs
        with pytest.raises(ValueError):
            import asyncio
            asyncio.run(pipeline_with_mocks.run_pipeline_with_validation([]))

        # Test with invalid URL format
        with pytest.raises(ValueError):
            import asyncio
            asyncio.run(pipeline_with_mocks.run_pipeline_with_validation(["invalid-url"]))

    def test_pipeline_configuration_validation(self, pipeline_with_mocks, sample_urls):
        """Test configuration validation methods."""
        # Test valid configuration
        errors = pipeline_with_mocks.validate_pipeline_config(sample_urls, 1)
        assert len(errors) == 0

        # Test invalid max_depth
        errors = pipeline_with_mocks.validate_pipeline_config(sample_urls, -1)
        assert len(errors) > 0
        assert any("max_depth must be non-negative" in error for error in errors)

        # Test too high max_depth
        errors = pipeline_with_mocks.validate_pipeline_config(sample_urls, 10)
        assert len(errors) > 0
        assert any("max_depth should be 5 or less" in error for error in errors)

    def test_content_quality_validation(self, pipeline_with_mocks):
        """Test content quality validation methods."""
        # Create test content chunks
        test_chunks = [
            ContentChunk(content="Valid content chunk.", source_url="https://example.com/1", title="Page 1"),
            ContentChunk(content="", source_url="https://example.com/2", title="Page 2"),  # Empty
            ContentChunk(content="Hi", source_url="https://example.com/3", title="Page 3"),  # Too short
            ContentChunk(content="Another valid chunk with sufficient content.", source_url="https://example.com/4", title="Page 4")
        ]

        # Run validation
        results = pipeline_with_mocks.validate_content_quality(test_chunks)

        # Verify results
        assert results["total_chunks"] == 4
        assert results["valid_chunks"] == 2
        assert results["empty_chunks"] == 1
        assert results["short_chunks"] == 1
        assert results["valid_percentage"] == 50.0

    def test_pipeline_error_handling(self, pipeline_with_mocks, sample_urls):
        """Test error handling in the pipeline."""
        # Mock the crawler to raise an exception
        pipeline_with_mocks.crawler_service.crawl_urls = Mock(side_effect=Exception("Network error"))

        # Run the pipeline and expect it to handle the error
        import asyncio
        with pytest.raises(Exception):
            job = asyncio.run(pipeline_with_mocks.run_pipeline(sample_urls))
            # The job should be marked as failed
            assert job.status == "failed"

    def test_job_management(self, pipeline_with_mocks, sample_urls):
        """Test job management functionality."""
        # Mock successful pipeline run
        mock_chunks = [
            ContentChunk(content="Test content.", source_url="https://example.com/test", title="Test Page")
        ]
        pipeline_with_mocks.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
        pipeline_with_mocks.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
        pipeline_with_mocks.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
        pipeline_with_mocks.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

        # Run pipeline
        import asyncio
        job = asyncio.run(pipeline_with_mocks.run_pipeline(sample_urls))

        # Get job status
        status_info = pipeline_with_mocks.get_job_status(job.id)

        # Verify status information
        assert status_info is not None
        assert status_info["job_id"] == job.id
        assert status_info["status"] == "completed"
        assert status_info["urls"] == sample_urls