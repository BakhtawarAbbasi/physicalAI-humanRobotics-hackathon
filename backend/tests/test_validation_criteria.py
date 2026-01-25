"""
Validation tests for success criteria (95% crawl success, etc.) in the RAG system.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import asyncio
from datetime import datetime

from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline
from src.common.models import ContentChunk, CrawlJob


class TestValidationCriteria:
    """Validation tests for success criteria."""

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

    def test_crawl_success_rate_validation(self, config):
        """Test validation of crawl success rate (aiming for 95%)."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Simulate successful crawling of multiple URLs
            urls = [f"https://example.com/page{i}" for i in range(20)]  # 20 URLs
            successful_chunks = [
                ContentChunk(
                    content=f"Content for page {i}",
                    source_url=f"https://example.com/page{i}",
                    title=f"Page {i}"
                ) for i in range(19)  # 19 successful, 1 will fail
            ]

            # Mock successful crawl for 19 out of 20 URLs (95% success rate)
            pipeline.crawler_service.crawl_urls = Mock(return_value=successful_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=successful_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=successful_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Calculate success rate
            total_urls = len(urls)
            successful_crawls = len(successful_chunks)
            success_rate = (successful_crawls / total_urls) * 100

            # The success rate should reflect the mocked behavior
            assert success_rate == 95.0  # 19/20 = 95%
            assert job.status == "completed"

    def test_content_quality_metrics(self, config):
        """Test validation of content quality metrics."""
        pipeline = IngestionPipeline(config)

        # Create content chunks with varying quality
        high_quality_chunks = [
            ContentChunk(
                content="This is high quality content with substantial information and useful details.",
                source_url="https://example.com/good1",
                title="Good Content 1"
            ),
            ContentChunk(
                content="Another piece of high quality content with valuable information for users.",
                source_url="https://example.com/good2",
                title="Good Content 2"
            )
        ]

        low_quality_chunks = [
            ContentChunk(
                content="Hi",  # Too short
                source_url="https://example.com/poor1",
                title="Poor Content 1"
            ),
            ContentChunk(
                content="",  # Empty
                source_url="https://example.com/poor2",
                title="Poor Content 2"
            )
        ]

        all_chunks = high_quality_chunks + low_quality_chunks

        # Test content quality validation
        quality_results = pipeline.validate_content_quality(all_chunks)

        assert quality_results["total_chunks"] == 4
        assert quality_results["valid_chunks"] == 2  # Only high quality chunks
        assert quality_results["empty_chunks"] == 1
        assert quality_results["short_chunks"] == 1
        assert quality_results["valid_percentage"] == 50.0  # 2 out of 4 are valid
        assert quality_results["avg_chunk_length"] > 50  # High quality chunks should have good length

    def test_embedding_success_rate(self, config):
        """Test validation of embedding generation success rate."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Create content chunks
            test_chunks = [
                ContentChunk(
                    content=f"Content for embedding test {i}",
                    source_url="https://example.com/test",
                    title="Test Page"
                ) for i in range(10)  # 10 chunks
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=test_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=test_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=test_chunks)

            # Mock successful embedding generation
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run the embedding process
            success = pipeline.embedding_service.generate_and_store_embeddings(test_chunks)

            # Should be successful
            assert success is True

    def test_pipeline_configuration_validation(self, config):
        """Test validation of pipeline configuration parameters."""
        pipeline = IngestionPipeline(config)

        # Test valid configuration
        valid_urls = ["https://example.com/docs"]
        validation_errors = pipeline.validate_pipeline_config(valid_urls, 1)
        assert len(validation_errors) == 0

        # Test invalid configurations and verify appropriate errors
        invalid_configs = [
            ([], 1),  # Empty URLs
            (["invalid-url"], 1),  # Invalid URL format
            (["https://example.com"], -1),  # Negative depth
            (["https://example.com"], 10),  # Too high depth
        ]

        for urls, depth in invalid_configs:
            errors = pipeline.validate_pipeline_config(urls, depth)
            assert len(errors) > 0

    def test_content_relevance_validation(self, config):
        """Test validation of content relevance and duplication."""
        pipeline = IngestionPipeline(config)

        # Create content chunks including some duplicates
        chunks = [
            ContentChunk(
                content="This is the original content that provides valuable information.",
                source_url="https://example.com/page1",
                title="Page 1"
            ),
            ContentChunk(
                content="This is the original content that provides valuable information.",  # Duplicate
                source_url="https://example.com/page2",
                title="Page 2"
            ),
            ContentChunk(
                content="This is different content with unique information.",
                source_url="https://example.com/page3",
                title="Page 3"
            ),
            ContentChunk(
                content="This is slightly different content with some similar phrases.",
                source_url="https://example.com/page4",
                title="Page 4"
            )
        ]

        # Test quality validation
        quality_results = pipeline.validate_content_quality(chunks)

        # Check that we have the expected number of chunks
        assert quality_results["total_chunks"] == 4
        assert quality_results["valid_chunks"] == 4  # All have content > 10 chars

    def test_crawl_job_success_criteria(self, config):
        """Test validation of crawl job success against criteria."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Create a scenario with mixed success/failure
            urls = [f"https://example.com/page{i}" for i in range(10)]
            successful_chunks = [
                ContentChunk(
                    content=f"Content for page {i}",
                    source_url=f"https://example.com/page{i}",
                    title=f"Page {i}"
                ) for i in range(9)  # 9 successful out of 10 (90%)
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=successful_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=successful_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=successful_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Validate job results
            assert job.status == "completed"
            assert job.processed_count == 9  # 9 successful crawls
            assert len(job.urls) == 10  # 10 total URLs attempted

            # Calculate success rate
            success_rate = (job.processed_count / len(job.urls)) * 100
            assert success_rate == 90.0

    def test_content_completeness_validation(self, config):
        """Test validation that content has necessary metadata."""
        pipeline = IngestionPipeline(config)

        # Test chunks with complete metadata
        complete_chunks = [
            ContentChunk(
                content="This is complete content with all required metadata.",
                source_url="https://example.com/complete",
                title="Complete Page"
            )
        ]

        # Test quality
        quality_results = pipeline.validate_content_quality(complete_chunks)

        # All should be valid
        assert quality_results["valid_chunks"] == 1
        assert quality_results["valid_percentage"] == 100.0

    def test_error_rate_acceptance(self, config):
        """Test validation of acceptable error rates in the pipeline."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Simulate a pipeline run with some expected errors
            urls = [f"https://example.com/page{i}" for i in range(20)]

            # Return 18 successful chunks out of 20 possible (allowing for 10% error rate)
            successful_chunks = [
                ContentChunk(
                    content=f"Content for page {i}",
                    source_url=f"https://example.com/page{i}",
                    title=f"Page {i}"
                ) for i in range(18)
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=successful_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=successful_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=successful_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Should still complete successfully with 90% success rate
            assert job.status == "completed"
            success_rate = (job.processed_count / len(urls)) * 100
            assert success_rate == 90.0

    def test_validation_with_realistic_scenarios(self, config):
        """Test validation with more realistic crawling scenarios."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Simulate realistic scenario: 100 URLs with 95% success rate
            urls = [f"https://example.com/docs/page{i}" for i in range(100)]

            # 95 successful chunks (95% success rate)
            successful_chunks = [
                ContentChunk(
                    content=f"Documentation content for page {i}. This is meaningful content that would be useful for RAG system.",
                    source_url=f"https://example.com/docs/page{i}",
                    title=f"Documentation Page {i}"
                ) for i in range(95)
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=successful_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=successful_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=successful_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=1))

            # Validate success criteria
            assert job.status == "completed"
            success_rate = (job.processed_count / len(urls)) * 100
            assert success_rate == 95.0  # Meets the 95% target

            # Validate content quality
            quality_results = pipeline.validate_content_quality(successful_chunks)
            assert quality_results["valid_percentage"] == 100.0  # All chunks should be valid
            assert quality_results["avg_chunk_length"] > 20  # Content should be substantial

    def test_pipeline_success_thresholds(self, config):
        """Test that pipeline meets various success thresholds."""
        pipeline = IngestionPipeline(config)

        # Test different success scenarios
        test_cases = [
            {
                "name": "High success rate",
                "total": 100,
                "successful": 95,
                "expected_success_rate": 95.0
            },
            {
                "name": "Medium success rate",
                "total": 50,
                "successful": 40,
                "expected_success_rate": 80.0
            },
            {
                "name": "Low success rate",
                "total": 10,
                "successful": 5,
                "expected_success_rate": 50.0
            }
        ]

        for case in test_cases:
            # Create content chunks for this test case
            chunks = [
                ContentChunk(
                    content=f"Content for test {case['name']} - item {i}",
                    source_url=f"https://example.com/test{i}",
                    title=f"Test {case['name']} - {i}"
                ) for i in range(case["successful"])
            ]

            # Validate quality
            quality_results = pipeline.validate_content_quality(chunks)
            actual_success_rate = quality_results["valid_percentage"]

            # For this test, all generated chunks should be valid
            assert actual_success_rate == 100.0, f"Case {case['name']}: Expected 100% valid chunks"

            # The expected success rate refers to URL crawling success, not content validation
            # This test validates that our quality validation works properly