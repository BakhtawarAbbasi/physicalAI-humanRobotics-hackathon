#!/usr/bin/env python3
"""
Script to parse sitemap.xml and extract all documentation URLs for ingestion.
"""

import requests
from xml.etree import ElementTree as ET
from typing import List


def parse_sitemap(sitemap_url: str) -> List[str]:
    """
    Parse sitemap.xml and extract all URLs.

    Args:
        sitemap_url: URL to the sitemap.xml file

    Returns:
        List of URLs extracted from the sitemap
    """
    response = requests.get(sitemap_url)
    response.raise_for_status()

    # Parse the XML content
    root = ET.fromstring(response.content)

    # Extract all URLs from the sitemap
    urls = []
    for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.append(url_elem.text)

    return urls


def filter_documentation_urls(urls: List[str]) -> List[str]:
    """
    Filter URLs to include only documentation pages.

    Args:
        urls: List of all URLs from the sitemap

    Returns:
        List of documentation URLs only
    """
    documentation_urls = []
    for url in urls:
        # Include URLs that are part of the docs section
        if '/docs/' in url or '/markdown-page' in url:
            documentation_urls.append(url)

    return documentation_urls


def main():
    """Main function to parse sitemap and display URLs."""
    sitemap_url = "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/sitemap.xml"

    print("Fetching sitemap from:", sitemap_url)
    all_urls = parse_sitemap(sitemap_url)

    print(f"Found {len(all_urls)} total URLs in sitemap")

    # Filter to get only documentation URLs
    doc_urls = filter_documentation_urls(all_urls)

    print(f"Found {len(doc_urls)} documentation URLs")
    print("\nDocumentation URLs:")
    for i, url in enumerate(doc_urls, 1):
        print(f"{i:2d}. {url}")

    return doc_urls


if __name__ == "__main__":
    documentation_urls = main()