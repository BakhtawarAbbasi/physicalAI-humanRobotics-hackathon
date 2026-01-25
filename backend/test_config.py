#!/usr/bin/env python3
"""Test script to verify the configuration loading."""

from config.settings import ProcessingConfig

def test_config():
    """Test loading the configuration."""
    try:
        config = ProcessingConfig()
        print("Configuration loaded successfully!")
        print(f"Cohere API key: {config.cohere_api_key[:10]}...")
        print(f"OpenAI API key: {config.openai_api_key[:10]}...")
        print(f"Qdrant URL: {config.qdrant_url}")
        print(f"Qdrant API key: {config.qdrant_api_key[:10]}...")
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_config()