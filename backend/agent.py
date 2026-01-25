#!/usr/bin/env python3
"""
RAG Agent with OpenAI Agents SDK Integration

This script creates an AI agent that can retrieve information from book content using
Qdrant vector search and respond to questions based only on retrieved content.
"""

import argparse
import asyncio
import logging
from typing import List, Dict, Any, Optional
import sys
import os
from pathlib import Path

# Add the backend directory to the path so we can import from config
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import ProcessingConfig
from qdrant_client import QdrantClient
from openai import OpenAI
from pydantic import BaseModel


# Define a model for the retrieval result
class RetrievalResult(BaseModel):
    content: str
    source_url: str
    title: str
    score: float


def retrieve_content_from_qdrant(query: str, top_k: int = 5) -> List[RetrievalResult]:
    """
    Retrieve relevant content chunks from Qdrant based on the query.

    Args:
        query: The search query
        top_k: Number of top results to retrieve (default: 5)

    Returns:
        List of retrieval results with content, source URL, title, and score
    """
    # Load configuration
    config = ProcessingConfig()

    # Initialize Qdrant client
    qdrant_client = QdrantClient(
        url=config.qdrant_url,
        api_key=config.qdrant_api_key,
        https=True
    )

    try:
        # Generate embedding for the query using Cohere
        import cohere
        cohere_client = cohere.Client(config.cohere_api_key)

        response = cohere_client.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"
        )

        query_embedding = response.embeddings[0] if response.embeddings else None

        if not query_embedding:
            raise Exception("Failed to generate embedding for query")

        # Search in Qdrant using the correct method
        search_response = qdrant_client.query_points(
            collection_name="content_embeddings",
            query=query_embedding,
            limit=top_k
        )

        # Handle the response properly - it returns a QueryResponse object with points
        if hasattr(search_response, 'points'):
            search_results = search_response.points
        else:
            search_results = search_response

        # Process results
        results = []
        for result in search_results:
            payload = result.payload
            retrieval_result = RetrievalResult(
                content=payload.get("content", ""),
                source_url=payload.get("source_url", ""),
                title=payload.get("title", ""),
                score=result.score
            )
            results.append(retrieval_result)

        return results

    except Exception as e:
        logging.error(f"Error retrieving content from Qdrant: {str(e)}")
        raise
    finally:
        qdrant_client.close()


def main():
    """Main function to run the RAG agent."""
    parser = argparse.ArgumentParser(description="RAG Agent with OpenAI Integration")
    parser.add_argument("--query", type=str, help="Question to ask the agent",
                        default="What is Gazebo physics simulation?")
    parser.add_argument("--top-k", type=int, default=5, help="Number of top results to retrieve")

    args = parser.parse_args()

    print("Initializing RAG Agent with OpenAI API...")

    try:
        # Retrieve relevant content from Qdrant
        print(f"Processing query: '{args.query}'")
        print(f"Retrieving top-{args.top_k} relevant content chunks...")

        retrieved_results = retrieve_content_from_qdrant(args.query, args.top_k)

        print(f"Retrieved {len(retrieved_results)} content chunks from Qdrant")

        if not retrieved_results:
            print("No relevant content found in documentation")
            return

        # Prepare context for the OpenAI API call
        context_parts = [
            "You are a helpful documentation assistant that answers questions based only on the provided context.",
            "Do not use any external knowledge or make up information.",
            "If the context doesn't contain information to answer the query, say so explicitly.",
            "",
            "QUERY:",
            args.query,
            "",
            "CONTEXT:"
        ]

        for i, result in enumerate(retrieved_results, 1):
            context_parts.extend([
                f"[Source {i} - {result.source_url}]:",
                result.content,
                ""
            ])

        context_parts.append("ANSWER:")
        context = "\n".join(context_parts)

        # Initialize OpenAI client with OpenRouter API
        config = ProcessingConfig()

        # Generate response using OpenRouter API
        import openai
        client = openai.OpenAI(
            api_key=config.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        response = client.chat.completions.create(
            model="microsoft/wizardlm-2-8x22b:nitro",  # Free model from OpenRouter that's available
            messages=[
                {"role": "system", "content": "You are a helpful documentation assistant that answers questions based only on the provided context. Do not use any external knowledge or make up information."},
                {"role": "user", "content": context}
            ],
            temperature=0.1,  # Low temperature for more factual responses
            max_tokens=1000
        )

        answer = response.choices[0].message.content

        print("\n" + "="*80)
        print("RAG AGENT RESPONSE")
        print("="*80)
        print(f"Query: {args.query}")
        print(f"Response: {answer}")
        print(f"Retrieved Chunks: {len(retrieved_results)}")
        print("-" * 80)

        # Show top 3 sources
        print("SOURCES:")
        for i, result in enumerate(retrieved_results[:3], 1):
            print(f"  {i}. {result.source_url}")
            print(f"     Score: {result.score:.3f}")
            print(f"     Title: {result.title}")
            print()

        print("="*80)
        if answer:
            print("OK RAG agent responded successfully!")
            print("The system can successfully retrieve and respond using documentation content.")
        else:
            print("NO RAG agent did not return a response.")

        print("="*80)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"NO Error running RAG agent: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()