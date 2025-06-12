"""
Database Service Layer for SBI Personalization Engine

This module provides high-level database operations that integrate with
both PostgreSQL (via MCP) and FAISS for vector operations.
"""
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

from src.database.postgres_mcp_server import (
    mcp_server, 
    mcp_execute_query, 
    mcp_insert_record, 
    mcp_get_customer_data,
    mcp_store_message
)
from src.vector_database.vector_db_client import VectorDBClient
from src.embedding_service.embedding_generator import EmbeddingGenerator

logger = logging.getLogger(__name__)

class DatabaseService:
    """
    High-level database service that coordinates between PostgreSQL and FAISS
    """
    
    def __init__(self):
        self.vector_db = VectorDBClient()
        self.embedding_generator = EmbeddingGenerator()
        self._initialized = False
    
    async def initialize(self):
        """Initialize the database service"""
        try:
            await mcp_server.initialize()
            self._initialized = True
            logger.info("Database service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize database service: {e}")
            return False
    
    def is_initialized(self):
        """Check if the service is initialized"""
        return self._initialized
    
    async def store_interaction(self, customer_id: str, interaction_text: str, 
                              interaction_type: str = "chatbot", 
                              user_language: str = 'en',
                              additional_metadata: Dict = None) -> Dict[str, Any]:
        """
        Store a user interaction in both PostgreSQL and FAISS
        
        This method:
        1. Generates embeddings for the interaction
        2. Stores the interaction in FAISS
        3. Stores structured data in PostgreSQL
        4. Returns the response from the recommendation engine
        """
        try:
            # Generate unique IDs
            conversation_turn_id = f"{customer_id}_{int(datetime.now().timestamp())}"
            conversation_id = f"CONVO_{customer_id}_{datetime.now().strftime('%Y%m%d')}"
            
            # Generate embedding for FAISS
            embedding = self.embedding_generator.get_embedding(
                interaction_text, 
                task_type="RETRIEVAL_DOCUMENT"
            )
            
            if not embedding:
                return {"success": False, "error": "Failed to generate embedding"}
            
            # Prepare metadata for FAISS
            faiss_metadata = {
                "customer_id": customer_id,
                "conversation_id": conversation_id,
                "timestamp": str(datetime.now()),
                "speaker": "customer",
                "text": interaction_text,
                "interaction_type": interaction_type,
                "language": user_language
            }
            
            if additional_metadata:
                faiss_metadata.update(additional_metadata)
            
            # Store in FAISS
            faiss_success = self.vector_db.upsert_embedding(
                conversation_turn_id, 
                embedding, 
                faiss_metadata
            )
            
            if not faiss_success:
                logger.warning(f"Failed to store interaction in FAISS: {conversation_turn_id}")
            
            # Store in PostgreSQL
            message_data = {
                "speaker": "customer",
                "message_text": interaction_text,
                "message_type": interaction_type,
                "language": user_language,
                "embedding_id": conversation_turn_id if faiss_success else None,
                "metadata": additional_metadata
            }
            
            postgres_result = await mcp_store_message(
                customer_id, 
                conversation_id, 
                message_data
            )
            
            # Log interaction
            await self._log_interaction(
                customer_id, 
                conversation_id, 
                interaction_type, 
                {
                    "text": interaction_text,
                    "language": user_language,
                    "faiss_stored": faiss_success,
                    "postgres_stored": postgres_result["success"]
                }
            )
            
            return {
                "success": True,
                "conversation_turn_id": conversation_turn_id,
                "conversation_id": conversation_id,
                "faiss_stored": faiss_success,
                "postgres_stored": postgres_result["success"]
            }
            
        except Exception as e:
            logger.error(f"Failed to store interaction: {e}")
            return {"success": False, "error": str(e)}
    
    async def store_response(self, customer_id: str, conversation_id: str, 
                           response_text: str, response_type: str = "assistant",
                           sentiment: str = None, additional_metadata: Dict = None) -> Dict[str, Any]:
        """Store an assistant response"""
        try:
            message_data = {
                "speaker": response_type,
                "message_text": response_text,
                "message_type": "response",
                "sentiment": sentiment,
                "metadata": additional_metadata
            }
            
            result = await mcp_store_message(customer_id, conversation_id, message_data)
            return result
            
        except Exception as e:
            logger.error(f"Failed to store response: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_customer_profile(self, customer_id: str) -> Dict[str, Any]:
        """Get comprehensive customer profile"""
        try:
            postgres_data = await mcp_get_customer_data(customer_id)
            
            if not postgres_data["success"]:
                return postgres_data
            
            # Get FAISS interaction history
            faiss_history = await self._get_faiss_interaction_history(customer_id)
            
            profile = postgres_data["rows"][0] if postgres_data["rows"] else {}
            profile["faiss_interaction_count"] = len(faiss_history)
            profile["faiss_interactions"] = faiss_history[-10:]  # Last 10 interactions
            
            return {"success": True, "profile": profile}
            
        except Exception as e:
            logger.error(f"Failed to get customer profile: {e}")
            return {"success": False, "error": str(e)}
    
    async def search_similar_interactions(self, customer_id: str, query_text: str, 
                                        top_k: int = 5) -> Dict[str, Any]:
        """Search for similar interactions using FAISS"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.get_embedding(
                query_text, 
                task_type="RETRIEVAL_QUERY"
            )
            
            if not query_embedding:
                return {"success": False, "error": "Failed to generate query embedding"}
            
            # Search FAISS
            faiss_results = self.vector_db.query_similar_embeddings(query_embedding, top_k)
            
            if not faiss_results or not faiss_results.get('matches'):
                return {"success": True, "matches": []}
            
            # Enrich with PostgreSQL data
            enriched_matches = []
            for match in faiss_results['matches']:
                enriched_match = match.copy()
                
                # Try to get related PostgreSQL data
                try:
                    if match.get('metadata', {}).get('conversation_id'):
                        conv_id = match['metadata']['conversation_id']
                        postgres_context = await self._get_conversation_context(conv_id)
                        enriched_match['postgres_context'] = postgres_context
                except Exception as e:
                    logger.warning(f"Failed to enrich match with PostgreSQL data: {e}")
                
                enriched_matches.append(enriched_match)
            
            return {
                "success": True, 
                "matches": enriched_matches,
                "query_text": query_text,
                "total_matches": len(enriched_matches)
            }
            
        except Exception as e:
            logger.error(f"Failed to search similar interactions: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_customer_preferences(self, customer_id: str, 
                                        preference_type: str, 
                                        preference_value: Any,
                                        confidence_score: float = 0.5) -> Dict[str, Any]:
        """Update customer preferences"""
        try:
            preference_data = {
                "customer_id": customer_id,
                "preference_type": preference_type,
                "preference_value": json.dumps(preference_value) if not isinstance(preference_value, str) else preference_value,
                "confidence_score": confidence_score
            }
            
            # Check if preference exists
            existing_query = """
                SELECT id FROM customer_preferences 
                WHERE customer_id = $1 AND preference_type = $2
            """
            existing = await mcp_execute_query(existing_query, [customer_id, preference_type])
            
            if existing["rows"]:
                # Update existing preference
                result = await mcp_server.update_record(
                    "customer_preferences",
                    "customer_id = $1 AND preference_type = $2",
                    [customer_id, preference_type],
                    {
                        "preference_value": preference_data["preference_value"],
                        "confidence_score": confidence_score
                    }
                )
            else:
                # Insert new preference
                result = await mcp_insert_record("customer_preferences", preference_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to update customer preferences: {e}")
            return {"success": False, "error": str(e)}
    
    async def store_document_processing(self, filename: str, content: str, 
                                      document_type: str = "brochure",
                                      chunks: List[Dict] = None) -> Dict[str, Any]:
        """Store processed document and its chunks"""
        try:
            document_id = f"doc_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"
            
            # Store document metadata
            document_data = {
                "document_id": document_id,
                "filename": filename,
                "document_type": document_type,
                "content_text": content,
                "chunk_count": len(chunks) if chunks else 0,
                "processing_status": "processed",
                "upload_source": "api_upload",
                "processed_at": datetime.now()
            }
            
            doc_result = await mcp_insert_record("documents", document_data)
            
            if not doc_result["success"]:
                return doc_result
            
            # Store chunks if provided
            if chunks:
                for i, chunk in enumerate(chunks):
                    chunk_data = {
                        "chunk_id": f"{document_id}_chunk_{i}",
                        "document_id": document_id,
                        "chunk_index": i,
                        "chunk_text": chunk.get("text", ""),
                        "chunk_metadata": json.dumps(chunk.get("metadata", {})),
                        "vector_id": chunk.get("vector_id")
                    }
                    
                    await mcp_insert_record("document_chunks", chunk_data)
            
            return {
                "success": True,
                "document_id": document_id,
                "chunks_stored": len(chunks) if chunks else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to store document processing: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_analytics_summary(self, customer_id: str = None, 
                                  days: int = 30) -> Dict[str, Any]:
        """Get analytics summary"""
        try:
            base_query = f"""
                SELECT 
                    COUNT(*) as total_interactions,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    AVG(CASE WHEN sentiment = 'Positive' THEN 1.0 
                             WHEN sentiment = 'Negative' THEN -1.0 
                             ELSE 0.0 END) as avg_sentiment,
                    COUNT(CASE WHEN sentiment = 'Positive' THEN 1 END) as positive_interactions,
                    COUNT(CASE WHEN sentiment = 'Negative' THEN 1 END) as negative_interactions,
                    COUNT(CASE WHEN sentiment = 'Neutral' THEN 1 END) as neutral_interactions
                FROM messages 
                WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '{days} day'
            """
            
            params = []
            if customer_id:
                base_query += " AND customer_id = $1"
                params.append(customer_id)
            
            result = await mcp_execute_query(base_query, params)
            
            if not result.get("success", False):
                return {"success": False, "error": result.get("error", "Query failed")}
            
            analytics_data = result.get("rows", [{}])[0] if result.get("rows") else {
                "total_interactions": 0,
                "unique_customers": 0,
                "avg_sentiment": 0.0,
                "positive_interactions": 0,
                "negative_interactions": 0,
                "neutral_interactions": 0
            }
            
            return {
                "success": True,
                "analytics": analytics_data,
                "period_days": days,
                "customer_id": customer_id
            }
            
        except Exception as e:
            logger.error(f"Failed to get analytics summary: {e}")
            return {"success": False, "error": str(e)}
    
    async def _log_interaction(self, customer_id: str, conversation_id: str, 
                             interaction_type: str, interaction_data: Dict):
        """Log user interaction for analytics"""
        try:
            interaction_record = {
                "interaction_id": str(uuid.uuid4()),
                "customer_id": customer_id,
                "conversation_id": conversation_id,
                "interaction_type": interaction_type,
                "interaction_data": json.dumps(interaction_data),
                "outcome": "successful"
            }
            
            await mcp_insert_record("user_interactions", interaction_record)
            
        except Exception as e:
            logger.warning(f"Failed to log interaction: {e}")
    
    async def _get_faiss_interaction_history(self, customer_id: str) -> List[Dict]:
        """Get interaction history from FAISS"""
        try:
            # This is a simplified implementation - in practice, you might want
            # to store customer-specific vectors or use metadata filtering
            return []  # Placeholder for now
        except Exception as e:
            logger.warning(f"Failed to get FAISS history: {e}")
            return []
    
    async def _get_conversation_context(self, conversation_id: str) -> Dict:
        """Get conversation context from PostgreSQL"""
        try:
            query = """
                SELECT c.title, c.status, COUNT(m.id) as message_count
                FROM conversations c
                LEFT JOIN messages m ON c.conversation_id = m.conversation_id
                WHERE c.conversation_id = $1
                GROUP BY c.id, c.title, c.status
            """
            
            result = await mcp_execute_query(query, [conversation_id])
            return result["rows"][0] if result["rows"] else {}
            
        except Exception as e:
            logger.warning(f"Failed to get conversation context: {e}")
            return {}

# Global database service instance
db_service = DatabaseService()

async def initialize_database_service():
    """Initialize the global database service"""
    return await db_service.initialize()

async def get_database_service() -> DatabaseService:
    """Get the database service instance"""
    if not db_service.is_initialized():
        await db_service.initialize()
    return db_service
