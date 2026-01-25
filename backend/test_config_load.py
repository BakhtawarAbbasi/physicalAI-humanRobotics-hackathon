#!/usr/bin/env python3
"""Test script to check if the configuration loads properly."""

import sys
from pathlib import Path

# Add the backend directory to the path so we can import from config
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import ProcessingConfig


def test_config_loading():
    """Test if the configuration loads properly."""
    try:
        config = ProcessingConfig()
        print("Configuration loaded successfully!")
        print(f"Cohere API Key: {config.cohere_api_key[:10]}...")
        print(f"OpenAI API Key: {config.openai_api_key[:10]}...")
        print(f"Qdrant URL: {config.qdrant_url}")
        print(f"Qdrant API Key: {config.qdrant_api_key[:10]}...")
        return True
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_config_loading()