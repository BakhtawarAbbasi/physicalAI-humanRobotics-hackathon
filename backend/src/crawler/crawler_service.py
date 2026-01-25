"""
Crawler service for the RAG system.

This module orchestrates the crawling and parsing operations.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

from config.settings import ProcessingConfig
from src.common.exceptions import CrawlerException
from src.common.models import ContentChunk
from .html_parser import HTMLParser
from .js_html_parser import JSHTMLParser
from .url_fetcher import URLFetcher


class CrawlerService:
    """Coordinates crawling and parsing operations."""

    def __init__(self, config: ProcessingConfig):
        """
        Initialize the crawler service.

        Args:
            config: Processing configuration
        """
        self.config = config
        self.url_fetcher = URLFetcher(config)
        self.html_parser = HTMLParser()
        self.js_html_parser = JSHTMLParser(timeout=config.timeout * 1000)  # Convert to milliseconds
        self.logger = logging.getLogger(__name__)

    async def crawl_urls(self, urls: List[str], max_depth: int = 1) -> List[ContentChunk]:
        """
        Crawl a list of URLs and extract content chunks.

        Args:
            urls: List of URLs to crawl
            max_depth: Maximum depth to follow links (0 = no following)

        Returns:
            List of ContentChunk objects containing extracted content
        """
        all_chunks = []
        visited_urls = set()
        urls_to_crawl = urls.copy()

        for depth in range(max_depth + 1):
            self.logger.info(f"Crawling at depth {depth}, {len(urls_to_crawl)} URLs to process")

            # Fetch all URLs at current depth
            fetch_results = await self.url_fetcher.fetch_urls(urls_to_crawl)

            # Process fetched content
            next_urls_to_crawl = []
            for url, content in fetch_results:
                if content is None:
                    self.logger.warning(f"Failed to fetch content for {url}")
                    continue

                if url in visited_urls:
                    continue

                try:
                    # Parse and clean the HTML content using regular parser first
                    clean_content, title = self.html_parser.parse_and_clean(content, url)

                    # If regular parser didn't extract enough content, try JavaScript-enabled parser
                    if not clean_content.strip() or len(clean_content.strip()) < 50:
                        self.logger.info(f"Content too short ({len(clean_content)} chars) from regular parser for {url}, trying JavaScript-enabled parser")
                        try:
                            clean_content, title = await self.js_html_parser.parse_and_clean(url)
                        except Exception as js_error:
                            self.logger.warning(f"JavaScript parser also failed for {url}: {str(js_error)}")
                            if not clean_content.strip():
                                self.logger.warning(f"No content extracted from {url}")
                                continue

                    # Create content chunk
                    chunk = ContentChunk(
                        content=clean_content,
                        source_url=url,
                        title=title,
                        section="",  # Will be populated during chunking
                        chunk_index=0
                    )

                    all_chunks.append(chunk)
                    visited_urls.add(url)

                    # Extract links if we're not at max depth
                    if depth < max_depth:
                        new_urls = self.url_fetcher.extract_links(content, url)
                        for new_url in new_urls:
                            if self._is_valid_url_for_crawling(new_url, url) and new_url not in visited_urls:
                                next_urls_to_crawl.append(new_url)

                except Exception as e:
                    self.logger.error(f"Error processing {url}: {str(e)}")
                    continue

            # Update URLs for next depth
            urls_to_crawl = list(set(next_urls_to_crawl))  # Remove duplicates

        self.logger.info(f"Crawling completed. Extracted content from {len(all_chunks)} pages")
        return all_chunks

    def _is_valid_url_for_crawling(self, url: str, base_url: str) -> bool:
        """
        Check if a URL is valid for crawling based on criteria.

        Args:
            url: URL to validate
            base_url: Base URL for comparison

        Returns:
            True if URL is valid for crawling, False otherwise
        """
        try:
            parsed_url = urlparse(url)
            parsed_base = urlparse(base_url)

            # Must be same domain
            if parsed_url.netloc != parsed_base.netloc:
                return False

            # Must be HTTP or HTTPS
            if parsed_url.scheme not in ['http', 'https']:
                return False

            # Skip certain file types
            skip_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.exe', '.dmg']
            if any(url.lower().endswith(ext) for ext in skip_extensions):
                return False

            # Skip anchor links
            if parsed_url.fragment:
                return False

            return True

        except Exception:
            return False

    async def crawl_single_url(self, url: str) -> List[ContentChunk]:
        """
        Crawl a single URL and extract content chunks.

        Args:
            url: URL to crawl

        Returns:
            List of ContentChunk objects containing extracted content
        """
        try:
            content = await self.url_fetcher.fetch_url(url)
            if content is None:
                raise CrawlerException(f"Failed to fetch content from {url}")

            clean_content, title = self.html_parser.parse_and_clean(content, url)

            # If regular parser didn't extract enough content, try JavaScript-enabled parser
            if not clean_content.strip() or len(clean_content.strip()) < 50:
                self.logger.info(f"Content too short ({len(clean_content)} chars) from regular parser for {url}, trying JavaScript-enabled parser")
                try:
                    clean_content, title = await self.js_html_parser.parse_and_clean(url)
                except Exception as js_error:
                    self.logger.warning(f"JavaScript parser also failed for {url}: {str(js_error)}")
                    if not clean_content.strip():
                        raise CrawlerException(f"No content extracted from {url}")

            chunk = ContentChunk(
                content=clean_content,
                source_url=url,
                title=title,
                section="",
                chunk_index=0
            )

            return [chunk]

        except Exception as e:
            self.logger.error(f"Error crawling single URL {url}: {str(e)}")
            raise CrawlerException(f"Failed to crawl {url}: {str(e)}")