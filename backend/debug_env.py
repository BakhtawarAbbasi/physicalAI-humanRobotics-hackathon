#!/usr/bin/env python3
"""Debug script to check environment variables."""

import os
from pathlib import Path
import dotenv

def check_env_vars():
    """Check if environment variables are accessible."""
    # Load the .env file from the parent directory
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        print(f"Loading .env file from: {env_path}")
        dotenv.load_dotenv(env_path)
    else:
        print(f".env file not found at: {env_path}")

    print("Environment variables check:")
    print(f"OPENAI_API_KEY: {'SET' if 'OPENAI_API_KEY' in os.environ else 'NOT SET'}")
    print(f"COHERE_API_KEY: {'SET' if 'COHERE_API_KEY' in os.environ else 'NOT SET'}")
    print(f"QDRANT_URL: {'SET' if 'QDRANT_URL' in os.environ else 'NOT SET'}")
    print(f"QDRANT_API_KEY: {'SET' if 'QDRANT_API_KEY' in os.environ else 'NOT SET'}")

    # Print actual values (first 10 chars for security)
    if 'OPENAI_API_KEY' in os.environ:
        val = os.environ['OPENAI_API_KEY']
        print(f"OPENAI_API_KEY value (first 10): {val[:10] if val else 'None'}")
    if 'COHERE_API_KEY' in os.environ:
        val = os.environ['COHERE_API_KEY']
        print(f"COHERE_API_KEY value (first 10): {val[:10] if val else 'None'}")
    if 'QDRANT_URL' in os.environ:
        val = os.environ['QDRANT_URL']
        print(f"QDRANT_URL value: {val}")
    if 'QDRANT_API_KEY' in os.environ:
        val = os.environ['QDRANT_API_KEY']
        print(f"QDRANT_API_KEY value (first 10): {val[:10] if val else 'None'}")

if __name__ == "__main__":
    check_env_vars()