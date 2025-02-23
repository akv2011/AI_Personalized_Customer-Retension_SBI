import os
from src.vector_database.vector_db_client import VectorDBClient
from src.embedding_service.embedding_generator import EmbeddingGenerator
from src.config import config
import pandas as pd
import openai # Import the openai library

class RecommendationEngine:
    def __init__(self):
        self.vector_db_client = VectorDBClient()
        self.embedding_generator = EmbeddingGenerator()
        openai.api_key = config.OPENAI_API_KEY # Set OpenAI API key

    def process_user_interaction(self, customer_id, interaction_text, interaction_type="chatbot"):
        """Processes user interaction and stores it in Pinecone."""
        conversation_turn_id = f"{customer_id}_{int(pd.Timestamp.now().timestamp())}"
        embedding = self.embedding_generator.get_embedding(interaction_text)
        metadata = {
            "customer_id": customer_id,
            "conversation_id": "BASIC_CONVO_" + str(int(pd.Timestamp.now().timestamp())), # Basic convo ID for now
            "timestamp": str(pd.Timestamp.now()),
            "speaker": "customer",
            "text": interaction_text,
            "interaction_type": interaction_type,
            "outcome": "message_stored" # Basic outcome for now
        }
        if self.vector_db_client:
            self.vector_db_client.upsert_embedding(conversation_turn_id, embedding, metadata)
        print(f"Stored interaction in Pinecone: {conversation_turn_id}") # Confirmation log

    def get_openai_response_test(self, prompt_text): # New function to test OpenAI API
        """Tests OpenAI API connectivity with a simple completion task."""
        try:
            response = openai.completions.create( # Use openai.completions.create
                model="gpt-3.5-turbo-instruct", # Or another simple model
                prompt=prompt_text,
                max_tokens=50
            )
            return response.choices[0].text.strip() # Return the generated text
        except Exception as e:
            error_message = f"Error calling OpenAI API: {e}"
            print(error_message)
            return error_message # Return error message to be sent to frontend

    def get_rag_personalized_response(self, customer_id, user_input_text):
        """Placeholder for RAG response generation."""
        openai_test_prompt = f"User message: '{user_input_text}'.  Respond briefly."
        openai_response = self.get_openai_response_test(openai_test_prompt)
        return {"rag_response": {"rag_response": openai_response, "source": "OpenAI Test"}} # Return OpenAI response for now


if __name__ == '__main__':
    # Example Usage for testing (optional)
    recommender = RecommendationEngine()
    recommender.process_user_interaction("TEST_USER_001", "Hello, just testing the storage.")
    print("Test interaction processed.")
    # Test OpenAI function (optional):
    openai_test_result = recommender.get_openai_response_test("Write a very short poem about insurance.")
    print(f"\nOpenAI Test Result:\n{openai_test_result}")