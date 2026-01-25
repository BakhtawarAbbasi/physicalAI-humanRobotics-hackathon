#!/usr/bin/env python3
"""
Debug script to check what's happening in the JSHTMLParser.
"""

import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.async_api import async_playwright


async def debug_js_parser():
    """Debug what's happening in the JS parser."""
    timeout = 30000

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the page
        url = "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-02/chapter-1-gazebo-physics"
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

        # Now parse the rendered HTML with BeautifulSoup (same as in our parser)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Remove comments
        from bs4 import Comment
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        # Try to find the main content area in Docusaurus sites
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
                    print(f"Found content in selector: {selector}")
                    break
            else:
                element = soup.select_one(selector)
                if element:
                    main_content = element
                    print(f"Found content in selector: {selector}")
                    break

        if not main_content:
            main_content = soup.find('body')
            print("Using body as main content")

        if not main_content:
            main_content = soup
            print("Using entire document as main content")

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
        print(f"Title: {title}")

        # Extract clean text content
        clean_text = main_content.get_text(separator=' ', strip=True)

        # Clean up extra whitespace
        clean_text = ' '.join(clean_text.split())

        print(f"Text after cleaning: {len(clean_text)} characters")
        safe_preview = clean_text[:100].encode('utf-8', errors='ignore').decode('utf-8')
        print(f"Text preview: {safe_preview}...")

        # Remove common navigation elements that might have slipped through
        lines = clean_text.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            if line and not _is_navigation_text(line):
                clean_lines.append(line)

        final_text = ' '.join(clean_lines)

        print(f"Final text: {len(final_text)} characters")
        safe_final_preview = final_text[:100].encode('utf-8', errors='ignore').decode('utf-8') if final_text else "No final text"
        print(f"Final text preview: {safe_final_preview}..." if final_text else "No final text")


def _is_navigation_text(text: str) -> bool:
    """
    Check if text is likely to be navigation text that should be removed.
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


if __name__ == "__main__":
    asyncio.run(debug_js_parser())