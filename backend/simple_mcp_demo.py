#!/usr/bin/env python3
"""
Simple MCP Insert and Retrieve Demo
This script demonstrates adding values to tables and retrieving them using MCP.
"""

import asyncio
import sys
import os
import json
from datetime import datetime
import uuid
import random

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.postgres_mcp_server import PostgresMCPServer

# JSON encoder that handles various types
class CompleteJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)

async def run_mcp_demo():
    """Run a simple MCP insert and retrieve demo"""
    print("\n🚀 Starting Simple MCP Demo...")
    
    mcp_server = None
    try:
        # Initialize MCP server
        mcp_server = PostgresMCPServer()
        initialized = await mcp_server.initialize()
        
        if not initialized:
            print("❌ Failed to initialize MCP server")
            return False
        
        print("✅ MCP server initialized successfully")
        
        # Generate test data
        customer_id = f"TEST_USER_{random.randint(1000, 9999)}"
        print(f"\n📝 Creating test customer with ID: {customer_id}")
        
        # 1. Insert customer
        customer_data = {
            "customer_id": customer_id,
            "first_name": "Test",
            "last_name": "User",
            "email": f"{customer_id.lower()}@example.com",
            "phone": f"+1{random.randint(1000000000, 9999999999)}",
            "preferred_language": "en"
        }
        
        result = await mcp_server.insert_record("customers", customer_data)
        
        if result["success"]:
            print("✅ Customer created successfully")
            
            # Convert the record for JSON serialization
            record_dict = {}
            for k, v in result["inserted_record"].items():
                if isinstance(v, (datetime, uuid.UUID)):
                    record_dict[k] = str(v)
                else:
                    record_dict[k] = v
                    
            print(f"📊 Customer Record: {json.dumps(record_dict, indent=2)}")
        else:
            print(f"❌ Failed to create customer: {result.get('error')}")
            return False
        
        # 2. Query the inserted data
        print(f"\n🔍 Retrieving customer data for ID: {customer_id}")
        
        query = "SELECT * FROM customers WHERE customer_id = $1"
        result = await mcp_server.execute_query(query, [customer_id])
        
        if result["success"] and result["rows"]:
            print("✅ Successfully retrieved customer data")
            
            # Convert the row for JSON serialization
            row_dict = {}
            for k, v in result["rows"][0].items():
                if isinstance(v, (datetime, uuid.UUID)):
                    row_dict[k] = str(v)
                else:
                    row_dict[k] = v
                    
            print(f"📊 Retrieved Data: {json.dumps(row_dict, indent=2)}")
        else:
            print(f"❌ Failed to retrieve customer: {result.get('error')}")
        
        # 3. Clean up
        print("\n🧹 Cleaning up test data...")
        
        cleanup_result = await mcp_server.execute_query(
            "DELETE FROM customers WHERE customer_id = $1 RETURNING customer_id",
            [customer_id]
        )
        
        if cleanup_result["success"]:
            print(f"✅ Successfully deleted test customer")
        else:
            print(f"❌ Failed to delete test data: {cleanup_result.get('error')}")
        
        await mcp_server.close()
        print("\n✅ MCP server connection closed")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        if mcp_server:
            try:
                await mcp_server.close()
            except:
                pass

if __name__ == "__main__":
    print(f"🚀 Simple MCP Insert & Retrieve Demo")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    loop = asyncio.get_event_loop()
    try:
        success = loop.run_until_complete(run_mcp_demo())
        sys.exit(0 if success else 1)
    finally:
        loop.close()
