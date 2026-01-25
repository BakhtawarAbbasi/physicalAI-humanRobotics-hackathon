#!/usr/bin/env python3
"""
Script to run the RAG ingestion pipeline with all documentation URLs from the sitemap.
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


async def run_ingestion_with_sitemap():
    """Run the ingestion pipeline with all documentation URLs from the sitemap."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting RAG system ingestion pipeline with all documentation URLs...")

    # Load configuration
    config = ProcessingConfig()

    # Initialize the full pipeline
    pipeline = IngestionPipeline(config)

    # Documentation URLs extracted from sitemap
    documentation_urls = [
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/markdown-page",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/category/module-1---the-robotic-nervous-system-ros-2",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/category/module-2---the-digital-twin-gazebo--unity",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/intro",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-01/chapter-1-ros2-fundamentals",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-01/chapter-2-agent-ros-bridge",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-01/chapter-3-urdf-modeling",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-02/",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-02/chapter-1-gazebo-physics",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-02/chapter-2-sensor-simulation",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-02/chapter-3-unity-digital-twin",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-03/isaac-ros",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-03/isaac-sim",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-03/nav2-navigation",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-03/quickstart",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-04/capstone",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-04/cognitive-planning",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-04/voice-to-action"
    ]

    logger.info(f"Starting crawl of {len(documentation_urls)} documentation URLs")

    try:
        # Run the complete pipeline with all documentation URLs
        job = await pipeline.run_pipeline_with_validation(documentation_urls, max_depth=0)

        logger.info(f"Pipeline completed with status: {job.status}")
        logger.info(f"Processed {job.processed_count} content chunks")
        logger.info(f"Failed {job.failed_count} operations")

        if job.error_details:
            logger.warning(f"Errors encountered: {len(job.error_details)}")
            for error in job.error_details:
                logger.warning(f"  - {error['error']} ({error['type']})")

        success = job.status == "completed"

        if success:
            logger.info("Successfully completed the RAG ingestion pipeline!")
            # Get and display storage information
            storage_info = pipeline.embedding_service.get_storage_info()
            logger.info(f"Storage collection info: {storage_info}")
        else:
            logger.error("Failed to complete the ingestion pipeline")

        # Get detailed job status
        job_status = pipeline.get_job_status(job.id)
        if job_status:
            logger.info(f"Job details: {job_status}")

        return success

    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        return False
    except Exception as e:
        logger.error(f"Error in ingestion pipeline: {str(e)}", exc_info=True)
        return False
    finally:
        # Clean up resources
        try:
            pipeline.close()
        except Exception as e:
            logger.error(f"Error during pipeline cleanup: {str(e)}")


def main():
    """Main function to run the ingestion pipeline."""
    success = asyncio.run(run_ingestion_with_sitemap())
    if not success:
        exit(1)


if __name__ == "__main__":
    main()