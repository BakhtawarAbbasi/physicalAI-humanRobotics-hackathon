#!/usr/bin/env python3
"""
Test script to verify the JavaScript-enabled parser works with documentation pages.
"""

import asyncio
from config.settings import ProcessingConfig
from src.crawler.js_html_parser import JSHTMLParser


async def test_js_parser():
    """Test the JavaScript-enabled parser with a documentation page."""
    config = ProcessingConfig()
    js_parser = JSHTMLParser(timeout=config.timeout * 1000)

    # Test URL that was problematic
    test_url = "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-02/chapter-1-gazebo-physics"

    print(f"Testing JavaScript-enabled parser on: {test_url}")

    try:
        content, title = await js_parser.parse_and_clean(test_url)
        print(f"Title: {title}")
        print(f"Content length: {len(content)} characters")
        safe_preview = content[:200].encode('utf-8', errors='ignore').decode('utf-8') if content else 'No content'
        print(f"First 200 chars: {safe_preview}")
        print(f"Content length: {len(content) if content else 0} characters")

        if content and len(content) > 0:
            print("SUCCESS: Content extracted!")
        else:
            print("FAILURE: No content extracted")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_js_parser())