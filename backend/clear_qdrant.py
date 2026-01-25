#!/usr/bin/env python3
"""
Script to clear the Qdrant collection before re-ingesting.
"""

from config.settings import ProcessingConfig
from qdrant_client import QdrantClient


def clear_qdrant_collection():
    """Clear the Qdrant collection."""
    config = ProcessingConfig()

    # Create Qdrant client directly
    client = QdrantClient(
        url=config.qdrant_url,
        api_key=config.qdrant_api_key,
        https=True
    )

    collection_name = "content_embeddings"

    print("Clearing Qdrant collection...")

    try:
        # Get collection info first
        collection_info = client.get_collection(collection_name)
        print(f"Current collection info:")
        print(f"  Points count: {collection_info.points_count}")
        print(f"  Vector size: {collection_info.config.params.vectors.size}")
        print(f"  Distance: {collection_info.config.params.vectors.distance}")

        # Clear the collection by deleting and recreating it
        client.delete_collection(collection_name)
        print(f"Deleted collection: {collection_name}")

        # Recreate collection
        from qdrant_client.http import models
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere's default embedding size
                distance=models.Distance.COSINE
            )
        )
        print(f"Recreated collection: {collection_name}")

        # Verify it's empty
        collection_info = client.get_collection(collection_name)
        print(f"New collection info:")
        print(f"  Points count: {collection_info.points_count}")

        client.close()
        print("Collection cleared successfully!")
        return True

    except Exception as e:
        print(f"Error clearing collection: {str(e)}")
        try:
            client.close()
        except:
            pass
        return False


if __name__ == "__main__":
    clear_qdrant_collection()