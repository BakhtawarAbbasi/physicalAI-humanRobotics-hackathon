#!/usr/bin/env python3
"""
Test script to debug content extraction from JavaScript-heavy pages - with proper encoding handling.
"""

import asyncio
import sys
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def test_content_extraction():
    """Test content extraction from the page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the page
        await page.goto("https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-02/chapter-1-gazebo-physics", wait_until="networkidle")

        # Wait for content to load
        try:
            await page.wait_for_selector('.theme-doc-markdown', timeout=10000)
        except:
            print("Could not find .theme-doc-markdown selector")
            await page.wait_for_timeout(5000)

        await page.wait_for_timeout(2000)

        # Get the fully rendered HTML
        html_content = await page.content()

        # Now parse the rendered HTML with BeautifulSoup (same as in our parser)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

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

        # Extract clean text content
        clean_text = main_content.get_text(separator=' ', strip=True)

        # Clean up extra whitespace
        clean_text = ' '.join(clean_text.split())

        print(f"Raw extracted text length: {len(clean_text)}")
        print(f"Contains 'Gazebo Physics': {'Gazebo Physics' in clean_text}")
        print(f"Contains 'gravity': {'gravity' in clean_text.lower()}")

        # Print a safe version of the first 200 characters
        safe_preview = clean_text[:200].encode('utf-8', errors='ignore').decode('utf-8')
        print(f"First 200 chars (safe): {safe_preview}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_content_extraction())