# backend/src/personalization_engine/recommendation_engine.py
import os
from src.vector_database.vector_db_client import VectorDBClient
from src.embedding_service.embedding_generator import EmbeddingGenerator
from src.config import config
import pandas as pd

class RecommendationEngine:
    def __init__(self):
        self.vector_db_client = VectorDBClient() # **Corrected line - no arguments passed**
        self.embedding_generator = EmbeddingGenerator()

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

    def get_rag_personalized_response(self, customer_id, user_input_text):
        """Placeholder for RAG response generation."""
        return {"rag_response": {"rag_response": "Placeholder RAG response.  RAG logic not fully implemented yet."}} # Placeholder

if __name__ == '__main__':
    # Example Usage for testing (optional)
    recommender = RecommendationEngine()
    recommender.process_user_interaction("TEST_USER_001", "Hello, just testing the storage.")
    print("Test interaction processed.")