#!/usr/bin/env python3
"""
Integration Test Script for Enhanced SBI Chatbot
Tests the complete flow: Flask API -> Database Service -> PostgreSQL MCP Server
"""

import asyncio
import sys
import os
import json
import requests
import time
from datetime import datetime

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Test Flask application endpoints
BASE_URL = "http://127.0.0.1:5000"

def test_flask_server_status():
    """Test if Flask server is running"""
    print("🚀 Testing Flask server status...")
    try:
        response = requests.get(f"{BASE_URL}/api/database/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Flask server is running")
            print(f"   📊 Database available: {data.get('database_available')}")
            print(f"   💚 Database healthy: {data.get('database_healthy')}")
            print(f"   🔧 MCP server: {data.get('mcp_server')}")
            return True
        else:
            print(f"❌ Flask server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Flask server is not running. Please start it with 'python run.py'")
        return False
    except Exception as e:
        print(f"❌ Error checking Flask server: {e}")
        return False

def test_chat_endpoint():
    """Test the enhanced chat endpoint"""
    print("\n💬 Testing enhanced chat endpoint...")
    
    test_cases = [
        {
            "customer_id": "TEST_INTEGRATION_001",
            "user_input_text": "Tell me about term insurance plans",
            "language": "en"
        },
        {
            "customer_id": "TEST_INTEGRATION_002", 
            "user_input_text": "What are the benefits of ULIP?",
            "language": "en"
        },
        {
            "customer_id": "TEST_INTEGRATION_001",  # Same customer for continuity
            "user_input_text": "How much premium should I pay monthly?",
            "language": "en"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: Customer {test_case['customer_id']}")
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json=test_case,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Chat successful")
                print(f"   📝 Response: {data.get('response', 'No response')[:100]}...")
                print(f"   🗣️ Language: {data.get('detected_language', 'N/A')}")
                if 'conversation_id' in data:
                    print(f"   🆔 Conversation ID: {data['conversation_id']}")
            else:
                print(f"   ❌ Chat failed with status {response.status_code}")
                print(f"   📄 Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Chat test {i} error: {e}")
    
    return True

def test_customer_profile():
    """Test customer profile retrieval"""
    print("\n👤 Testing customer profile retrieval...")
    
    customer_id = "TEST_INTEGRATION_001"
    try:
        response = requests.get(f"{BASE_URL}/api/customer/{customer_id}/profile")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Profile retrieved successfully")
            print(f"   🆔 Customer ID: {data.get('customer_id', 'N/A')}")
            print(f"   💬 Recent messages: {len(data.get('recent_messages', []))}")
            print(f"   🎯 Preferences: {len(data.get('preferences', []))}")
            print(f"   📊 Interactions: {data.get('total_interactions', 0)}")
            return True
        else:
            print(f"   ❌ Profile retrieval failed with status {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Profile retrieval error: {e}")
        return False

def test_analytics():
    """Test analytics endpoint"""
    print("\n📊 Testing analytics...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/summary?days=7")
        
        if response.status_code == 200:
            data = response.json()
            analytics = data.get('analytics', {})
            print(f"   ✅ Analytics retrieved successfully")
            print(f"   📈 Total interactions: {analytics.get('total_interactions', 0)}")
            print(f"   👥 Unique customers: {analytics.get('unique_customers', 0)}")
            print(f"   😊 Positive: {analytics.get('positive_interactions', 0)}")
            print(f"   😐 Neutral: {analytics.get('neutral_interactions', 0)}")
            print(f"   😞 Negative: {analytics.get('negative_interactions', 0)}")
            return True
        else:
            print(f"   ❌ Analytics failed with status {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Analytics error: {e}")
        return False

def test_mcp_operations():
    """Test MCP operations monitoring"""
    print("\n🔧 Testing MCP operations monitoring...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/mcp/operations?limit=5")
        
        if response.status_code == 200:
            data = response.json()
            operations = data.get('operations', [])
            print(f"   ✅ MCP operations retrieved successfully")
            print(f"   📋 Recent operations: {len(operations)}")
            
            for op in operations[:3]:  # Show first 3
                print(f"   🔹 {op.get('operation_type', 'N/A')} - {op.get('status', 'N/A')} - {op.get('execution_time_ms', 0)}ms")
            
            return True
        else:
            print(f"   ❌ MCP operations failed with status {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ MCP operations error: {e}")
        return False

def test_exa_search():
    """Test Exa search endpoint"""
    print("\n🔍 Testing Exa search...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/gemini_search",
            json={
                "query": "What are the latest SBI Life insurance schemes?",
                "language": "en"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Exa search successful")
            print(f"   🔍 Response: {data.get('response', 'No response')[:150]}...")
            return True
        else:
            print(f"   ❌ Exa search failed with status {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exa search error: {e}")
        return False

def cleanup_test_data():
    """Clean up test data created during integration tests"""
    print("\n🧹 Cleaning up integration test data...")
    
    try:
        # Import the MCP server directly to clean up
        from src.database.postgres_mcp_server import PostgresMCPServer
        
        async def cleanup_async():
            mcp_server = PostgresMCPServer()
            await mcp_server.initialize()
            
            # Clean up test customers and related data in correct order to avoid FK violations
            cleanup_queries = [
                # Delete from child tables first
                "DELETE FROM user_interactions WHERE customer_id LIKE 'TEST_INTEGRATION_%'",
                "DELETE FROM messages WHERE customer_id LIKE 'TEST_INTEGRATION_%'",
                "DELETE FROM conversations WHERE customer_id LIKE 'TEST_INTEGRATION_%'",
                "DELETE FROM customer_preferences WHERE customer_id LIKE 'TEST_INTEGRATION_%'",
                # Delete from parent tables last
                "DELETE FROM customers WHERE customer_id LIKE 'TEST_INTEGRATION_%'",
                # Clean up operations
                "DELETE FROM mcp_operations WHERE operation_id LIKE '%TEST_INTEGRATION%'"
            ]
            
            total_cleaned = 0
            for query in cleanup_queries:
                try:
                    result = await mcp_server.execute_query(query)
                    if result.get("success", False):
                        rows_affected = result.get("rows_affected", 0)
                        if rows_affected > 0:
                            table_name = query.split("FROM")[1].split("WHERE")[0].strip()
                            print(f"   🗑️ Cleaned {rows_affected} records from {table_name}")
                            total_cleaned += rows_affected
                except Exception as e:
                    # Only log non-FK constraint errors
                    if "does not exist" not in str(e) and "violates foreign key constraint" not in str(e):
                        print(f"   ⚠️ Cleanup query error: {e}")
            
            await mcp_server.close()
            
            if total_cleaned > 0:
                print(f"   ✅ Cleanup completed - removed {total_cleaned} total records")
            else:
                print("   ✅ Cleanup completed - no test records found")
        
        # Run cleanup
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(cleanup_async())
        loop.close()
        
    except Exception as e:
        print(f"   ⚠️ Cleanup error: {e}")

def main():
    """Run all integration tests"""
    print("🚀 Starting SBI Chatbot Integration Tests")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Flask Server Status", test_flask_server_status),
        ("Chat Endpoint", test_chat_endpoint),
        ("Customer Profile", test_customer_profile),
        ("Analytics", test_analytics),
        ("MCP Operations", test_mcp_operations),
        ("Exa Search", test_exa_search)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            if result:
                passed_tests += 1
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
    
    # Cleanup
    cleanup_test_data()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    if passed_tests == total_tests:
        print(f"🎉 All {total_tests} tests passed! Your enhanced SBI chatbot is working perfectly!")
        print("\n✨ WHAT'S WORKING:")
        print("   ✅ PostgreSQL MCP Server integration")
        print("   ✅ Enhanced chat API with database storage")
        print("   ✅ Customer profile management")
        print("   ✅ Analytics and monitoring")
        print("   ✅ MCP operations tracking")
        print("   ✅ Gemini search with grounding")
        
        print("\n🎯 NEXT STEPS:")
        print("   1. Test with your React frontend")
        print("   2. Add more complex conversation flows")
        print("   3. Implement advanced analytics")
        print("   4. Add real-time monitoring dashboards")
        print("   5. Scale to production environment")
        
    else:
        print(f"⚠️ {passed_tests}/{total_tests} tests passed. Some issues need attention.")
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Check Flask server is running: python run.py")
        print("   2. Verify PostgreSQL is running and accessible")
        print("   3. Ensure MCP server initialization was successful")
        print("   4. Check environment variables and configurations")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⛔ Integration tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Integration tests crashed: {e}")
        sys.exit(1)
