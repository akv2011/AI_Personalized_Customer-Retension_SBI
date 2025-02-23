import json  # Import the json module
import os
from src.vector_database.vector_db_client import VectorDBClient
from src.embedding_service.embedding_generator import EmbeddingGenerator
from src.config import config
import pandas as pd
import openai  # Import the openai library

class RecommendationEngine:
    def __init__(self):
        self.vector_db_client = VectorDBClient()
        self.embedding_generator = EmbeddingGenerator()
        openai.api_key = config.OPENAI_API_KEY  # Set OpenAI API key

    def process_user_interaction(self, customer_id, interaction_text, interaction_type="chatbot"):
        """Processes user interaction, stores it in Pinecone, and gets a personalized response."""
        conversation_turn_id = f"{customer_id}_{int(pd.Timestamp.now().timestamp())}"
        embedding = self.embedding_generator.get_embedding(interaction_text)
        metadata = {
            "customer_id": customer_id,
            "conversation_id": "BASIC_CONVO_" + str(int(pd.Timestamp.now().timestamp())),  # Basic convo ID for now
            "timestamp": str(pd.Timestamp.now()),
            "speaker": "customer",
            "text": interaction_text,
            "interaction_type": interaction_type,
            "outcome": "message_stored"  # Basic outcome for now
        }
        if self.vector_db_client:
            self.vector_db_client.upsert_embedding(conversation_turn_id, embedding, metadata)
        print(f"Stored interaction in Pinecone: {conversation_turn_id}")  # Confirmation log

        # Get personalized response using RAG and OpenAI
        response = self.get_rag_personalized_response(customer_id, interaction_text)
        return response

    def get_openai_response_test(self, prompt_text):
        try:
            response = openai.chat.completions.create(  # Updated API call format
                model="gpt-4o",  # Or another simple model
                messages=[
                    {"role": "user", "content": prompt_text}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return "I apologize, but I'm having trouble processing your request right now."

    # --- Corrected Indentation for get_rag_personalized_response ---
    def get_rag_personalized_response(self, customer_id, user_input_text):
        """Generates a formatted personalized response using RAG with Pinecone and OpenAI."""
        query_embedding = self.embedding_generator.get_embedding(user_input_text)
        if query_embedding:
            query_results = self.vector_db_client.query_similar_embeddings(query_embedding, top_k=3)
            
            similar_interactions_context = []
            if query_results and query_results.matches:
                for match in query_results.matches:
                    metadata = match.metadata
                    similar_interactions_context.append(f"Similar interaction text: {metadata.get('text', 'No text')}, Outcome: {metadata.get('outcome', 'No outcome')}")

            context_string = "\n".join(similar_interactions_context)

            prompt = f"""You are an AI assistant for SBI Life Insurance.
                Generate a helpful and personalized response to the user's query.
                
                User query: "{user_input_text}"

                Context from similar past interactions:
                {context_string}

                Format your response in the following JSON structure:
                {{
                    "sections": [
                        {{
                            "type": "main_response",
                            "content": "Primary response text"
                        }},
                        {{
                            "type": "bullet_points",
                            "points": ["Point 1", "Point 2", "Point 3"]
                        }},
                        {{
                            "type": "action_items",
                            "items": ["Action 1", "Action 2"]
                        }}
                    ]
                }}

                Ensure each section is concise and relevant to the query.
                """

            try:
                openai_response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant for SBI Life Insurance. Format responses in structured JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=400
                )
                
                response_text = openai_response.choices[0].message.content.strip()
                formatted_response = json.loads(response_text)
                
                return {
                    "rag_response": {
                        "formatted_response": formatted_response,
                        "source": "RAG+OpenAI"
                    }
                }
                
            except Exception as e:
                print(f"Error in RAG response generation: {e}")
                return {
                    "rag_response": {
                        "formatted_response": {
                            "sections": [{
                                "type": "main_response",
                                "content": "I apologize, but I'm having trouble processing your request right now."
                            }]
                        },
                        "source": "Error"
                    }
                }
        return {
            "rag_response": {
                "formatted_response": {
                    "sections": [{
                        "type": "main_response",
                        "content": "I'm here to help you with SBI Life insurance. How can I assist you today?"
                    }]
                },
                "source": "Fallback"
            }
        }


if __name__ == '__main__':
    # Example Usage for testing (optional)
    recommender = RecommendationEngine()
    recommender.process_user_interaction("TEST_USER_001", "Hello, just testing the storage.")
    print("Test interaction processed.")
    # Test OpenAI function (optional):
    openai_test_result = recommender.get_openai_response_test("Write a very short poem about insurance.")
    print(f"\nOpenAI Test Result:\n{openai_test_result}")