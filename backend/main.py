#!/usr/bin/env python3
"""
Main entry point for the RAG system ingestion pipeline.

This script orchestrates the entire ingestion process:
1. Crawls Docusaurus documentation sites
2. Extracts and cleans text content
3. Chunks the content appropriately
4. Generates embeddings using Cohere
5. Stores embeddings in Qdrant Cloud

For command-line usage, see cli.py
"""

import asyncio
import logging
from typing import List

from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline


def setup_logging():
    """Set up basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


async def main():
    """Main ingestion pipeline function for programmatic use."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting RAG system ingestion pipeline...")

    # Load configuration
    config = ProcessingConfig()

    # Initialize the full pipeline
    pipeline = IngestionPipeline(config)

    try:
        # For demonstration, we'll use a sample URL
        # In a real scenario, this would come from config or command line
        sample_urls = ["https://example.com"]  # This should be configured via environment variable

        logger.info(f"Starting crawl of URLs: {sample_urls}")

        # Run the complete pipeline
        job = await pipeline.run_pipeline(sample_urls, max_depth=1)

        logger.info(f"Pipeline completed with status: {job.status}")
        logger.info(f"Processed {job.processed_count} content chunks")
        logger.info(f"Failed {job.failed_count} operations")

        if job.error_details:
            logger.warning(f"Errors encountered: {len(job.error_details)}")

        success = job.status == "completed"

        if success:
            logger.info("Successfully completed the RAG ingestion pipeline!")
            # Get and display storage information
            storage_info = pipeline.embedding_service.get_storage_info()
            logger.info(f"Storage collection info: {storage_info}")
        else:
            logger.error("Failed to complete the ingestion pipeline")

        return success

    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        return False
    except Exception as e:
        logger.error(f"Error in ingestion pipeline: {str(e)}")
        return False
    finally:
        # Clean up resources
        try:
            pipeline.close()
        except Exception as e:
            logger.error(f"Error during pipeline cleanup: {str(e)}")


if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        exit(1)