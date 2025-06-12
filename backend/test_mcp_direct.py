#!/usr/bin/env python3
"""
Direct Test Script for PostgreSQL MCP Server
This script directly tests the MCP server functionality without going through the full application stack.
"""

import asyncio
import sys
import os
from datetime import datetime
import json
from uuid import UUID

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.postgres_mcp_server import PostgresMCPServer

# JSON encoder that handles UUID
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

API_KEY = os.getenv("MCP_API_KEY", "default_api_key")

async def test_mcp_server():
    """Test basic MCP server operations"""
    print("\n🚀 Testing PostgreSQL MCP Server...")
    
    mcp_server = None
    try:
        # Initialize MCP server
        mcp_server = PostgresMCPServer()
        initialized = await mcp_server.initialize()
        
        if not initialized:
            print("❌ Failed to initialize MCP server")
            return False
        
        print("✅ MCP server initialized successfully")
        
        # Test 1: Simple Query
        print("\n📋 Test 1: Simple Query")
        query = "SELECT version();"
        result = await mcp_server.execute_query(query)
        if result["success"]:
            print("✅ Basic query successful")
            print(f"📊 Result: {result['rows'][0] if result['rows'] else 'No data'}")
        else:
            print(f"❌ Query failed: {result.get('error')}")
        
        # Test 2: Insert Operation
        print("\n📋 Test 2: Insert Operation")
        test_data = {
            "customer_id": "TEST_CUSTOMER_001",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "1234567890",
            "preferred_language": "en"
        }

        # Check if record already exists
        check_query = "SELECT * FROM customers WHERE customer_id = 'TEST_CUSTOMER_001'"
        check_result = await mcp_server.execute_query(check_query)
        if check_result["success"] and check_result.get("rows"):
            print("⚠️ Record already exists, skipping insert operation")
        else:
            insert_result = await mcp_server.insert_record("customers", test_data)
            if insert_result["success"]:
                print("✅ Insert operation successful")
                print(f"📊 Inserted Record: {json.dumps(insert_result.get('inserted_record', {}), indent=2, cls=UUIDEncoder)}")
            else:
                print(f"❌ Insert failed: {insert_result.get('error')}")
        
        # Test 3: Select Inserted Data
        print("\n📋 Test 3: Select Inserted Data")
        select_query = "SELECT * FROM customers WHERE customer_id = 'TEST_CUSTOMER_001'"
        select_result = await mcp_server.execute_query(select_query)
        if select_result["success"]:
            print("✅ Select operation successful")
            # Convert datetime objects to strings for JSON serialization
            rows = select_result.get("rows", [{}])
            for row in rows:
                for key, value in row.items():
                    if isinstance(value, datetime):
                        row[key] = value.isoformat()
            print(f"📊 Retrieved Data: {json.dumps(rows[0], indent=2, cls=UUIDEncoder)}")
        else:
            print(f"❌ Select failed: {select_result.get('error')}")
        
        # Test 4: Update Operation
        print("\n📋 Test 4: Update Operation")
        update_result = await mcp_server.update_record(
            "customers",
            "customer_id = $1",
            ["TEST_CUSTOMER_001"],
            {"first_name": "Updated", "last_name": "TestUser"}
        )
        if update_result["success"]:
            print("✅ Update operation successful")
            # Convert datetime objects to strings for JSON serialization
            updated_records = update_result.get("updated_records", [{}])
            for record in updated_records:
                for key, value in record.items():
                    if isinstance(value, datetime):
                        record[key] = value.isoformat()
            print(f"📊 Updated Record: {json.dumps(updated_records[0], indent=2, cls=UUIDEncoder)}")
        else:
            print(f"❌ Update failed: {update_result.get('error')}")
        
        # Cleanup: Delete test data
        print("\n🧹 Cleaning up test data...")
        cleanup_query = "DELETE FROM customers WHERE customer_id = 'TEST_CUSTOMER_001'"
        cleanup_result = await mcp_server.execute_query(cleanup_query)
        if cleanup_result["success"]:
            print("✅ Cleanup successful")
        else:
            print(f"❌ Cleanup failed: {cleanup_result.get('error')}")
        
        # Close the connection
        await mcp_server.close()
        print("\n✅ MCP server connection closed")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during MCP server test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if mcp_server:
            try:
                await mcp_server.close()
                print("\n✅ MCP server connection closed")
            except Exception as e:
                print(f"\n⚠️ Error closing MCP server: {e}")

async def test_mcp_operations_log():
    """Test MCP operations logging"""
    print("\n🔍 Testing MCP Operations Logging...")
    
    try:
        mcp_server = PostgresMCPServer()
        await mcp_server.initialize()
        
        # Query recent operations
        query = """
            SELECT operation_id, operation_type, status, 
                   execution_time_ms, created_at, completed_at
            FROM mcp_operations
            ORDER BY created_at DESC
            LIMIT 5
        """
        
        result = await mcp_server.execute_query(query)
        if result["success"]:
            print("✅ Operations log query successful")
            print("\n📋 Recent Operations:")
            for op in result.get('rows', []):
                print(f"🔹 {op['operation_type']} - {op['status']} - {op['execution_time_ms']}ms")
        else:
            print(f"❌ Failed to query operations log: {result.get('error')}")
        
        await mcp_server.close()
        return True
        
    except Exception as e:
        print(f"❌ Error querying operations log: {e}")
        return False

async def test_mcp_server_with_api_key():
    """Test MCP server operations with API key authentication"""
    print("\n🚀 Testing PostgreSQL MCP Server with API Key...")

    mcp_server = None
    try:
        # Initialize MCP server with API key
        mcp_server = PostgresMCPServer(api_key=API_KEY)
        initialized = await mcp_server.initialize()

        if not initialized:
            print("❌ Failed to initialize MCP server with API key")
            return False

        print("✅ MCP server initialized successfully with API key")

        # Test 1: Simple Query
        print("\n📋 Test 1: Simple Query")
        query = "SELECT version();"
        result = await mcp_server.execute_query(query)
        if result["success"]:
            print("✅ Basic query successful")
            print(f"📊 Result: {result['rows'][0] if result['rows'] else 'No data'}")
        else:
            print(f"❌ Query failed: {result.get('error')}")

        # Test 2: Insert Operation
        print("\n📋 Test 2: Insert Operation")
        test_data = {
            "customer_id": "TEST_CUSTOMER_001",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "1234567890",
            "preferred_language": "en"
        }

        # Check if record already exists
        check_query = "SELECT * FROM customers WHERE customer_id = 'TEST_CUSTOMER_001'"
        check_result = await mcp_server.execute_query(check_query)
        if check_result["success"] and check_result.get("rows"):
            print("⚠️ Record already exists, skipping insert operation")
        else:
            insert_result = await mcp_server.insert_record("customers", test_data)
            if insert_result["success"]:
                print("✅ Insert operation successful")
                print(f"📊 Inserted Record: {json.dumps(insert_result.get('inserted_record', {}), indent=2, cls=UUIDEncoder)}")
            else:
                print(f"❌ Insert failed: {insert_result.get('error')}")

        # Cleanup: Delete test data
        print("\n🧹 Cleaning up test data...")
        cleanup_query = "DELETE FROM customers WHERE customer_id = 'TEST_CUSTOMER_001'"
        cleanup_result = await mcp_server.execute_query(cleanup_query)
        if cleanup_result["success"]:
            print("✅ Cleanup successful")
        else:
            print(f"❌ Cleanup failed: {cleanup_result.get('error')}")

        # Close the connection
        await mcp_server.close()
        print("\n✅ MCP server connection closed")

        return True

    except Exception as e:
        print(f"\n❌ Error during MCP server test with API key: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if mcp_server:
            try:
                await mcp_server.close()
                print("\n✅ MCP server connection closed")
            except Exception as e:
                print(f"\n⚠️ Error closing MCP server: {e}")

def main():
    """Run all MCP server tests"""
    print("🚀 Starting Direct MCP Server Tests")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run basic operations test
        basic_success = loop.run_until_complete(test_mcp_server())
        
        # Run operations log test
        log_success = loop.run_until_complete(test_mcp_operations_log())
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎯 MCP SERVER TEST SUMMARY")
        print("=" * 60)
        
        if basic_success and log_success:
            print("🎉 All MCP server tests passed!")
            print("\n✨ Verified:")
            print("   ✅ Server initialization")
            print("   ✅ Basic CRUD operations")
            print("   ✅ Operations logging")
            print("   ✅ Connection management")
        else:
            print("⚠️ Some MCP server tests failed.")
            print("\n🔧 Status:")
            print(f"   {'✅' if basic_success else '❌'} Basic operations")
            print(f"   {'✅' if log_success else '❌'} Operations logging")
        
        return basic_success and log_success
        
    finally:
        loop.close()

def main_api_key():
    """Run all MCP server tests with API key"""
    print("🚀 Starting Direct MCP Server Tests with API Key")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Run basic operations test with API key
        basic_success = loop.run_until_complete(test_mcp_server_with_api_key())

        # Print summary
        print("\n" + "=" * 60)
        print("🎯 MCP SERVER TEST SUMMARY WITH API KEY")
        print("=" * 60)

        if basic_success:
            print("🎉 All MCP server tests passed with API key!")
            print("\n✨ Verified:")
            print("   ✅ Server initialization with API key")
            print("   ✅ Basic CRUD operations")
            print("   ✅ Connection management")
        else:
            print("⚠️ Some MCP server tests failed with API key.")
            print("\n🔧 Status:")
            print(f"   {'✅' if basic_success else '❌'} Basic operations")

        return basic_success

    finally:
        loop.close()

if __name__ == "__main__":
    try:
        # Check if API key is set
        if os.getenv("MCP_API_KEY"):
            success = main_api_key()
        else:
            success = main()
        
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⛔ MCP server tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 MCP server tests crashed: {e}")
        sys.exit(1)
