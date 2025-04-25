import faiss
import numpy as np
import os
import pickle
from src.config.config import FAISS_INDEX_PATH # Use absolute import from src
# Removed Pinecone import
# from pinecone import Pinecone, ServerlessSpec

# Adjust dimension for Google's embedding-001 model
EMBEDDING_DIM = 768

class VectorDBClient:
    def __init__(self):
        """Initializes the FAISS index, loading from disk if available."""
        self.index_file = FAISS_INDEX_PATH
        self.metadata_file = self.index_file + ".meta"
        self.index = None
        self.index_to_id = []
        self.id_to_metadata = {}

        self.load_index()

        if self.index is None:
            print(f"FAISS index file '{self.index_file}' not found or failed to load. Creating a new index.")
            # Using IndexFlatL2 for simple Euclidean distance search
            self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
            self.index_to_id = []
            self.id_to_metadata = {}
        else:
            print(f"FAISS index loaded from '{self.index_file}' with {self.index.ntotal} vectors.")
            print(f"Metadata loaded for {len(self.id_to_metadata)} IDs.")

    def load_index(self):
        """Loads the FAISS index and metadata from disk."""
        try:
            if os.path.exists(self.index_file):
                self.index = faiss.read_index(self.index_file)
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'rb') as f:
                    saved_data = pickle.load(f)
                    self.index_to_id = saved_data.get('index_to_id', [])
                    self.id_to_metadata = saved_data.get('id_to_metadata', {})
            # Basic consistency check
            if self.index is not None and self.index.ntotal != len(self.index_to_id):
                 print(f"Warning: Index size ({self.index.ntotal}) and ID mapping size ({len(self.index_to_id)}) mismatch. Resetting index.")
                 self.index = None # Force recreation
                 self.index_to_id = []
                 self.id_to_metadata = {}

        except Exception as e:
            print(f"Error loading FAISS index or metadata: {e}. A new index will be created.")
            self.index = None # Ensure index is reset on error
            self.index_to_id = []
            self.id_to_metadata = {}

    def save_index(self):
        """Saves the FAISS index and metadata to disk."""
        try:
            print(f"Saving FAISS index to '{self.index_file}' ({self.index.ntotal} vectors)...")
            faiss.write_index(self.index, self.index_file)
            metadata_to_save = {
                'index_to_id': self.index_to_id,
                'id_to_metadata': self.id_to_metadata
            }
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(metadata_to_save, f)
            print("FAISS index and metadata saved successfully.")
        except Exception as e:
            print(f"Error saving FAISS index or metadata: {e}")

    def upsert_embedding(self, vector_id, embedding, metadata):
        """Adds or updates a vector in the FAISS index."""
        # Note: FAISS IndexFlatL2 doesn't directly support updates or deletions by ID.
        # This implementation currently only adds. True upsert would require rebuilding
        # or using an index type that supports removals (like IndexIDMap).
        # For simplicity, we just add and store metadata.
        try:
            if vector_id in self.id_to_metadata:
                # Simple approach: Ignore if ID already exists to avoid duplicates in this basic setup.
                # More complex logic could involve removing the old vector first if using IndexIDMap.
                print(f"Warning: Vector ID '{vector_id}' already exists. Skipping add. (FAISS IndexFlatL2 doesn't easily support updates)")
                return True # Or False, depending on desired behavior for existing IDs

            vector = np.array([embedding]).astype('float32') # FAISS expects float32 and 2D array
            self.index.add(vector)
            faiss_index = self.index.ntotal - 1 # Index of the added vector
            self.index_to_id.append(vector_id)
            self.id_to_metadata[vector_id] = metadata

            # Check consistency after adding
            if self.index.ntotal != len(self.index_to_id):
                 print(f"CRITICAL ERROR: Index size ({self.index.ntotal}) and ID mapping size ({len(self.index_to_id)}) mismatch after add! Aborting save.")
                 # Potentially try to recover or raise a more specific error
                 return False

            self.save_index() # Save after each addition for persistence
            return True  # Indicate successful add
        except Exception as e:
            print(f"Error adding embedding to FAISS: {e}")
            return False # Indicate add failure

    def query_similar_embeddings(self, query_embedding, top_k=5):
        """Queries FAISS for similar embeddings."""
        if self.index is None or self.index.ntotal == 0:
            print("FAISS index is not initialized or is empty.")
            return {'matches': []} # Return empty matches structure

        try:
            query_vector = np.array([query_embedding]).astype('float32')
            # Search returns distances (D) and indices (I)
            distances, indices = self.index.search(query_vector, top_k)

            results = []
            if len(indices[0]) > 0:
                for i, faiss_index in enumerate(indices[0]):
                    if faiss_index != -1: # -1 indicates no neighbor found
                        vector_id = self.index_to_id[faiss_index]
                        metadata = self.id_to_metadata.get(vector_id, {}) # Get metadata
                        score = distances[0][i] # Lower score (distance) is better
                        results.append({
                            'id': vector_id,
                            'score': float(score), # Ensure score is standard float
                            'metadata': metadata
                        })
            return {'matches': results}
        except Exception as e:
            print(f"Error querying FAISS: {e}")
            return None

# Example Usage needs to be updated
if __name__ == '__main__':
    # Import necessary components for the example
    # This assumes embedding_generator is in the parent directory's embedding_service
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Add src to path
    from embedding_service.embedding_generator import EmbeddingGenerator
    from config.config import OPENAI_API_KEY # Need API key for embedding gen

    if not OPENAI_API_KEY:
        print("Cannot run example: OPENAI_API_KEY not set.")
    else:
        try:
            print("\n--- Running FAISS VectorDBClient Example ---")
            db_client = VectorDBClient()
            embed_gen = EmbeddingGenerator() # Uses OpenAI by default now

            # --- Test Data ---
            test_data = {
                "FAISS_TEST_001": "This is the first test document for FAISS.",
                "FAISS_TEST_002": "FAISS provides efficient similarity search.",
                "FAISS_TEST_003": "Another document to test the FAISS index."
            }
            test_embeddings = {}

            # --- Generate and Upsert Embeddings ---
            print("\n--- Upserting Test Embeddings ---")
            for vec_id, text in test_data.items():
                print(f"Generating embedding for: '{vec_id}'")
                embedding = embed_gen.get_embedding(text)
                if embedding:
                    test_embeddings[vec_id] = embedding
                    metadata = {"text_snippet": text[:50] + "...", "source": "test_data"}
                    print(f"Upserting '{vec_id}'...")
                    success = db_client.upsert_embedding(vec_id, embedding, metadata)
                    if success:
                        print(f"'{vec_id}' upserted successfully.")
                    else:
                        print(f"'{vec_id}' upsert failed.")
                else:
                    print(f"Failed to generate embedding for '{vec_id}'. Skipping upsert.")

            # --- Query Example ---
            print("\n--- Querying Example ---")
            query_text = "Tell me about similarity search"
            print(f"Query Text: '{query_text}'")
            query_embedding = embed_gen.get_embedding(query_text)

            if query_embedding:
                query_results = db_client.query_similar_embeddings(query_embedding, top_k=2)
                if query_results and query_results.get('matches'):
                    print("Query Results (Lower score is more similar):")
                    for match in query_results['matches']:
                        print(f"  Score: {match['score']:.4f}, ID: {match['id']}, Metadata: {match['metadata']}")
                elif query_results is not None:
                     print("No matches found for the query.")
                else:
                    print("Error during query.")
            else:
                print("Failed to generate query embedding.")

            print("\n--- Example Finished ---")

        except Exception as e:
            print(f"\nError during VectorDBClient FAISS example usage: {e}")
            import traceback
            traceback.print_exc()