"""
URL fetching module for the RAG system.

This module handles fetching URLs with rate limiting and error handling.
"""

import asyncio
import logging
import time
from typing import List, Optional
from urllib.parse import urljoin, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import ProcessingConfig
from src.common.exceptions import NetworkException, RateLimitException


class URLFetcher:
    """Handles URL fetching with rate limiting and error handling."""

    def __init__(self, config: ProcessingConfig):
        """
        Initialize the URL fetcher with configuration.

        Args:
            config: Processing configuration with crawling parameters
        """
        self.config = config
        self.session = self._create_session()
        self.logger = logging.getLogger(__name__)
        self.last_request_time = 0

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()

        # Define retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        # Create adapter with retry strategy
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            'User-Agent': 'RAG-Ingestion-Bot/1.0 (compatible; +https://example.com/bot)'
        })

        return session

    async def fetch_url(self, url: str) -> Optional[str]:
        """
        Fetch a single URL with rate limiting and error handling.

        Args:
            url: URL to fetch

        Returns:
            Content of the URL as string, or None if failed
        """
        try:
            # Rate limiting: ensure minimum delay between requests
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            min_delay = self.config.request_delay

            if time_since_last_request < min_delay:
                await asyncio.sleep(min_delay - time_since_last_request)

            self.logger.info(f"Fetching URL: {url}")

            response = self.session.get(
                url,
                timeout=self.config.timeout,
                allow_redirects=True
            )

            # Check for rate limiting
            if response.status_code == 429:
                self.logger.warning(f"Rate limited for URL: {url}")
                raise RateLimitException(f"Rate limited when fetching {url}")

            response.raise_for_status()

            self.last_request_time = time.time()
            return response.text

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching URL {url}: {str(e)}")
            raise NetworkException(f"Failed to fetch {url}: {str(e)}")

    async def fetch_urls(self, urls: List[str]) -> List[tuple[str, Optional[str]]]:
        """
        Fetch multiple URLs concurrently with rate limiting.

        Args:
            urls: List of URLs to fetch

        Returns:
            List of tuples (url, content) for successfully fetched URLs
        """
        results = []
        semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)

        async def fetch_with_semaphore(url):
            async with semaphore:
                try:
                    content = await self.fetch_url(url)
                    return url, content
                except Exception as e:
                    self.logger.error(f"Failed to fetch {url}: {str(e)}")
                    return url, None

        tasks = [fetch_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out any exceptions that might have occurred
        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Exception during fetch: {result}")
            else:
                valid_results.append(result)

        return valid_results

    def extract_links(self, html_content: str, base_url: str) -> List[str]:
        """
        Extract links from HTML content.

        Args:
            html_content: HTML content to parse
            base_url: Base URL to resolve relative links

        Returns:
            List of absolute URLs extracted from the content
        """
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        base_domain = urlparse(base_url).netloc

        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)

            # Only include links from the same domain
            if urlparse(absolute_url).netloc == base_domain:
                links.append(absolute_url)

        return links