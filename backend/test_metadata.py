#!/usr/bin/env python3
"""
Test Script for Metadata Generation and Storage in RecommendationEngine
Tests the metadata structure, FAISS storage, and MCP server integration
"""

import sys
import os
import asyncio
import json
from datetime import datetime
import pandas as pd

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from personalization_engine.recommendation_engine import RecommendationEngine
from database.postgres_mcp_server import PostgresMCPServer
from database.database_service import get_database_service

def test_metadata_structure():
    """Test the structure and content of generated metadata"""
    print("\n🔍 Testing Metadata Structure...")
    
    recommender = RecommendationEngine()
    customer_id = "TEST_METADATA_001"
    interaction_text = "Tell me about term insurance plans"
    interaction_type = "chatbot"
    conversation_turn_id = f"{customer_id}_{int(pd.Timestamp.now().timestamp())}"
    
    # Test basic FAISS metadata
    embedding = recommender.embedding_generator.get_embedding(interaction_text, task_type="RETRIEVAL_DOCUMENT")
    if embedding is None:
        print("❌ Failed to generate embedding")
        return False
    
    metadata = {
        "customer_id": customer_id,
        "conversation_id": f"TEST_CONVO_{int(pd.Timestamp.now().timestamp())}",
        "timestamp": str(pd.Timestamp.now()),
        "speaker": "customer",
        "text": interaction_text,
        "interaction_type": interaction_type,
        "source": "test_metadata",
        "outcome": "metadata_test"
    }
    
    # Test FAISS storage
    success = recommender.vector_db_client.upsert_embedding(conversation_turn_id, embedding, metadata)
    if success:
        print("✅ Metadata stored in FAISS successfully")
    else:
        print("❌ Failed to store metadata in FAISS")
        return False
    
    # Query back the stored metadata
    query_embedding = recommender.embedding_generator.get_embedding(interaction_text, task_type="RETRIEVAL_QUERY")
    query_results = recommender.vector_db_client.query_similar_embeddings(query_embedding, top_k=1)
    
    if query_results and query_results.get('matches'):
        retrieved_metadata = query_results['matches'][0].get('metadata', {})
        print("\n📋 Retrieved Metadata:")
        print(json.dumps(retrieved_metadata, indent=2))
        
        # Verify metadata fields
        required_fields = ["customer_id", "conversation_id", "timestamp", "speaker", "text", "interaction_type"]
        missing_fields = [field for field in required_fields if field not in retrieved_metadata]
        
        if missing_fields:
            print(f"❌ Missing required metadata fields: {missing_fields}")
            return False
        else:
            print("✅ All required metadata fields present")
            return True
    else:
        print("❌ Failed to retrieve metadata from FAISS")
        return False

async def test_mcp_metadata_storage():
    """Test metadata storage in PostgreSQL MCP server"""
    print("\n🔍 Testing MCP Metadata Storage...")
    
    try:
        # Initialize MCP server
        mcp_server = PostgresMCPServer()
        await mcp_server.initialize()
        
        # Get database service
        db_service = await get_database_service()
        
        # Test customer data
        customer_id = "TEST_METADATA_001"
        interaction_text = "What are the benefits of Smart Swadhan Plus?"
        
        # Store interaction with metadata
        result = await db_service.store_interaction(
            customer_id=customer_id,
            interaction_text=interaction_text,
            interaction_type="metadata_test",
            user_language="en",
            additional_metadata={
                "test_id": "MCP_TEST_001",
                "source": "metadata_test",
                "outcome": "test_storage"
            }
        )
        
        if result["success"]:
            print("✅ Interaction stored in MCP server successfully")
            print("\n📋 Stored Data:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Failed to store interaction in MCP: {result.get('error')}")
        
        # Clean up test data
        cleanup_queries = [
            "DELETE FROM user_interactions WHERE customer_id = 'TEST_METADATA_001'",
            "DELETE FROM messages WHERE customer_id = 'TEST_METADATA_001'",
            "DELETE FROM conversations WHERE customer_id = 'TEST_METADATA_001'"
        ]
        
        for query in cleanup_queries:
            await mcp_server.execute_query(query)
        
        await mcp_server.close()
        return result["success"]
        
    except Exception as e:
        print(f"❌ Error in MCP metadata test: {e}")
        return False

def main():
    """Run all metadata tests"""
    print("🚀 Starting Metadata Integration Tests")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test metadata structure and FAISS storage
    faiss_success = test_metadata_structure()
    
    # Test MCP metadata storage
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mcp_success = loop.run_until_complete(test_mcp_metadata_storage())
    loop.close()
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 METADATA TEST SUMMARY")
    print("=" * 60)
    
    if faiss_success and mcp_success:
        print("🎉 All metadata tests passed!")
        print("\n✨ Verified:")
        print("   ✅ Metadata structure generation")
        print("   ✅ FAISS storage and retrieval")
        print("   ✅ MCP server integration")
        print("   ✅ Required fields present")
    else:
        print("⚠️ Some metadata tests failed.")
        print("\n🔧 Status:")
        print(f"   {'✅' if faiss_success else '❌'} FAISS metadata tests")
        print(f"   {'✅' if mcp_success else '❌'} MCP metadata tests")
    
    return faiss_success and mcp_success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⛔ Metadata tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Metadata tests crashed: {e}")
        sys.exit(1)
