"""
Metrics collection and monitoring for the RAG system.

This module provides utilities for collecting and monitoring various metrics
throughout the ingestion pipeline, including performance metrics, error rates,
and system health indicators.
"""
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class MetricType(Enum):
    """Types of metrics that can be collected."""
    PERFORMANCE = "performance"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    RESOURCE_USAGE = "resource_usage"
    QUALITY = "quality"


@dataclass
class Metric:
    """Represents a single metric measurement."""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)
    description: Optional[str] = None


class MetricsCollector:
    """Collects and manages metrics for the RAG system."""

    def __init__(self):
        """Initialize the metrics collector."""
        self.metrics: list[Metric] = []
        self.logger = logging.getLogger(__name__)
        self.start_time = time.time()

    def record_metric(self, name: str, value: float, metric_type: MetricType,
                     tags: Optional[Dict[str, str]] = None, description: Optional[str] = None):
        """
        Record a metric measurement.

        Args:
            name: Name of the metric
            value: Value of the metric
            metric_type: Type of metric
            tags: Optional tags for the metric
            description: Optional description of the metric
        """
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            tags=tags or {},
            description=description
        )
        self.metrics.append(metric)
        self.logger.debug(f"Recorded metric: {name} = {value} ({metric_type.value})")

    def record_pipeline_duration(self, duration: float, pipeline_name: str = "ingestion"):
        """Record the duration of a pipeline execution."""
        self.record_metric(
            name=f"{pipeline_name}_duration",
            value=duration,
            metric_type=MetricType.PERFORMANCE,
            tags={"pipeline": pipeline_name},
            description=f"Duration of {pipeline_name} pipeline execution in seconds"
        )

    def record_items_processed(self, count: int, item_type: str = "content_chunks"):
        """Record the number of items processed."""
        self.record_metric(
            name=f"{item_type}_processed",
            value=count,
            metric_type=MetricType.THROUGHPUT,
            tags={"item_type": item_type},
            description=f"Number of {item_type} processed"
        )

    def record_error_rate(self, error_count: int, total_count: int, operation: str = "pipeline"):
        """Record the error rate for an operation."""
        error_rate = (error_count / total_count * 100) if total_count > 0 else 0
        self.record_metric(
            name=f"{operation}_error_rate",
            value=error_rate,
            metric_type=MetricType.ERROR_RATE,
            tags={"operation": operation},
            description=f"Error rate for {operation} operation in percentage"
        )

    def record_content_quality(self, quality_score: float, content_type: str = "chunks"):
        """Record content quality metrics."""
        self.record_metric(
            name=f"{content_type}_quality_score",
            value=quality_score,
            metric_type=MetricType.QUALITY,
            tags={"content_type": content_type},
            description=f"Quality score for {content_type} (0-100 scale)"
        )

    def record_crawl_success_rate(self, successful: int, total: int):
        """Record the success rate of URL crawling."""
        success_rate = (successful / total * 100) if total > 0 else 0
        self.record_metric(
            name="crawl_success_rate",
            value=success_rate,
            metric_type=MetricType.QUALITY,
            tags={"operation": "crawling"},
            description="Success rate of URL crawling in percentage"
        )

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of collected metrics."""
        if not self.metrics:
            return {"message": "No metrics collected yet"}

        summary = {
            "total_metrics": len(self.metrics),
            "collection_duration": time.time() - self.start_time,
            "metrics_by_type": {},
            "latest_metrics": {}
        }

        # Group metrics by type
        for metric in self.metrics:
            if metric.metric_type.value not in summary["metrics_by_type"]:
                summary["metrics_by_type"][metric.metric_type.value] = []
            summary["metrics_by_type"][metric.metric_type.value].append({
                "name": metric.name,
                "value": metric.value,
                "timestamp": metric.timestamp.isoformat()
            })

        # Get latest value for each metric name
        for metric in self.metrics:
            summary["latest_metrics"][metric.name] = metric.value

        return summary

    def get_metric_by_name(self, name: str) -> Optional[Metric]:
        """Get the most recent metric with the given name."""
        for metric in reversed(self.metrics):  # Search in reverse to get the most recent
            if metric.name == name:
                return metric
        return None

    def get_metrics_by_type(self, metric_type: MetricType) -> list[Metric]:
        """Get all metrics of a specific type."""
        return [metric for metric in self.metrics if metric.metric_type == metric_type]

    def reset(self):
        """Reset the metrics collector."""
        self.metrics.clear()
        self.start_time = time.time()
        self.logger.info("Metrics collector reset")


class PipelineMonitor:
    """Monitor for tracking pipeline execution metrics."""

    def __init__(self):
        """Initialize the pipeline monitor."""
        self.metrics_collector = MetricsCollector()
        self.pipeline_start_time = None
        self.logger = logging.getLogger(__name__)

    def start_pipeline(self, pipeline_name: str = "ingestion"):
        """Record the start of a pipeline execution."""
        self.pipeline_start_time = time.time()
        self.logger.info(f"Started monitoring pipeline: {pipeline_name}")

    def end_pipeline(self, pipeline_name: str = "ingestion",
                    items_processed: int = 0, errors_occurred: int = 0):
        """Record the end of a pipeline execution and collect metrics."""
        if self.pipeline_start_time is None:
            self.logger.warning("Pipeline end recorded without start - skipping metrics")
            return

        duration = time.time() - self.pipeline_start_time
        total_items = items_processed + errors_occurred

        # Record metrics
        self.metrics_collector.record_pipeline_duration(duration, pipeline_name)
        self.metrics_collector.record_items_processed(items_processed)

        if total_items > 0:
            self.metrics_collector.record_error_rate(errors_occurred, total_items, pipeline_name)

        self.logger.info(f"Pipeline {pipeline_name} completed in {duration:.2f}s - "
                        f"Processed: {items_processed}, Errors: {errors_occurred}")

    def record_crawl_metrics(self, successful_crawls: int, total_crawls: int):
        """Record metrics related to URL crawling."""
        self.metrics_collector.record_crawl_success_rate(successful_crawls, total_crawls)
        self.logger.info(f"Crawl metrics recorded - Success: {successful_crawls}/{total_crawls}")

    def record_content_metrics(self, content_chunks: list, quality_score: float = None):
        """Record metrics related to content processing."""
        self.metrics_collector.record_items_processed(len(content_chunks), "content_chunks")

        if quality_score is not None:
            self.metrics_collector.record_content_quality(quality_score, "content_chunks")

        self.logger.info(f"Content metrics recorded - {len(content_chunks)} chunks processed")

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all collected metrics."""
        return self.metrics_collector.get_metrics_summary()

    def log_summary(self):
        """Log a summary of collected metrics."""
        summary = self.get_summary()

        if "latest_metrics" in summary:
            self.logger.info("=== Pipeline Metrics Summary ===")
            for name, value in summary["latest_metrics"].items():
                self.logger.info(f"{name}: {value}")
            self.logger.info("===============================")


# Global metrics collector instance for convenience
global_metrics = MetricsCollector()


def get_global_metrics() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return global_metrics


def record_global_metric(name: str, value: float, metric_type: MetricType,
                       tags: Optional[Dict[str, str]] = None, description: Optional[str] = None):
    """Record a metric using the global metrics collector."""
    global_metrics.record_metric(name, value, metric_type, tags, description)