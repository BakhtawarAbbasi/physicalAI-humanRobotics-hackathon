#!/usr/bin/env python3
"""
FastAPI server for RAG agent with Qdrant integration.

This module implements a FastAPI server that exposes a query endpoint
to receive user queries from the frontend and process them through
the existing RAG agent with retrieval from Qdrant.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

# Add the backend directory to the path so we can import from config
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config.settings import ProcessingConfig
from src.crawler.js_html_parser import JSHTMLParser
from fastapi.middleware.cors import CORSMiddleware


# Define request/response models
class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    query: str
    top_k: Optional[int] = 5


class RetrievedChunk(BaseModel):
    """Model for retrieved content chunks."""
    content: str
    source_url: str
    title: str
    score: float
    chunk_index: int


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    answer: str
    sources: List[str]
    retrieved_chunks: List[RetrievedChunk]
    success: bool
    error_message: Optional[str] = None


# Create FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="API for querying the RAG agent with documentation content retrieval",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose the headers that the frontend might need to access
    expose_headers=["Access-Control-Allow-Origin"]
)


class RAGAgentAPI:
    """API wrapper for the RAG agent functionality."""

    def __init__(self):
        """Initialize the RAG Agent API with configuration and clients."""
        self.config = ProcessingConfig()
        self.js_parser = JSHTMLParser(timeout=self.config.timeout * 1000)  # Convert to milliseconds
        self.logger = logging.getLogger(__name__)

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    async def query_rag_agent(self, query: str, top_k: int = 5) -> QueryResponse:
        """
        Process a query through the RAG agent with Qdrant retrieval.

        Args:
            query: The user query to process
            top_k: Number of top results to retrieve

        Returns:
            QueryResponse with answer and supporting information
        """
        try:
            self.logger.info(f"Processing query: '{query[:50]}{'...' if len(query) > 50 else ''}'")

            # This is where we'd integrate with the existing agent functionality
            # For now, we'll simulate the process using the existing retrieval logic
            from src.crawler.crawler_service import CrawlerService

            # Initialize crawler service to use existing retrieval functionality
            crawler = CrawlerService(self.config)

            # Since we're creating an API, we need to simulate the retrieval process
            # We'll use the existing retrieval mechanism from agent.py but adapt it for API use
            retrieved_chunks = await self._retrieve_content_from_qdrant(query, top_k)

            if not retrieved_chunks:
                return QueryResponse(
                    answer="No relevant content found in the documentation for your query.",
                    sources=[],
                    retrieved_chunks=[],
                    success=False,
                    error_message="No relevant content found"
                )

            # Generate context for response generation
            context_parts = [
                "You are a helpful documentation assistant that answers questions based only on the provided context.",
                "Do not use any external knowledge or make up information.",
                "If the context doesn't contain information to answer the query, say so explicitly.",
                "",
                "QUERY:",
                query,
                "",
                "CONTEXT:"
            ]

            sources = set()
            processed_chunks = []

            for i, chunk in enumerate(retrieved_chunks[:top_k], 1):
                context_parts.extend([
                    f"[Source {i} - {chunk.source_url}]:",
                    chunk.content,
                    ""
                ])
                sources.add(chunk.source_url)

                processed_chunk = RetrievedChunk(
                    content=chunk.content,
                    source_url=chunk.source_url,
                    title=chunk.title,
                    score=chunk.score,
                    chunk_index=chunk.chunk_index
                )
                processed_chunks.append(processed_chunk)

            context_parts.append("ANSWER:")
            context = "\n".join(context_parts)

            # Generate response using OpenRouter API (similar to agent.py)
            from openai import AsyncOpenAI

            openai_client = AsyncOpenAI(
                api_key=self.config.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1"
            )

            response = await openai_client.chat.completions.create(
                model="microsoft/wizardlm-2-8x22b:nitro",  # Using a high-quality free model
                messages=[
                    {"role": "system", "content": "You are a helpful documentation assistant that answers questions based only on the provided context. Do not use any external knowledge or make up information."},
                    {"role": "user", "content": context}
                ],
                temperature=0.1,  # Low temperature for factual responses
                max_tokens=1000
            )

            answer = response.choices[0].message.content

            return QueryResponse(
                answer=answer,
                sources=list(sources),
                retrieved_chunks=processed_chunks,
                success=True
            )

        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return QueryResponse(
                answer="An error occurred while processing your query.",
                sources=[],
                retrieved_chunks=[],
                success=False,
                error_message=str(e)
            )

    async def _retrieve_content_from_qdrant(self, query: str, top_k: int) -> List[RetrievedChunk]:
        """
        Retrieve content from Qdrant using the existing retrieval pipeline logic.

        Args:
            query: Query string to search for
            top_k: Number of top results to retrieve

        Returns:
            List of retrieved content chunks
        """
        try:
            # Reuse the retrieval logic from the existing system
            from src.storage.qdrant_storage import QdrantStorage
            from qdrant_client import QdrantClient
            import cohere

            # Initialize Qdrant client
            qdrant_client = QdrantClient(
                url=self.config.qdrant_url,
                api_key=self.config.qdrant_api_key,
                https=True
            )

            # Generate embedding for the query using Cohere
            cohere_client = cohere.Client(self.config.cohere_api_key)

            response = cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            )

            query_embedding = response.embeddings[0] if response.embeddings else None

            if not query_embedding:
                raise Exception("Failed to generate embedding for query")

            # Search in Qdrant using the query_points method
            search_response = qdrant_client.query_points(
                collection_name="content_embeddings",
                query=query_embedding,
                limit=top_k
            )

            # Process results - query_points method returns a response with points
            results = []
            # The query_points response should always have points, iterate directly
            for result in search_response.points:
                payload = result.payload if hasattr(result, 'payload') else getattr(result, 'payload', {})

                retrieved_chunk = RetrievedChunk(
                    content=payload.get("content", ""),
                    source_url=payload.get("source_url", ""),
                    title=payload.get("title", ""),
                    score=getattr(result, 'score', 0.0),
                    chunk_index=payload.get("chunk_index", 0)
                )
                results.append(retrieved_chunk)

            self.logger.info(f"Retrieved {len(results)} content chunks for query")

            # Close the client connection
            qdrant_client.close()

            return results

        except Exception as e:
            self.logger.error(f"Error retrieving content from Qdrant: {str(e)}")
            return []


# Initialize the RAG Agent API
rag_agent = RAGAgentAPI()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Process a user query through the RAG agent.

    Args:
        request: QueryRequest containing the query and top_k parameter

    Returns:
        QueryResponse with the agent's answer and supporting information
    """
    try:
        response = await rag_agent.query_rag_agent(request.query, request.top_k)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running."""
    return {"status": "healthy", "timestamp": __import__('datetime').datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn

    # Run the API server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )