#!/usr/bin/env python3
"""Test script to check what methods are available in the Qdrant client."""

from config.settings import ProcessingConfig
from qdrant_client import QdrantClient


def check_qdrant_methods():
    """Check what methods are available in the Qdrant client."""
    config = ProcessingConfig()

    client = QdrantClient(
        url=config.qdrant_url,
        api_key=config.qdrant_api_key,
        https=True
    )

    # Get all methods of the client
    methods = [method for method in dir(client) if not method.startswith('_')]

    print("Available methods in Qdrant client:")
    for method in sorted(methods):
        print(f"  - {method}")

    # Check specifically for search-related methods
    search_methods = [method for method in methods if 'search' in method.lower()]
    print(f"\nSearch-related methods: {search_methods}")

    client.close()


if __name__ == "__main__":
    check_qdrant_methods()