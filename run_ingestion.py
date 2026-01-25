#!/usr/bin/env python3
"""
Script to run the ingestion pipeline with proper environment setup.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Now import and run the pipeline
from backend.scripts.run_pipeline import main

if __name__ == "__main__":
    # Set up command line arguments to crawl the local Docusaurus site
    sys.argv = [
        'run_ingestion.py',
        '--urls', 'http://localhost:3000',
        '--verbose'
    ]

    main()