"""
Main ingestion pipeline service for the RAG system.

This module orchestrates the entire ingestion pipeline from crawling to storage.
It coordinates all components of the RAG system including crawling, chunking,
embedding generation, and storage in Qdrant. The pipeline is designed to be
resilient, efficient, and trackable with comprehensive error handling and
progress reporting.

The pipeline follows these main steps:
1. Crawling: Extract content from specified URLs using the CrawlerService
2. Chunking: Process and split content into appropriately sized chunks
3. Validation: Ensure content quality and proper formatting
4. Embedding: Generate vector embeddings using Cohere API
5. Storage: Store embeddings in Qdrant vector database

Each step includes error handling, progress tracking, and quality validation
to ensure robust processing of documentation sites, particularly Docusaurus-based
documentation.
"""

import asyncio
import logging
import time
from typing import List, Optional, Dict
from datetime import datetime

from config.settings import ProcessingConfig
from src.common.models import ContentChunk, CrawlJob
from src.common.exceptions import RAGException
from src.crawler.crawler_service import CrawlerService
from src.chunker.chunker_service import ChunkerService
from src.embedding.embedding_service import EmbeddingService
from .crawl_job_manager import CrawlJobManager
from ..utils.metrics_collector import PipelineMonitor


class IngestionPipeline:
    """Orchestrates the entire ingestion pipeline from crawling to storage."""

    def __init__(self, config: ProcessingConfig):
        """
        Initialize the ingestion pipeline with all required services.

        Args:
            config: Processing configuration
        """
        self.config = config
        self.crawler_service = CrawlerService(config)
        self.chunker_service = ChunkerService(config)
        self.embedding_service = EmbeddingService(config)
        self.job_manager = CrawlJobManager()
        self.monitor = PipelineMonitor()
        self.logger = logging.getLogger(__name__)

    async def run_pipeline(self, urls: List[str], max_depth: int = 1, job_id: Optional[str] = None) -> CrawlJob:
        """
        Run the complete ingestion pipeline from crawling to storage.

        Args:
            urls: List of URLs to crawl and process
            max_depth: Maximum depth to follow links during crawling
            job_id: Optional job ID for tracking (if not provided, one will be generated)

        Returns:
            CrawlJob object with status and results
        """
        # Create a crawl job using the job manager
        crawl_job = self.job_manager.create_job(
            urls=urls,
            config={
                "max_depth": max_depth,
                "chunk_size": self.config.chunk_size,
                "chunk_overlap": self.config.chunk_overlap,
                "max_concurrent_requests": self.config.max_concurrent_requests
            }
        )

        # If a specific job_id was requested, update the job
        if job_id and crawl_job.id != job_id:
            # In a real implementation, we'd need to handle ID assignment differently
            # For now, we'll just use the generated ID
            pass

        self.logger.info(f"Starting ingestion pipeline job {crawl_job.id} for {len(urls)} URLs")

        # Start monitoring
        self.monitor.start_pipeline("ingestion")

        try:
            # Update job status to in_progress
            self.job_manager.update_job_status(crawl_job.id, "in_progress")

            # Step 1: Crawl URLs to extract content
            self.logger.info(f"Step 1: Crawling {len(urls)} URLs with max depth {max_depth}")
            content_chunks = await self._safe_crawl_urls(urls, max_depth, crawl_job.id)
            self.logger.info(f"Successfully extracted {len(content_chunks)} content chunks from crawling")

            # Record crawl metrics
            self.monitor.record_crawl_metrics(len(content_chunks), len(urls))

            # Update job progress
            self.job_manager.update_job_progress(crawl_job.id, len(content_chunks), 0)

            # Report progress
            self._report_progress(crawl_job.id, "crawling", len(content_chunks), len(urls))

            # Step 2: Process and chunk the content appropriately
            self.logger.info("Step 2: Processing and chunking content...")
            processed_chunks = await self._safe_process_chunks(content_chunks, crawl_job.id)
            self.logger.info(f"Processed into {len(processed_chunks)} final chunks")

            # Step 3: Validate chunks before embedding
            self.logger.info("Step 3: Validating content chunks...")
            valid_chunks = self._safe_validate_chunks(processed_chunks, crawl_job.id)
            self.logger.info(f"Validated {len(valid_chunks)} chunks for embedding")

            # Record content processing metrics
            self.monitor.record_content_metrics(valid_chunks)

            # Report progress
            self._report_progress(crawl_job.id, "chunking", len(valid_chunks), len(content_chunks))

            # Step 4: Generate embeddings and store in Qdrant
            self.logger.info("Step 4: Generating embeddings and storing in Qdrant...")
            success = await self._safe_generate_and_store_embeddings(valid_chunks, crawl_job.id)

            if success:
                self.logger.info(f"Successfully completed pipeline job {crawl_job.id}")
                self.job_manager.update_job_status(crawl_job.id, "completed")
                self._report_progress(crawl_job.id, "completed", len(valid_chunks), len(valid_chunks))

                # Record success metrics
                self.monitor.end_pipeline(
                    pipeline_name="ingestion",
                    items_processed=len(valid_chunks),
                    errors_occurred=0
                )

                return self.job_manager.get_job(crawl_job.id)
            else:
                self.logger.error(f"Failed to complete pipeline job {crawl_job.id}")
                self.job_manager.update_job_status(crawl_job.id, "failed")

                # Record failure metrics
                self.monitor.end_pipeline(
                    pipeline_name="ingestion",
                    items_processed=0,
                    errors_occurred=len(valid_chunks)
                )

                return self.job_manager.get_job(crawl_job.id)

        except Exception as e:
            self.logger.error(f"Critical error in pipeline job {crawl_job.id}: {str(e)}", exc_info=True)
            self.job_manager.update_job_status(crawl_job.id, "failed")
            self.job_manager.add_job_error(crawl_job.id, str(e), type(e).__name__)

            # Record error metrics
            self.monitor.end_pipeline(
                pipeline_name="ingestion",
                items_processed=0,
                errors_occurred=1
            )

            raise
        finally:
            # Log metrics summary
            self.monitor.log_summary()

    async def _safe_crawl_urls(self, urls: List[str], max_depth: int, job_id: str) -> List[ContentChunk]:
        """
        Safely crawl URLs with error handling.

        Args:
            urls: List of URLs to crawl
            max_depth: Maximum depth to follow links
            job_id: ID of the job for error tracking

        Returns:
            List of content chunks, or empty list if error occurred
        """
        try:
            content_chunks = await self.crawler_service.crawl_urls(urls, max_depth=max_depth)
            return content_chunks
        except Exception as e:
            self.logger.error(f"Error during crawling for job {job_id}: {str(e)}", exc_info=True)
            self.job_manager.add_job_error(job_id, f"Crawling error: {str(e)}", type(e).__name__)
            raise

    async def _safe_process_chunks(self, content_chunks: List[ContentChunk], job_id: str) -> List[ContentChunk]:
        """
        Safely process content chunks with error handling.

        Args:
            content_chunks: List of content chunks to process
            job_id: ID of the job for error tracking

        Returns:
            List of processed content chunks, or empty list if error occurred
        """
        try:
            processed_chunks = self.chunker_service.process_content_chunks(content_chunks)
            return processed_chunks
        except Exception as e:
            self.logger.error(f"Error during chunking for job {job_id}: {str(e)}", exc_info=True)
            self.job_manager.add_job_error(job_id, f"Chunking error: {str(e)}", type(e).__name__)
            raise

    def _safe_validate_chunks(self, processed_chunks: List[ContentChunk], job_id: str) -> List[ContentChunk]:
        """
        Safely validate content chunks with error handling.

        Args:
            processed_chunks: List of processed content chunks to validate
            job_id: ID of the job for error tracking

        Returns:
            List of validated content chunks
        """
        try:
            valid_chunks = self.chunker_service.validate_chunks(processed_chunks)
            return valid_chunks
        except Exception as e:
            self.logger.error(f"Error during validation for job {job_id}: {str(e)}", exc_info=True)
            self.job_manager.add_job_error(job_id, f"Validation error: {str(e)}", type(e).__name__)
            raise

    async def _safe_generate_and_store_embeddings(self, valid_chunks: List[ContentChunk], job_id: str) -> bool:
        """
        Safely generate and store embeddings with error handling.

        Args:
            valid_chunks: List of validated content chunks to embed
            job_id: ID of the job for error tracking

        Returns:
            True if successful, False otherwise
        """
        try:
            success = self.embedding_service.generate_and_store_embeddings(valid_chunks)
            return success
        except Exception as e:
            self.logger.error(f"Error during embedding/storage for job {job_id}: {str(e)}", exc_info=True)
            self.job_manager.add_job_error(job_id, f"Embedding/storage error: {str(e)}", type(e).__name__)
            raise

    def _report_progress(self, job_id: str, stage: str, processed: int, total: int):
        """
        Report progress for a specific job and stage.

        Args:
            job_id: ID of the job
            stage: Current processing stage
            processed: Number of items processed
            total: Total number of items to process
        """
        progress_percentage = (processed / total * 100) if total > 0 else 0
        self.logger.info(f"Job {job_id} - {stage}: {processed}/{total} ({progress_percentage:.1f}%)")

    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """
        Get detailed status information for a job.

        Args:
            job_id: ID of the job to check

        Returns:
            Dictionary with job status information, or None if job not found
        """
        job = self.job_manager.get_job(job_id)
        if job:
            return {
                "job_id": job.id,
                "status": job.status,
                "urls": job.urls,
                "processed_count": job.processed_count,
                "failed_count": job.failed_count,
                "start_time": job.start_time.isoformat(),
                "end_time": job.end_time.isoformat() if job.end_time else None,
                "config": job.config,
                "error_details": job.error_details
            }
        return None

    def validate_pipeline_config(self, urls: List[str], max_depth: int) -> List[str]:
        """
        Validate the pipeline configuration before running.

        Args:
            urls: List of URLs to validate
            max_depth: Maximum depth to validate

        Returns:
            List of validation errors, empty if all validations pass
        """
        errors = []

        # Validate URLs
        if not urls or len(urls) == 0:
            errors.append("URLs list cannot be empty")

        for url in urls:
            if not url or not url.strip():
                errors.append(f"URL cannot be empty: '{url}'")
            elif not url.startswith(('http://', 'https://')):
                errors.append(f"Invalid URL format: '{url}' - must start with http:// or https://")

        # Validate max_depth
        if max_depth < 0:
            errors.append("max_depth must be non-negative")
        if max_depth > 5:  # Reasonable limit to prevent excessive crawling
            errors.append("max_depth should be 5 or less to prevent excessive crawling")

        # Validate config parameters
        if self.config.chunk_size <= 0:
            errors.append("chunk_size must be positive")
        if self.config.chunk_overlap < 0:
            errors.append("chunk_overlap must be non-negative")
        if self.config.chunk_overlap >= self.config.chunk_size:
            errors.append("chunk_overlap must be less than chunk_size")
        if self.config.max_concurrent_requests <= 0:
            errors.append("max_concurrent_requests must be positive")
        if self.config.request_delay < 0:
            errors.append("request_delay must be non-negative")
        if self.config.timeout <= 0:
            errors.append("timeout must be positive")

        return errors

    def validate_content_quality(self, content_chunks: List[ContentChunk]) -> Dict[str, any]:
        """
        Validate the quality of content chunks.

        Args:
            content_chunks: List of content chunks to validate

        Returns:
            Dictionary with validation results
        """
        total_chunks = len(content_chunks)
        valid_chunks = 0
        empty_chunks = 0
        short_chunks = 0
        total_chars = 0

        for chunk in content_chunks:
            is_valid = True
            if not chunk.content or not chunk.content.strip():
                empty_chunks += 1
                is_valid = False
            elif len(chunk.content) < 10:  # Less than 10 characters is considered too short
                short_chunks += 1
                is_valid = False

            if is_valid:
                valid_chunks += 1
                total_chars += len(chunk.content)

        avg_chunk_length = total_chars / valid_chunks if valid_chunks > 0 else 0

        return {
            "total_chunks": total_chunks,
            "valid_chunks": valid_chunks,
            "empty_chunks": empty_chunks,
            "short_chunks": short_chunks,
            "valid_percentage": (valid_chunks / total_chunks * 100) if total_chunks > 0 else 0,
            "avg_chunk_length": avg_chunk_length,
            "total_characters": total_chars
        }

    async def run_pipeline_with_validation(self, urls: List[str], max_depth: int = 1, job_id: Optional[str] = None) -> CrawlJob:
        """
        Run the complete ingestion pipeline with validation checks.

        Args:
            urls: List of URLs to crawl and process
            max_depth: Maximum depth to follow links during crawling
            job_id: Optional job ID for tracking (if not provided, one will be generated)

        Returns:
            CrawlJob object with status and results
        """
        # Validate configuration first
        validation_errors = self.validate_pipeline_config(urls, max_depth)
        if validation_errors:
            error_msg = f"Pipeline configuration validation failed: {'; '.join(validation_errors)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # Run the regular pipeline
        return await self.run_pipeline(urls, max_depth, job_id)

    async def run_pipeline_for_single_url(self, url: str) -> CrawlJob:
        """
        Run the complete ingestion pipeline for a single URL.

        Args:
            url: URL to crawl and process

        Returns:
            CrawlJob object with status and results
        """
        return await self.run_pipeline([url])

    def get_pipeline_status(self, job_id: str) -> Optional[CrawlJob]:
        """
        Get the status of a pipeline job (placeholder implementation).

        In a real implementation, this would retrieve job status from a database.

        Args:
            job_id: ID of the job to check

        Returns:
            CrawlJob object if found, None otherwise
        """
        # This is a placeholder - in a real implementation, you'd store jobs in a database
        self.logger.warning("Job status tracking is not implemented in this version")
        return None

    def close(self):
        """Close all service connections and clean up resources."""
        self.logger.info("Starting graceful shutdown of ingestion pipeline...")

        # Close embedding service (includes Qdrant connection)
        try:
            self.embedding_service.close()
            self.logger.info("Embedding service closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing embedding service: {str(e)}")

        # Perform any other cleanup as needed
        self.logger.info("Ingestion pipeline resources cleaned up")