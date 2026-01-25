"""
Custom exceptions for the RAG system.

This module contains custom exception classes for error handling throughout the system.
"""


class RAGException(Exception):
    """Base exception class for RAG system errors."""
    pass


class CrawlerException(RAGException):
    """Exception raised when crawling operations fail."""
    pass


class ParserException(RAGException):
    """Exception raised when HTML parsing operations fail."""
    pass


class ChunkerException(RAGException):
    """Exception raised when text chunking operations fail."""
    pass


class EmbeddingException(RAGException):
    """Exception raised when embedding operations fail."""
    pass


class StorageException(RAGException):
    """Exception raised when storage operations fail."""
    pass


class ConfigurationException(RAGException):
    """Exception raised when configuration validation fails."""
    pass


class NetworkException(CrawlerException):
    """Exception raised when network operations fail."""
    pass


class RateLimitException(CrawlerException):
    """Exception raised when rate limits are exceeded."""
    pass


class APIException(RAGException):
    """Exception raised when API operations fail."""
    pass


class ContentValidationException(RAGException):
    """Exception raised when content validation fails."""
    pass