#!/bin/bash

# Setup script for RAG system on Linux/Mac

echo "Setting up RAG system environment..."

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not in PATH. Please install Python 3.11 or higher."
    exit 1
fi

# Check Python version
version=$(python3 --version 2>&1 | cut -d' ' -f2)
major=$(echo $version | cut -d'.' -f1)
minor=$(echo $version | cut -d'.' -f2)

if [ $major -lt 3 ] || ([ $major -eq 3 ] && [ $minor -lt 11 ]); then
    echo "Python 3.11 or higher is required. Current version: $version"
    exit 1
fi

echo "Python version $version is compatible."

# Install uv package manager if not already installed
if ! pip list | grep -q uv; then
    echo "Installing uv package manager..."
    pip install uv
fi

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment and install dependencies
source .venv/bin/activate
echo "Installing dependencies..."
uv pip install -e .

echo
echo "Environment setup complete!"
echo "To activate the virtual environment in the future, run: source .venv/bin/activate"
echo
echo "Set your environment variables in .env file:"
echo "- COHERE_API_KEY=your_cohere_api_key"
echo "- QDRANT_URL=your_qdrant_cluster_url"
echo "- QDRANT_API_KEY=your_qdrant_api_key"
echo
echo "Then run the ingestion pipeline with:"
echo "python cli.py --urls https://example.com/docs"