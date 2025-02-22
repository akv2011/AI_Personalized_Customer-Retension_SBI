# backend/src/embedding_service/embedding_generator.py
from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initializes the SentenceTransformer model."""
        self.model = SentenceTransformer(model_name)
        print(f"Embedding model '{model_name}' loaded.") # Optional: Confirmation log

    def get_embedding(self, text):
        """Generates a vector embedding for the given text."""
        try:
            embedding = self.model.encode(text, convert_to_tensor=False).tolist() # Convert to list for JSON serialization
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None # Indicate embedding generation failure

if __name__ == '__main__':
    # --- Example Usage ---
    try:
        embed_gen = EmbeddingGenerator()
        sample_text = "This is a sample text to generate an embedding for."
        embedding = embed_gen.get_embedding(sample_text)

        if embedding:
            print(f"Embedding generated successfully for: '{sample_text}'")
            print(f"Embedding (first 10 dimensions): {embedding[:10]}...") # Print first few dimensions
        else:
            print(f"Embedding generation failed for: '{sample_text}'")

    except Exception as e:
        print(f"Error during EmbeddingGenerator example usage: {e}")
        print("Make sure you have sentence-transformers library installed.")