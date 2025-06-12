#!/usr/bin/env python3
"""
Test script for PostgreSQL MCP Server setup
This script tests the MCP server functionality and database connectivity.
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import our MCP components
try:
    from src.database.postgres_mcp_server import PostgresMCPServer, initialize_mcp_server
    from src.database.database_service import DatabaseService, get_database_service
    from src.config.config import DATABASE_URL, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER
    print("✅ Successfully imported MCP components")
except ImportError as e:
    print(f"❌ Failed to import MCP components: {e}")
    sys.exit(1)

async def test_basic_connection():
    """Test basic PostgreSQL connection"""
    print("\n🔗 Testing basic PostgreSQL connection...")
    
    try:
        mcp_server = PostgresMCPServer()
        success = await mcp_server.initialize()
        
        if success:
            print("✅ PostgreSQL MCP Server initialized successfully")
            
            # Test a simple query
            result = await mcp_server.execute_query("SELECT version() as version, current_timestamp as time")
            if result["success"]:
                version = result["rows"][0]["version"]
                timestamp = result["rows"][0]["time"]
                print(f"✅ Database query successful")
                print(f"   📊 Version: {version[:50]}...")
                print(f"   🕐 Time: {timestamp}")
            else:
                print(f"❌ Database query failed: {result.get('error')}")
                return False
            
            await mcp_server.close()
            return True
        else:
            print("❌ Failed to initialize PostgreSQL MCP Server")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

async def test_table_operations():
    """Test basic table operations"""
    print("\n📋 Testing table operations...")
    
    try:
        mcp_server = PostgresMCPServer()
        await mcp_server.initialize()
        
        # Generate unique test customer ID with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_customer_id = f"TEST_MCP_{timestamp}"
        
        # Test customer creation
        print("   👤 Testing customer creation...")
        customer_data = {
            "customer_id": test_customer_id,
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.doe.{timestamp}@test.com",
            "preferred_language": "en"
        }
        
        result = await mcp_server.insert_record("customers", customer_data)
        if result["success"]:
            print("   ✅ Customer created successfully")
            customer_id = result["inserted_record"]["id"]
            print(f"   🆔 Customer UUID: {customer_id}")
        else:
            print(f"   ❌ Customer creation failed: {result.get('error')}")
            await mcp_server.close()
            return False
        
        # Test customer retrieval
        print("   🔍 Testing customer retrieval...")
        query_result = await mcp_server.execute_query(
            "SELECT * FROM customers WHERE customer_id = $1", 
            [test_customer_id]
        )
        
        if query_result["success"] and query_result["rows"]:
            customer = query_result["rows"][0]
            print("   ✅ Customer retrieved successfully")
            print(f"   📧 Email: {customer['email']}")
            print(f"   🏷️ Language: {customer['preferred_language']}")
        else:
            print("   ❌ Customer retrieval failed")
            await mcp_server.close()
            return False
        
        # Test conversation creation
        print("   💬 Testing conversation creation...")
        conversation_data = {
            "conversation_id": f"CONV_{timestamp}",
            "customer_id": test_customer_id,
            "title": "Test Conversation",
            "status": "active"
        }
        
        conv_result = await mcp_server.insert_record("conversations", conversation_data)
        if conv_result["success"]:
            print("   ✅ Conversation created successfully")
        else:
            print(f"   ❌ Conversation creation failed: {conv_result.get('error')}")
        
        # Test message storage
        print("   📝 Testing message storage...")
        message_data = {
            "message_id": f"MSG_{timestamp}",
            "conversation_id": f"CONV_{timestamp}",
            "customer_id": test_customer_id,
            "speaker": "customer",
            "message_text": "Hello, I need help with insurance plans",
            "message_type": "chatbot",
            "sentiment": "Neutral",
            "language": "en"
        }
        
        msg_result = await mcp_server.store_conversation_message(test_customer_id, f"CONV_{timestamp}", message_data)
        if msg_result["success"]:
            print("   ✅ Message stored successfully")
        else:
            print(f"   ❌ Message storage failed: {msg_result.get('error')}")
        
        await mcp_server.close()
        return True
        
    except Exception as e:
        print(f"❌ Table operations test failed: {e}")
        return False

async def test_database_service():
    """Test the high-level database service"""
    print("\n🔧 Testing Database Service...")
    
    try:
        db_service = await get_database_service()
        
        # Generate unique test customer ID with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_customer_id = f"TEST_MCP_SVC_{timestamp}"
        
        # Test interaction storage
        print("   💾 Testing interaction storage...")
        result = await db_service.store_interaction(
            customer_id=test_customer_id,
            interaction_text="Tell me about term insurance",
            interaction_type="chatbot",
            user_language="en",
            additional_metadata={"test_run": True}
        )
        
        if result["success"]:
            print("   ✅ Interaction stored successfully")
            print(f"   🆔 Conversation ID: {result['conversation_id']}")
            print(f"   📊 FAISS stored: {result['faiss_stored']}")
            print(f"   🗄️ PostgreSQL stored: {result['postgres_stored']}")
        else:
            print(f"   ❌ Interaction storage failed: {result.get('error')}")
            return False
        
        # Test customer profile retrieval
        print("   👤 Testing customer profile retrieval...")
        profile_result = await db_service.get_customer_profile(test_customer_id)
        
        if profile_result["success"]:
            print("   ✅ Customer profile retrieved successfully")
            profile = profile_result["profile"]
            print(f"   📧 Customer ID: {profile.get('customer_id', 'N/A')}")
            print(f"   💬 Messages: {len(profile.get('recent_messages', []))}")
        else:
            print(f"   ❌ Profile retrieval failed: {profile_result.get('error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database service test failed: {e}")
        return False

async def test_analytics():
    """Test analytics functionality"""
    print("\n📊 Testing Analytics...")
    
    try:
        db_service = await get_database_service()
        
        # Get analytics summary
        analytics_result = await db_service.get_analytics_summary(days=7)
        
        if analytics_result["success"]:
            print("   ✅ Analytics retrieved successfully")
            analytics = analytics_result["analytics"]
            print(f"   📈 Total interactions: {analytics.get('total_interactions', 0)}")
            print(f"   👥 Unique customers: {analytics.get('unique_customers', 0)}")
            print(f"   😊 Positive interactions: {analytics.get('positive_interactions', 0)}")
            print(f"   😐 Neutral interactions: {analytics.get('neutral_interactions', 0)}")
            print(f"   😞 Negative interactions: {analytics.get('negative_interactions', 0)}")
        else:
            print(f"   ❌ Analytics failed: {analytics_result.get('error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
        return False

async def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        mcp_server = PostgresMCPServer()
        await mcp_server.initialize()
        
        # Get the correct table name for messages
        # Check if 'messages' or 'conversation_messages' table exists
        table_check = await mcp_server.execute_query("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('messages', 'conversation_messages')
        """)
        
        message_table = "messages"  # default
        if table_check["success"] and table_check["rows"]:
            available_tables = [row["table_name"] for row in table_check["rows"]]
            if "conversation_messages" in available_tables:
                message_table = "conversation_messages"
            elif "messages" in available_tables:
                message_table = "messages"
        
        # Delete in correct order to avoid foreign key constraints
        # First delete messages, then conversations, then customers
        cleanup_queries = [
            # Delete test messages first (using correct table name)
            f"DELETE FROM {message_table} WHERE customer_id LIKE 'TEST_MCP_%'",
            # Delete test conversations second
            "DELETE FROM conversations WHERE customer_id LIKE 'TEST_MCP_%'", 
            # Delete test customers last
            "DELETE FROM customers WHERE customer_id LIKE 'TEST_MCP_%'",
            # Clean up MCP operations
            "DELETE FROM mcp_operations WHERE operation_id LIKE '%TEST%'"
        ]
        
        cleanup_count = 0
        for query in cleanup_queries:
            try:
                result = await mcp_server.execute_query(query)
                if result["success"]:
                    rows_affected = result.get("rows_affected", 0)
                    if rows_affected > 0:
                        table_name = query.split("FROM")[1].split("WHERE")[0].strip()
                        print(f"   🗑️ Cleaned up {rows_affected} records from {table_name}")
                        cleanup_count += rows_affected
                else:
                    error_msg = result.get('error', 'Unknown error')
                    if "does not exist" not in error_msg and "violates foreign key constraint" not in error_msg:
                        print(f"   ⚠️ Cleanup query failed: {error_msg}")
            except Exception as e:
                error_str = str(e)
                if "does not exist" not in error_str and "violates foreign key constraint" not in error_str:
                    print(f"   ⚠️ Cleanup query error: {e}")
        
        if cleanup_count > 0:
            print(f"   ✅ Test data cleanup completed - removed {cleanup_count} total records")
        else:
            print("   ✅ Test data cleanup completed - no test records found")
        await mcp_server.close()
        
    except Exception as e:
        print(f"   ⚠️ Cleanup warning: {e}")

async def main():
    """Main test function"""
    print("🚀 Starting PostgreSQL MCP Server Tests")
    print(f"📍 Database: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    print(f"👤 User: {POSTGRES_USER}")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run tests
    tests = [
        ("Basic Connection", test_basic_connection),
        ("Table Operations", test_table_operations),
        ("Database Service", test_database_service),
        ("Analytics", test_analytics)
    ]
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            if not result:
                all_tests_passed = False
                print(f"❌ {test_name} test failed")
            else:
                print(f"✅ {test_name} test passed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            all_tests_passed = False
    
    # Cleanup
    await cleanup_test_data()
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 All tests passed! PostgreSQL MCP Server is working correctly.")
        print("\n📋 Next steps:")
        print("   1. Update your recommendation engine to use the database service")
        print("   2. Test with your existing Flask application")
        print("   3. Monitor MCP operations in the 'mcp_operations' table")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Verify database connection settings in .env")
        print("   2. Check PostgreSQL service status")
        print("   3. Ensure all dependencies are installed")
    
    return all_tests_passed

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⛔ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test script crashed: {e}")
        sys.exit(1)
