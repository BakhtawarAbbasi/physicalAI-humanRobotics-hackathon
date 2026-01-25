"""
Crawl job management service for the RAG system.

This module handles tracking and management of crawl jobs throughout their lifecycle.
The CrawlJobManager provides a centralized way to create, track, update, and
manage the status of ingestion jobs in the RAG system.

Key features:
- Job creation with initial status and configuration
- Status tracking (pending, in_progress, completed, failed)
- Progress reporting with processed/failed counters
- Error tracking with timestamps and details
- Job listing and cleanup functionality

The job manager is designed to work in-memory for this implementation, but could
be extended to use persistent storage for production environments. Each job tracks
important metrics like start/end times, configuration parameters, and error details
to provide comprehensive monitoring and debugging capabilities.
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime

from src.common.models import CrawlJob


class CrawlJobManager:
    """Manages tracking and status of crawl jobs."""

    def __init__(self):
        """Initialize the crawl job manager."""
        self.jobs: Dict[str, CrawlJob] = {}
        self.logger = logging.getLogger(__name__)

    def create_job(self, urls: List[str], config: Dict) -> CrawlJob:
        """
        Create a new crawl job.

        Args:
            urls: List of URLs to crawl
            config: Configuration for the crawl job

        Returns:
            Created CrawlJob object
        """
        job = CrawlJob(
            urls=urls,
            status="pending",
            config=config
        )
        self.jobs[job.id] = job
        self.logger.info(f"Created new crawl job {job.id} for {len(urls)} URLs")
        return job

    def get_job(self, job_id: str) -> Optional[CrawlJob]:
        """
        Get a crawl job by ID.

        Args:
            job_id: ID of the job to retrieve

        Returns:
            CrawlJob object if found, None otherwise
        """
        return self.jobs.get(job_id)

    def update_job_status(self, job_id: str, status: str) -> bool:
        """
        Update the status of a crawl job.

        Args:
            job_id: ID of the job to update
            status: New status for the job

        Returns:
            True if update was successful, False otherwise
        """
        job = self.jobs.get(job_id)
        if job:
            old_status = job.status
            job.status = status
            self.logger.info(f"Updated job {job_id} status from {old_status} to {status}")
            return True
        return False

    def update_job_progress(self, job_id: str, processed_count: int, failed_count: int) -> bool:
        """
        Update the progress of a crawl job.

        Args:
            job_id: ID of the job to update
            processed_count: Number of items processed
            failed_count: Number of items that failed

        Returns:
            True if update was successful, False otherwise
        """
        job = self.jobs.get(job_id)
        if job:
            job.processed_count = processed_count
            job.failed_count = failed_count
            return True
        return False

    def add_job_error(self, job_id: str, error: str, error_type: str = "unknown") -> bool:
        """
        Add an error to a crawl job.

        Args:
            job_id: ID of the job to update
            error: Error message to add
            error_type: Type of error (optional)

        Returns:
            True if update was successful, False otherwise
        """
        job = self.jobs.get(job_id)
        if job:
            job.error_details.append({
                "timestamp": datetime.now().isoformat(),
                "error": error,
                "type": error_type
            })
            return True
        return False

    def complete_job(self, job_id: str, success: bool = True) -> bool:
        """
        Mark a job as completed.

        Args:
            job_id: ID of the job to complete
            success: Whether the job completed successfully

        Returns:
            True if update was successful, False otherwise
        """
        job = self.jobs.get(job_id)
        if job:
            job.status = "completed" if success else "failed"
            job.end_time = datetime.now()
            return True
        return False

    def list_jobs(self) -> List[CrawlJob]:
        """
        Get a list of all crawl jobs.

        Returns:
            List of all CrawlJob objects
        """
        return list(self.jobs.values())

    def cleanup_old_jobs(self, days: int = 7) -> int:
        """
        Clean up jobs older than specified number of days.

        Args:
            days: Number of days to keep jobs

        Returns:
            Number of jobs removed
        """
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        old_job_ids = [
            job_id for job_id, job in self.jobs.items()
            if job.start_time.timestamp() < cutoff_time
        ]

        for job_id in old_job_ids:
            del self.jobs[job_id]

        self.logger.info(f"Cleaned up {len(old_job_ids)} old jobs")
        return len(old_job_ids)