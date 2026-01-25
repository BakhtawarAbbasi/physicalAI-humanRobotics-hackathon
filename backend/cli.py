"""
Command-line interface for the RAG system ingestion pipeline.

This module provides a comprehensive command-line interface for the RAG system,
allowing users to run the ingestion pipeline with various configuration options.
The CLI supports all major pipeline parameters including URL specification,
crawling depth, chunking parameters, and request configuration.

Usage:
    python cli.py --urls URL1 [URL2 ...] [OPTIONS]

The CLI includes:
- Comprehensive argument parsing with validation
- Configuration override capabilities
- Progress reporting and status updates
- Error handling and reporting
- Integration with the full pipeline system

Configuration can be provided via command-line arguments or environment variables,
with command-line arguments taking precedence. The CLI is designed to be user-friendly
with clear help messages and examples.
"""
import argparse
import asyncio
import sys
from typing import List

from config.settings import ProcessingConfig
from src.pipeline.ingestion_pipeline import IngestionPipeline


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="RAG System - Ingestion Pipeline for URL content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --urls https://example.com/docs
  %(prog)s --urls https://example.com/docs https://example.com/api --depth 2
  %(prog)s --urls https://example.com/docs --chunk-size 1500 --chunk-overlap 300
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
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    return parser


async def run_pipeline_from_args(args) -> bool:
    """Run the ingestion pipeline with the provided arguments."""
    # Create configuration from arguments
    config_dict = {
        'chunk_size': args.chunk_size,
        'chunk_overlap': args.chunk_overlap,
        'max_concurrent_requests': args.max_concurrent,
        'request_delay': args.request_delay,
        'timeout': args.timeout
    }

    # Override environment variables with CLI arguments
    import os
    os.environ['CHUNK_SIZE'] = str(args.chunk_size)
    os.environ['CHUNK_OVERLAP'] = str(args.chunk_overlap)
    os.environ['MAX_CONCURRENT_REQUESTS'] = str(args.max_concurrent)
    os.environ['REQUEST_DELAY'] = str(args.request_delay)
    os.environ['TIMEOUT'] = str(args.timeout)

    # Load configuration (will use env vars set above)
    config = ProcessingConfig()

    # Create pipeline
    pipeline = IngestionPipeline(config)

    try:
        # Run the pipeline
        job = await pipeline.run_pipeline(args.urls, max_depth=args.depth)

        print(f"\nPipeline completed with status: {job.status}")
        print(f"Processed {job.processed_count} content chunks")
        print(f"Failed {job.failed_count} operations")

        if job.error_details:
            print(f"\nErrors encountered:")
            for error in job.error_details:
                print(f"  - {error['timestamp']}: {error['error']} ({error['type']})")

        return job.status == "completed"

    except KeyboardInterrupt:
        print("\nPipeline interrupted by user", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Pipeline failed with error: {str(e)}", file=sys.stderr)
        return False
    finally:
        # Clean up resources
        try:
            pipeline.close()
        except Exception as e:
            print(f"Error during pipeline cleanup: {str(e)}", file=sys.stderr)


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Set up logging based on verbose flag
    import logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Run the async pipeline
    success = asyncio.run(run_pipeline_from_args(args))

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()