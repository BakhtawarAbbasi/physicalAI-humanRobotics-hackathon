#!/usr/bin/env python3
"""
Debug script to understand how the content is structured in the HTML.
"""

import asyncio
from playwright.async_api import async_playwright


async def debug_content_structure():
    """Debug the content structure of the page."""
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

        print("HTML Content length:", len(html_content))

        # Check if the content is present
        if 'Gazebo Physics Simulation' in html_content:
            print("Found 'Gazebo Physics Simulation' in HTML")
        else:
            print("Could NOT find 'Gazebo Physics Simulation' in HTML")

        # Look for the content area
        start_idx = html_content.find('<div class="theme-doc-markdown markdown">')
        if start_idx != -1:
            print("Found theme-doc-markdown div!")
            # Extract content from that div
            end_idx = html_content.find('</div>', start_idx)
            if end_idx != -1:
                content_area = html_content[start_idx:end_idx+6]
                print("Content area length:", len(content_area))
                print("Content area preview:", content_area[:500])
        else:
            print("Could NOT find theme-doc-markdown div")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_content_structure())