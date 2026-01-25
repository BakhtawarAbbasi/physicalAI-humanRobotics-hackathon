#!/usr/bin/env python3
"""
Deployment script for running the RAG ingestion pipeline.

This script provides a simple way to run the ingestion pipeline with
configuration validation and monitoring.
"""
import argparse
import asyncio
import logging
import os
import sys
from typing import List

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.config_validator import validate_setup_for_pipeline
from src.utils.metrics_collector import get_global_metrics
from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline


def setup_logging(verbosity: int = 1):
    """Set up logging based on verbosity level."""
    if verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for the deployment script."""
    parser = argparse.ArgumentParser(
        description="Run the RAG ingestion pipeline with validation and monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --urls https://example.com/docs
  %(prog)s --urls https://example.com/docs --validate-only
  %(prog)s --urls https://example.com/docs --chunk-size 1500 --verbose
        """
    )

    parser.add_argument(
        '--urls',
        nargs='+',
        required=True,
        help='URLs to crawl and process'
    )

    parser.add_argument(
        '--depth',
        type=int,
        default=1,
        help='Maximum depth to follow links during crawling (default: 1)'
    )

    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate the setup, don\'t run the pipeline'
    )

    parser.add_argument(
        '--chunk-size',
        type=int,
        default=1000,
        help='Size of text chunks (default: 1000)'
    )

    parser.add_argument(
        '--chunk-overlap',
        type=int,
        default=200,
        help='Overlap between chunks (default: 200)'
    )

    parser.add_argument(
        '--max-concurrent',
        type=int,
        default=5,
        help='Maximum number of concurrent requests (default: 5)'
    )

    parser.add_argument(
        '--request-delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=1,
        help='Increase verbosity (use -v, -vv, or -vvv for more output)'
    )

    return parser


async def run_pipeline_with_monitoring(urls: List[str], config_params: dict, validate_only: bool):
    """Run the pipeline with monitoring and validation."""
    logger = logging.getLogger(__name__)

    # Override environment variables with provided parameters
    os.environ['CHUNK_SIZE'] = str(config_params['chunk_size'])
    os.environ['CHUNK_OVERLAP'] = str(config_params['chunk_overlap'])
    os.environ['MAX_CONCURRENT_REQUESTS'] = str(config_params['max_concurrent'])
    os.environ['REQUEST_DELAY'] = str(config_params['request_delay'])
    os.environ['TIMEOUT'] = str(config_params['timeout'])

    # Validate setup before proceeding
    logger.info("Validating environment setup...")
    if not validate_setup_for_pipeline(urls):
        logger.error("Setup validation failed. Please fix the issues above.")
        return False

    if validate_only:
        logger.info("Validation completed successfully. Skipping pipeline execution.")
        return True

    # Load configuration and create pipeline
    config = ProcessingConfig()
    pipeline = IngestionPipeline(config)

    try:
        logger.info(f"Starting pipeline with {len(urls)} URLs...")
        job = await pipeline.run_pipeline(urls, max_depth=config_params['depth'])

        logger.info(f"Pipeline completed with status: {job.status}")
        logger.info(f"Processed {job.processed_count} content chunks")
        logger.info(f"Failed {job.failed_count} operations")

        if job.error_details:
            logger.warning(f"Errors encountered: {len(job.error_details)}")

        # Print metrics summary
        metrics = get_global_metrics()
        summary = metrics.get_metrics_summary()
        if 'latest_metrics' in summary:
            logger.info("=== Metrics Summary ===")
            for name, value in summary['latest_metrics'].items():
                logger.info(f"{name}: {value}")

        return job.status == "completed"

    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        return False
    finally:
        if 'pipeline' in locals():
            try:
                pipeline.close()
            except:
                pass


def main():
    """Main entry point for the deployment script."""
    parser = create_parser()
    args = parser.parse_args()

    # Set up logging
    setup_logging(args.verbose)

    # Prepare configuration parameters
    config_params = {
        'depth': args.depth,
        'chunk_size': args.chunk_size,
        'chunk_overlap': args.chunk_overlap,
        'max_concurrent': args.max_concurrent,
        'request_delay': args.request_delay,
        'timeout': args.timeout
    }

    # Run the pipeline
    success = asyncio.run(
        run_pipeline_with_monitoring(args.urls, config_params, args.validate_only)
    )

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()