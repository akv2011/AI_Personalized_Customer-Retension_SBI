# backend/src/vector_database/vector_db_client.py
import pinecone
from src.config import config  # Import config to access Pinecone settings
from pinecone import Pinecone, ServerlessSpec # Import Pinecone class

class VectorDBClient:
    def __init__(self):
        """Initializes the Pinecone client and connects to the specified index."""
        self.pc = Pinecone(  # Use Pinecone class for initialization
            api_key=config.PINECONE_API_KEY # Initialize with just the API Key
        )
        self.index = self.pc.Index(config.PINECONE_INDEX_NAME) # Get index using the Pinecone instance

    def upsert_embedding(self, vector_id, embedding, metadata):
        """Upserts a vector to the Pinecone index."""
        try:
            self.index.upsert(vectors=[(vector_id, embedding, metadata)])
            return True  # Indicate successful upsert
        except Exception as e:
            print(f"Error upserting to Pinecone: {e}")
            return False # Indicate upsert failure

    def query_similar_embeddings(self, query_embedding, top_k=5):
        """Queries Pinecone for similar embeddings."""
        try:
            query_results = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
            return query_results
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            return None # Indicate query failure

    # Optional: Add methods for deleting vectors, fetching vectors, etc. if needed

if __name__ == '__main__':
    # --- Example Usage (assuming you have Pinecone and config setup correctly) ---
    try:
        db_client = VectorDBClient()
        embed_gen = EmbeddingGenerator() # Assuming EmbeddingGenerator is defined (see next code block)

        # Example: Upsert a test vector
        test_vector_id = "TEST_VECTOR_001"
        test_text_to_embed = "This is a test vector for Pinecone."
        test_embedding = embed_gen.get_embedding(test_text_to_embed) # Assuming EmbeddingGenerator.get_embedding exists
        test_metadata = {"test_data": "example metadata", "text": test_text_to_embed}

        if db_client.upsert_embedding(test_vector_id, test_embedding, test_metadata):
            print(f"Test vector '{test_vector_id}' upserted successfully.")
        else:
            print(f"Test vector '{test_vector_id}' upsert failed.")

        # Example: Query for similar vectors (using the same embedding as query for testing)
        query_results = db_client.query_similar_embeddings(test_embedding)
        if query_results and query_results.matches:
            print("\nQuery Results:")
            for match in query_results.matches:
                print(f"  Score: {match.score}, ID: {match.id}, Metadata: {match.metadata.get('text', 'No Text in Metadata')[:50]}...")
        else:
            print("\nNo query results returned or error during query.")

    except Exception as e:
        print(f"Error during VectorDBClient example usage: {e}")
        print("Make sure you have set your PINECONE_API_KEY and PINECONE_ENVIRONMENT environment variables correctly, and that your Pinecone index exists.")