#!/usr/bin/env python3
"""
More detailed debug script to understand the issue with the JS parser.
"""

import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.async_api import async_playwright


async def detailed_debug():
    """Debug the JS parser with more details."""
    timeout = 30000

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the page
        url = "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-02/chapter-1-gazebo-physics"
        print(f"Loading page: {url}")

        await page.goto(url, wait_until="networkidle")
        print("Page loaded with networkidle")

        # Wait for Docusaurus-specific content to load
        try:
            await page.wait_for_selector('.theme-doc-markdown', timeout=10000)
            print("Found .theme-doc-markdown selector")
        except Exception as e:
            print(f"Could not find .theme-doc-markdown selector: {e}")
            # Wait for main content
            try:
                await page.wait_for_selector('main', timeout=5000)
                print("Found main selector")
            except:
                print("Could not find main selector either")
                await page.wait_for_timeout(5000)

        await page.wait_for_timeout(2000)
        print("Waited for content to render")

        # Get the fully rendered HTML
        html_content = await page.content()
        print(f"HTML content length: {len(html_content)}")

        # Check if key content exists in raw HTML
        if 'Gazebo Physics Simulation' in html_content:
            print("OK Found 'Gazebo Physics Simulation' in raw HTML")
        else:
            print("NO Could NOT find 'Gazebo Physics Simulation' in raw HTML")

        # Parse the rendered HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        print(f"BeautifulSoup parsed {len(str(soup))} characters")

        # Look for the main content area
        selectors_to_try = [
            'main',
            '.main-wrapper',
            '.container.padding-vert--lg',
            '.container',
            '.markdown',
            '.theme-doc-markdown',
            '.article',
            'article',
            '.docItemContainer_Djhp',
            '.theme-doc-markdown.markdown'
        ]

        content_found = False
        for selector in selectors_to_try:
            elements = soup.select(selector)
            if elements:
                element = elements[0]
                text_content = element.get_text(separator=' ', strip=True)
                clean_text = ' '.join(text_content.split())
                print(f"Selector '{selector}' found content: {len(clean_text)} chars")

                if 'Gazebo Physics Simulation' in clean_text:
                    print(f"✓ Content found in selector '{selector}' with key phrase!")
                    print(f"Preview: {clean_text[:200]}...")
                    content_found = True
                    break
                elif len(clean_text) > 100:  # If we have substantial content
                    print(f"~ Content found in selector '{selector}', length: {len(clean_text)}")
                    print(f"Preview: {clean_text[:200]}...")
                    content_found = True
                    break

        if not content_found:
            print("No content found in expected selectors")
            # Try getting content from the entire body
            body = soup.find('body')
            if body:
                text_content = body.get_text(separator=' ', strip=True)
                clean_text = ' '.join(text_content.split())
                print(f"Body content: {len(clean_text)} chars")
                if len(clean_text) > 0:
                    print(f"Body preview: {clean_text[:200]}...")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(detailed_debug())