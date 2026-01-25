#!/usr/bin/env python3
"""
Verification script to check the status of content ingestion in Qdrant.
"""

from config.settings import ProcessingConfig
from qdrant_client import QdrantClient


def verify_ingestion_status():
    """Verify the ingestion status by checking stored embeddings in Qdrant."""
    config = ProcessingConfig()

    # Create Qdrant client directly
    client = QdrantClient(
        url=config.qdrant_url,
        api_key=config.qdrant_api_key,
        https=True
    )

    collection_name = "content_embeddings"

    print("Verifying Qdrant collection status...")

    try:
        # Get collection info
        collection_info = client.get_collection(collection_name)
        print(f"Collection name: {collection_name}")
        print(f"Vector size: {collection_info.config.params.vectors.size}")
        print(f"Distance: {collection_info.config.params.vectors.distance}")
        print(f"Point count: {collection_info.points_count}")

        # Get sample points to verify content
        scroll_result, next_page = client.scroll(
            collection_name=collection_name,
            limit=5,  # Just check first 5 as sample
            with_payload=True,
            with_vectors=False
        )

        print(f"\nSample of stored points (first 5):")
        for i, point in enumerate(scroll_result):
            payload = point.payload
            print(f"  Point {i+1}:")
            print(f"    ID: {point.id}")
            print(f"    Source URL: {payload.get('source_url', 'N/A')}")
            print(f"    Title: {payload.get('title', 'N/A')}")
            print(f"    Content length: {len(payload.get('content', ''))}")
            print(f"    Chunk index: {payload.get('chunk_index', 'N/A')}")
            print()

        print(f"Successfully verified {len(scroll_result)} sample points")

        # Check for specific documentation pages
        print("Checking for specific documentation pages...")

        # Scroll through all points to find target documentation
        all_points, _ = client.scroll(
            collection_name=collection_name,
            limit=1000,  # Get up to 1000 points
            with_payload=True,
            with_vectors=False
        )

        target_urls = [
            "module-02/chapter-1-gazebo-physics",
            "module-02/chapter-2-sensor-simulation",
            "module-02/chapter-3-unity-digital-twin",
            "module-01/chapter-1-ros2-fundamentals",
            "module-03/isaac-ros",
            "module-04/capstone"
        ]

        found_urls = []
        for point in all_points:
            source_url = point.payload.get('source_url', '')
            for target in target_urls:
                if target in source_url and source_url not in found_urls:
                    found_urls.append(source_url)
                    print(f"  ✅ Found: {source_url}")
                    break

        print(f"\nFound {len(found_urls)} of {len(target_urls)} target documentation pages")
        print(f"Total points in collection: {collection_info.points_count}")
        print(f"Total points retrieved in scroll: {len(all_points)}")

        # Close client
        client.close()
        return True

    except Exception as e:
        print(f"Error during verification: {str(e)}")
        try:
            client.close()
        except:
            pass
        return False


if __name__ == "__main__":
    verify_ingestion_status()