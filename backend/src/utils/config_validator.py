"""
Configuration validation and environment setup checks for the RAG system.

This module provides utilities for validating configuration and environment setup
before running the ingestion pipeline. It includes checks for API connectivity,
environment variables, and configuration parameter validation.
"""
import os
import sys
from typing import List, Tuple
import requests
from urllib.parse import urlparse

from config.settings import ProcessingConfig


def validate_environment_variables() -> Tuple[bool, List[str]]:
    """
    Validate that all required environment variables are set.

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    required_vars = [
        'COHERE_API_KEY',
        'QDRANT_URL',
        'QDRANT_API_KEY'
    ]

    errors = []
    for var in required_vars:
        if not os.getenv(var):
            errors.append(f"Missing required environment variable: {var}")

    return len(errors) == 0, errors


def validate_api_connectivity(config: ProcessingConfig) -> Tuple[bool, List[str]]:
    """
    Validate connectivity to external APIs.

    Args:
        config: Processing configuration with API credentials

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Validate Cohere API connectivity
    try:
        import cohere
        client = cohere.Client(config.cohere_api_key)
        # Make a simple API call to test connectivity
        models = client.models.list()
        if not models:
            errors.append("Could not connect to Cohere API or no models available")
    except Exception as e:
        errors.append(f"Cohere API connectivity test failed: {str(e)}")

    # Validate Qdrant connectivity
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            https=True
        )
        # Try to get collections to test connectivity
        client.get_collections()
    except Exception as e:
        errors.append(f"Qdrant connectivity test failed: {str(e)}")

    return len(errors) == 0, errors


def validate_urls(urls: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate the format and accessibility of URLs.

    Args:
        urls: List of URLs to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    for url in urls:
        if not url or not url.strip():
            errors.append(f"Empty URL provided: '{url}'")
            continue

        if not url.startswith(('http://', 'https://')):
            errors.append(f"Invalid URL format: '{url}' - must start with http:// or https://")
            continue

        # Parse URL to check validity
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                errors.append(f"Invalid URL format: '{url}' - no domain specified")
        except Exception:
            errors.append(f"Invalid URL format: '{url}'")

    return len(errors) == 0, errors


def validate_config_parameters(config: ProcessingConfig) -> Tuple[bool, List[str]]:
    """
    Validate configuration parameters.

    Args:
        config: Processing configuration to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Validate chunk parameters
    if config.chunk_size <= 0:
        errors.append("chunk_size must be positive")
    if config.chunk_overlap < 0:
        errors.append("chunk_overlap must be non-negative")
    if config.chunk_overlap >= config.chunk_size:
        errors.append("chunk_overlap must be less than chunk_size")

    # Validate crawling parameters
    if config.max_concurrent_requests <= 0:
        errors.append("max_concurrent_requests must be positive")
    if config.request_delay < 0:
        errors.append("request_delay must be non-negative")
    if config.timeout <= 0:
        errors.append("timeout must be positive")

    return len(errors) == 0, errors


def run_full_validation(config: ProcessingConfig, urls: List[str] = None) -> Tuple[bool, List[str]]:
    """
    Run full validation including environment, API connectivity, and configuration.

    Args:
        config: Processing configuration to validate
        urls: Optional list of URLs to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    all_errors = []

    # Validate environment variables
    env_valid, env_errors = validate_environment_variables()
    all_errors.extend(env_errors)

    # Validate configuration parameters
    config_valid, config_errors = validate_config_parameters(config)
    all_errors.extend(config_errors)

    if env_valid and config_valid:
        # Only test API connectivity if environment is valid
        api_valid, api_errors = validate_api_connectivity(config)
        all_errors.extend(api_errors)

    # Validate URLs if provided
    if urls:
        urls_valid, url_errors = validate_urls(urls)
        all_errors.extend(url_errors)

    return len(all_errors) == 0, all_errors


def check_environment_setup() -> bool:
    """
    Check if the environment is properly set up for the RAG system.

    Returns:
        True if environment is properly set up, False otherwise
    """
    print("Checking environment setup...")

    # Check environment variables
    env_valid, env_errors = validate_environment_variables()
    if not env_valid:
        print("ERROR: Environment validation failed:")
        for error in env_errors:
            print(f"  - {error}")
        return False

    # Load config to test it
    try:
        config = ProcessingConfig()
    except Exception as e:
        print(f"ERROR: Configuration loading failed: {str(e)}")
        return False

    # Validate config parameters
    config_valid, config_errors = validate_config_parameters(config)
    if not config_valid:
        print("ERROR: Configuration validation failed:")
        for error in config_errors:
            print(f"  - {error}")
        return False

    print("SUCCESS: Environment variables and configuration are valid")
    return True


def validate_and_test_apis() -> bool:
    """
    Validate and test connectivity to external APIs.

    Returns:
        True if all APIs are accessible, False otherwise
    """
    print("Testing API connectivity...")

    try:
        config = ProcessingConfig()
    except Exception as e:
        print(f"ERROR: Could not load configuration: {str(e)}")
        return False

    api_valid, api_errors = validate_api_connectivity(config)
    if not api_valid:
        print("ERROR: API connectivity tests failed:")
        for error in api_errors:
            print(f"  - {error}")
        return False

    print("SUCCESS: All APIs are accessible")
    return True


def validate_setup_for_pipeline(urls: List[str] = None) -> bool:
    """
    Validate the complete setup for running the ingestion pipeline.

    Args:
        urls: Optional list of URLs to validate

    Returns:
        True if setup is valid for running the pipeline, False otherwise
    """
    print("Validating complete setup for ingestion pipeline...")

    # Check environment
    if not check_environment_setup():
        return False

    # Test API connectivity
    if not validate_and_test_apis():
        return False

    # Validate URLs if provided
    if urls:
        urls_valid, url_errors = validate_urls(urls)
        if not urls_valid:
            print("ERROR: URL validation failed:")
            for error in url_errors:
                print(f"  - {error}")
            return False

    print("SUCCESS: Complete setup validation passed")
    return True


if __name__ == "__main__":
    # If run directly, perform basic validation
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
        success = validate_setup_for_pipeline(urls)
    else:
        success = check_environment_setup()

    if not success:
        print("\nERROR: Setup validation failed. Please fix the issues above before running the pipeline.")
        sys.exit(1)
    else:
        print("\nSUCCESS: Setup validation passed. Environment is ready for the RAG system.")
        sys.exit(0)