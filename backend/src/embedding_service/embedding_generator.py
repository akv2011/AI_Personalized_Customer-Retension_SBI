import google.generativeai as genai
from src.config.config import GOOGLE_API_KEY # Use Google API Key

class EmbeddingGenerator:
    def __init__(self, model="models/embedding-001"):
        """Initializes the Google Generative AI client."""
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        try:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = model
            # Optional: Test connection or list models to ensure key is valid
            # models = [m for m in genai.list_models() if 'embedContent' in m.supported_generation_methods]
            # print(f"Available Google embedding models: {models}") 
            print(f"EmbeddingGenerator initialized with Google model: {self.model}")
        except Exception as e:
            print(f"Error configuring Google Generative AI: {e}")
            raise

    def get_embedding(self, text, task_type="RETRIEVAL_DOCUMENT"):
        """Generates an embedding for the given text using the configured Google model.
        
        Args:
            text: The text to embed.
            task_type: The task type for the embedding. Common types include:
                       RETRIEVAL_QUERY, RETRIEVAL_DOCUMENT, SEMANTIC_SIMILARITY,
                       CLASSIFICATION, CLUSTERING.
        """
        try:
            # Google API might have limits on text length per call
            # Simple approach: Use the provided text directly.
            # More robust: Handle potential errors related to text length.
            if not text.strip():
                print("Warning: Attempting to embed empty or whitespace-only text.")
                return None # Or handle as appropriate
                
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type=task_type
            )
            embedding = result['embedding']
            # print(f"Generated Google embedding of dimension {len(embedding)} for task '{task_type}' and text snippet: '{text[:50]}...'") # Optional: for debugging
            return embedding
        except Exception as e:
            print(f"Error generating Google embedding: {e}")
            # Add more specific error handling if needed (e.g., for API key issues, quota limits)
            return None

# --- Keep the old OpenAI class commented out or remove if no longer needed ---
# import openai
# from openai import OpenAI
# from src.config.config import OPENAI_API_KEY 
# class EmbeddingGeneratorOpenAI:
#     ...