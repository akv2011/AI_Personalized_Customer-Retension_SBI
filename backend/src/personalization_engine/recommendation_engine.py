import json
import os
from src.vector_database.vector_db_client import VectorDBClient
from src.embedding_service.embedding_generator import EmbeddingGenerator
from src.config import config
import pandas as pd
import openai

class RecommendationEngine:
    def __init__(self):
        self.vector_db_client = VectorDBClient()
        self.embedding_generator = EmbeddingGenerator()
        openai.api_key = config.OPENAI_API_KEY

    def clean_json_response(self, response_text):
        """Clean OpenAI response text to ensure valid JSON"""
      
        cleaned = response_text.replace('```json', '').replace('```', '')
        # Strip whitespace
        cleaned = cleaned.strip()
        return cleaned

    def process_user_interaction(self, customer_id, interaction_text, interaction_type="chatbot"):
        """Processes user interaction, stores it in Pinecone, and gets a personalized response."""
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

        # Get personalized response
        response = self.get_rag_personalized_response(customer_id, interaction_text)
        return response

    def get_rag_personalized_response(self, customer_id, user_input_text):
        """Generates a formatted personalized response using RAG with Pinecone and OpenAI."""
        # Generate embedding for the query
        query_embedding = self.embedding_generator.get_embedding(user_input_text)
        
        # Handle embedding generation failure
        if not query_embedding:
            return {
                "rag_response": {
                    "formatted_response": {
                        "sections": [{
                            "type": "main_response",
                            "content": "Error generating response."
                        }]
                    },
                    "source": "Embedding Error"
                }
            }

        # Query similar embeddings
        query_results = self.vector_db_client.query_similar_embeddings(query_embedding, top_k=3)
        print(f"Pinecone Query Results: {query_results}")

        # Handle case when no similar interactions found
        if not query_results or not query_results.matches:
            general_response = {
                "sections": [{
                    "type": "main_response",
                    "content": "I'm here to help you with SBI Life insurance. How can I assist you today?"
                }]
            }
            return {"rag_response": {"formatted_response": general_response, "source": "No Similar Interactions"}}

        # Build context from similar interactions
        similar_interactions_context = [
            f"Similar interaction text: {match.metadata.get('text', 'No text')}, "
            f"Outcome: {match.metadata.get('outcome', 'No outcome')}"
            for match in query_results.matches
        ]
        context_string = "\n".join(similar_interactions_context)

        prompt = f"""You are an AI assistant for SBI Life Insurance.
            Generate a helpful and personalized response to the user's query based on the context from similar past customer interactions.

            User query: "{user_input_text}"

            Context from similar past interactions:
            {context_string}

            Provide your response in the following JSON structure WITHOUT ANY MARKDOWN FORMATTING:
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

            Return ONLY the JSON object, without any markdown formatting or code blocks.
            """

        try:
            openai_response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant for SBI Life Insurance. Format responses in structured JSON without markdown."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400
            )
            rag_response_text = openai_response.choices[0].message.content.strip()
            
            # Clean the response text before parsing
            cleaned_response_text = self.clean_json_response(rag_response_text)
            print(f"Cleaned response text: {cleaned_response_text}")
            
            formatted_response = json.loads(cleaned_response_text)
            print(f"Parsed JSON Response:\n{formatted_response}")

            return {
                "rag_response": {
                    "formatted_response": formatted_response,
                    "source": "RAG+OpenAI"
                }
            }
        except Exception as e:
            error_message = f"Error calling OpenAI API for RAG response: {e}"
            print(f"ERROR in get_rag_personalized_response (OpenAI call): {error_message}")
            return {
                "rag_response": {
                    "formatted_response": {
                        "sections": [{
                            "type": "main_response",
                            "content": "Sorry, I encountered an issue generating a personalized response."
                        }]
                    },
                    "source": "RAG+OpenAI Error"
                }
            }


if __name__ == '__main__':
    # Example Usage for testing
    recommender = RecommendationEngine()
    test_result = recommender.get_rag_personalized_response("TEST_USER_001", "Tell me about life insurance policies")
    print("Test result:", test_result)