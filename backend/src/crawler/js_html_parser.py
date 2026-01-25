"""
JavaScript-enabled HTML parsing module for the RAG system.

This module handles parsing HTML content from JavaScript-heavy pages using Playwright.
"""

import asyncio
import logging
from typing import List, Tuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Comment
from playwright.async_api import async_playwright

from src.common.exceptions import ParserException


class JSHTMLParser:
    """Handles HTML parsing for JavaScript-heavy pages using Playwright."""

    def __init__(self, timeout: int = 30000):
        """
        Initialize the JavaScript-enabled HTML parser.

        Args:
            timeout: Timeout for page loading in milliseconds
        """
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    async def parse_and_clean(self, url: str) -> Tuple[str, str]:
        """
        Parse HTML content from a URL using a headless browser to handle JavaScript.

        Args:
            url: URL to fetch and parse

        Returns:
            Tuple of (clean_text_content, page_title)
        """
        async with async_playwright() as p:
            try:
                # Launch browser (use chromium)
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Set timeout
                page.set_default_timeout(self.timeout)

                # Navigate to the page
                await page.goto(url, wait_until="networkidle")

                # Wait for Docusaurus-specific content to load
                # Look for the main content area that contains the documentation
                try:
                    # Wait for the main content area to be present in the DOM
                    await page.wait_for_selector('.theme-doc-markdown', timeout=10000)
                except:
                    # If the specific selector isn't found, wait a bit more for general content
                    await page.wait_for_timeout(5000)

                # Additional wait to ensure content is fully rendered
                await page.wait_for_timeout(2000)

                # Get the fully rendered HTML
                html_content = await page.content()

                # Close browser
                await browser.close()

                # Now parse the rendered HTML with BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Remove comments
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                for comment in comments:
                    comment.extract()

                # Try to find the main content area in Docusaurus sites
                # Docusaurus typically uses specific classes for main content
                main_content = None

                # Look for common Docusaurus content containers
                selectors = [
                    'main',  # Standard main element
                    '.main-wrapper',  # Docusaurus main wrapper
                    '.container.padding-vert--lg',  # Docusaurus container
                    '.container',  # General container
                    '.markdown',  # Docusaurus markdown content
                    '.theme-doc-markdown',  # Docusaurus theme markdown
                    '.article',  # General article container
                    'article',  # Standard article element
                ]

                for selector in selectors:
                    if selector.startswith('.'):
                        elements = soup.select(selector)
                        if elements:
                            main_content = elements[0]
                            break
                    else:
                        element = soup.select_one(selector)
                        if element:
                            main_content = element
                            break

                # If no specific main content found, use body
                if not main_content:
                    main_content = soup.find('body')

                # If still no content found, use the whole document
                if not main_content:
                    main_content = soup

                # Remove navigation, headers, footers, and other non-content elements
                non_content_selectors = [
                    'nav',  # Navigation
                    '.navbar',  # Docusaurus navbar
                    '.nav',  # Navigation
                    '.footer',  # Footer
                    '.sidebar',  # Sidebar
                    '.menu',  # Menu
                    '.pagination-nav',  # Pagination
                    '.theme-edit-this-page',  # Edit this page link
                    '.theme-last-updated',  # Last updated info
                    '.theme-admonition',  # Admonition blocks (may want to keep some)
                    '.button',  # Buttons
                    'header',  # Header
                    '.header',  # Header
                    '.search-bar',  # Search bar
                    '.toc',  # Table of contents
                    '.table-of-contents',  # Table of contents
                ]

                for selector in non_content_selectors:
                    elements = main_content.select(selector) if hasattr(main_content, 'select') else []
                    for element in elements:
                        element.decompose()

                # Get the title
                title_tag = soup.find('title')
                title = title_tag.get_text().strip() if title_tag else urlparse(url).path.split('/')[-1] or 'Untitled'

                # Extract clean text content
                clean_text = main_content.get_text(separator=' ', strip=True)

                # Clean up extra whitespace
                clean_text = ' '.join(clean_text.split())

                # For documentation content, be more selective about what to filter
                # Split by newlines and filter carefully
                lines = clean_text.split('\n')
                clean_lines = []
                for line in lines:
                    line = line.strip()
                    if line:
                        # Only filter very obvious navigation elements, preserve content
                        if not self._is_obvious_navigation_text(line):
                            clean_lines.append(line)

                final_text = ' '.join(clean_lines)

                self.logger.info(f"Extracted {len(final_text)} characters from {url} using JavaScript rendering")
                return final_text, title

            except Exception as e:
                self.logger.error(f"Error parsing JavaScript-heavy page for {url}: {str(e)}")
                raise ParserException(f"Failed to parse JavaScript-heavy page for {url}: {str(e)}")

    def _is_navigation_text(self, text: str) -> bool:
        """
        Check if text is likely to be navigation text that should be removed.
        This is the original method kept for compatibility.

        Args:
            text: Text to check

        Returns:
            True if text is likely navigation text, False otherwise
        """
        # Common navigation-related words and patterns
        nav_indicators = [
            'home', 'about', 'contact', 'blog', 'docs', 'documentation',
            'menu', 'navigation', 'previous', 'next', 'table of contents',
            'tableofcontents', 'toc', 'sitemap', 'privacy', 'terms',
            'login', 'sign in', 'register', 'signup', 'search',
            'all categories', 'categories', 'tags', 'archive'
        ]

        text_lower = text.lower()
        for indicator in nav_indicators:
            if indicator in text_lower:
                return True

        # Check if text is short and looks like a menu item
        if len(text) < 50 and ('>' in text or '→' in text or text.count(' ') < 3):
            return True

        return False

    def _is_obvious_navigation_text(self, text: str) -> bool:
        """
        Check if text is obviously navigation text that should be removed.
        This is a more conservative version for documentation content.

        Args:
            text: Text to check

        Returns:
            True if text is obviously navigation text, False otherwise
        """
        # Only filter very obvious navigation elements
        nav_indicators = [
            'home', 'menu', 'navigation', 'table of contents', 'toc',
            'sitemap', 'login', 'sign in', 'register', 'search'
        ]

        text_lower = text.lower()
        for indicator in nav_indicators:
            # Only match if the entire line is just this navigation text
            if text_lower.strip() == indicator:
                return True
            # Also check for common menu-like patterns
            if text_lower.strip().startswith(indicator + ' ') and len(text) < 20:
                return True

        return False

    async def extract_headings(self, url: str) -> List[Tuple[str, str]]:
        """
        Extract headings from a JavaScript-heavy page.

        Args:
            url: URL to fetch and extract headings from

        Returns:
            List of tuples (heading_text, heading_level)
        """
        async with async_playwright() as p:
            try:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Set timeout
                page.set_default_timeout(self.timeout)

                # Navigate to the page
                await page.goto(url, wait_until="networkidle")

                # Wait for Docusaurus-specific content to load
                # Look for the main content area that contains the documentation
                try:
                    # Wait for the main content area to be present in the DOM
                    await page.wait_for_selector('.theme-doc-markdown', timeout=10000)
                except:
                    # If the specific selector isn't found, wait a bit more for general content
                    await page.wait_for_timeout(5000)

                # Additional wait to ensure content is fully rendered
                await page.wait_for_timeout(2000)

                # Get the fully rendered HTML
                html_content = await page.content()

                # Close browser
                await browser.close()

                soup = BeautifulSoup(html_content, 'html.parser')
                headings = []

                for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                    heading_text = heading.get_text().strip()
                    heading_level = heading.name
                    if heading_text:
                        headings.append((heading_text, heading_level))

                return headings

            except Exception as e:
                self.logger.error(f"Error extracting headings from {url}: {str(e)}")
                raise ParserException(f"Failed to extract headings from {url}: {str(e)}")