"""
End-to-end tests for the RAG system with sample Docusaurus sites.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import asyncio

from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline
from src.common.models import ContentChunk


class TestE2EDocusaurus:
    """End-to-end tests for Docusaurus site integration."""

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

    def test_docusaurus_content_extraction(self, config):
        """Test extraction of content from a mock Docusaurus site."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            # Create pipeline
            pipeline = IngestionPipeline(config)

            # Mock HTML content that resembles a Docusaurus page
            mock_html_content = """
            <!DOCTYPE html>
            <html>
            <head><title>Test Docusaurus Page</title></head>
            <body>
                <nav class="navbar">Navigation content</nav>
                <div class="main-wrapper">
                    <header>
                        <h1>Test Docusaurus Documentation</h1>
                    </header>
                    <main class="container padding-vert--lg">
                        <article class="markdown">
                            <h2>Getting Started</h2>
                            <p>This is the main content of the Docusaurus page.</p>
                            <p>It contains important documentation that should be extracted.</p>
                            <h3>Installation</h3>
                            <p>To install, run the following command:</p>
                            <code>npm install</code>
                            <h3>Configuration</h3>
                            <p>Configure your settings in the config file.</p>
                        </article>
                    </main>
                </div>
                <footer class="footer">Footer content</footer>
            </body>
            </html>
            """

            # Mock the crawler service to return content similar to what would be extracted from a Docusaurus site
            mock_chunks = [
                ContentChunk(
                    content="Test Docusaurus Documentation Getting Started This is the main content of the Docusaurus page. It contains important documentation that should be extracted. Installation To install, run the following command: npm install Configuration Configure your settings in the config file.",
                    source_url="https://example.com/docs/getting-started",
                    title="Test Docusaurus Page"
                )
            ]

            # Mock services to simulate the full pipeline
            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.crawler_service.url_fetcher.fetch_urls = Mock(return_value=[("https://example.com/docs/getting-started", mock_html_content)])
            pipeline.crawler_service.html_parser.parse_and_clean = Mock(return_value=("Test Docusaurus Documentation Getting Started This is the main content of the Docusaurus page. It contains important documentation that should be extracted. Installation To install, run the following command: npm install Configuration Configure your settings in the config file.", "Test Docusaurus Page"))

            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)

            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run the pipeline
            urls = ["https://example.com/docs/getting-started"]
            job = asyncio.run(pipeline.run_pipeline(urls))

            # Verify the job completed successfully
            assert job.status == "completed"
            assert job.processed_count == 1

            # Verify the content extraction worked as expected
            pipeline.crawler_service.crawl_urls.assert_called_once()
            pipeline.chunker_service.process_content_chunks.assert_called_once()
            pipeline.embedding_service.generate_and_store_embeddings.assert_called_once()

    def test_docusaurus_multi_page_crawl(self, config):
        """Test crawling multiple Docusaurus pages."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Mock multiple Docusaurus pages
            mock_pages = [
                ContentChunk(
                    content="Getting started guide for the product. Learn the basics here.",
                    source_url="https://example.com/docs/getting-started",
                    title="Getting Started"
                ),
                ContentChunk(
                    content="Advanced configuration options and settings.",
                    source_url="https://example.com/docs/configuration",
                    title="Configuration"
                ),
                ContentChunk(
                    content="API reference with detailed function descriptions.",
                    source_url="https://example.com/docs/api-reference",
                    title="API Reference"
                )
            ]

            # Mock services
            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_pages)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_pages)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_pages)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Run the pipeline with multiple URLs
            urls = [
                "https://example.com/docs/getting-started",
                "https://example.com/docs/configuration",
                "https://example.com/docs/api-reference"
            ]
            job = asyncio.run(pipeline.run_pipeline(urls, max_depth=0))

            # Verify the job completed successfully
            assert job.status == "completed"
            assert job.processed_count == 3

    def test_docusaurus_content_chunking(self, config):
        """Test that Docusaurus content is properly chunked preserving context."""
        from src.chunker.chunker_service import ChunkerService

        chunker_service = ChunkerService(config)

        # Create a longer Docusaurus-style content that would need chunking
        long_content = """
        Introduction to Docusaurus

        Docusaurus is a modern static website generator focused on documentation sites. It provides a great developer experience and is optimized for performance.

        Installation

        To install Docusaurus, you need to have Node.js installed on your system. Then run the following command:

        npx create-docusaurus@latest my-website classic

        This will create a new Docusaurus website in the my-website directory with the classic template.

        Configuration

        The main configuration file is docusaurus.config.js. This file contains all the configuration options for your site including site metadata, plugins, themes, and more.

        You can configure the site's title, tagline, organization name, project name, and URL. The trailing slash configuration determines whether URLs should end with a slash or not.

        Navigation

        Docusaurus provides several ways to organize your documentation. You can use the sidebar to organize your documentation into categories and subcategories.

        The sidebar can be auto-generated from your file structure or manually configured. You can also add custom links and categories to the sidebar.

        Deployment

        Docusaurus sites can be deployed to various platforms including GitHub Pages, GitLab Pages, Netlify, Vercel, and more.

        The deployment process is straightforward and Docusaurus provides built-in support for popular deployment platforms.
        """

        # Create content chunk
        test_chunk = ContentChunk(
            content=long_content,
            source_url="https://example.com/docs/intro",
            title="Introduction to Docusaurus"
        )

        # Process the chunk
        processed_chunks = chunker_service.process_content_chunks([test_chunk])

        # Verify chunking worked
        assert len(processed_chunks) > 0
        assert all(len(chunk.content) <= config.chunk_size for chunk in processed_chunks)

        # Verify that each chunk preserves the source information
        for chunk in processed_chunks:
            assert chunk.source_url == "https://example.com/docs/intro"
            assert chunk.title == "Introduction to Docusaurus"

        # Verify that the content was split meaningfully
        total_content_length = sum(len(chunk.content) for chunk in processed_chunks)
        original_length = len(long_content.strip())

        # Account for potential whitespace normalization
        assert abs(total_content_length - original_length) < 100

    def test_docusaurus_link_extraction(self, config):
        """Test extraction of links from Docusaurus pages."""
        from src.crawler.url_fetcher import URLFetcher

        url_fetcher = URLFetcher(config)

        # Mock Docusaurus HTML with internal links
        html_content = """
        <html>
        <body>
            <nav>
                <a href="/docs/getting-started">Getting Started</a>
                <a href="/docs/installation">Installation</a>
                <a href="/docs/configuration">Configuration</a>
                <a href="https://external-site.com">External Link</a>
            </nav>
            <main>
                <p>Check out our <a href="/docs/advanced">advanced guide</a>.</p>
                <p>Also see <a href="../tutorials">tutorials</a>.</p>
            </main>
        </body>
        </html>
        """

        # Extract links (should only get internal ones)
        base_url = "https://example.com/docs"
        extracted_links = url_fetcher.extract_links(html_content, base_url)

        # Verify that internal links were extracted but external ones were not
        expected_internal_links = [
            "https://example.com/docs/getting-started",
            "https://example.com/docs/installation",
            "https://example.com/docs/configuration",
            "https://example.com/docs/advanced"
        ]

        # Check that internal links are present
        for expected_link in expected_internal_links:
            assert expected_link in extracted_links

        # Check that external link is not present
        external_link = "https://external-site.com"
        assert external_link not in extracted_links

    def test_docusaurus_pipeline_validation(self, config):
        """Test the complete pipeline with Docusaurus-style validation."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Create mock Docusaurus content
            mock_chunks = [
                ContentChunk(
                    content="Docusaurus is a modern static website generator focused on documentation sites.",
                    source_url="https://example.com/docs/intro",
                    title="Introduction to Docusaurus"
                )
            ]

            # Mock the full pipeline flow
            pipeline.crawler_service.crawl_urls = Mock(return_value=mock_chunks)
            pipeline.chunker_service.process_content_chunks = Mock(return_value=mock_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=mock_chunks)
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            # Test with validation
            urls = ["https://example.com/docs/intro"]
            job = asyncio.run(pipeline.run_pipeline_with_validation(urls))

            # Verify success
            assert job.status == "completed"

            # Test content quality validation
            quality_results = pipeline.validate_content_quality(mock_chunks)
            assert quality_results["total_chunks"] == 1
            assert quality_results["valid_chunks"] == 1
            assert quality_results["valid_percentage"] == 100.0

    def test_docusaurus_error_handling(self, config):
        """Test error handling with Docusaurus content."""
        with patch('src.crawler.crawler_service.URLFetcher'), \
             patch('src.crawler.crawler_service.HTMLParser'), \
             patch('src.chunker.chunker_service.TextChunker'), \
             patch('src.embedding.embedding_service.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):

            pipeline = IngestionPipeline(config)

            # Test with empty content (should be handled gracefully)
            empty_chunks = [
                ContentChunk(
                    content="",
                    source_url="https://example.com/docs/empty",
                    title="Empty Page"
                )
            ]

            pipeline.crawler_service.crawl_urls = Mock(return_value=empty_chunks)
            pipeline.chunker_service.validate_chunks = Mock(return_value=[])  # Empty after validation
            pipeline.embedding_service.generate_and_store_embeddings = Mock(return_value=True)

            urls = ["https://example.com/docs/empty"]
            job = asyncio.run(pipeline.run_pipeline(urls))

            # Should still complete but with no processed content
            assert job.status == "completed"
            # The chunker should filter out empty chunks