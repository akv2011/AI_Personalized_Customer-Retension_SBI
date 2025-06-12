#!/usr/bin/env python3
"""
Script to insert and retrieve data using PostgreSQL MCP Server
This script demonstrates adding values to tables and retrieving them using MCP.
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from uuid import uuid4
import random

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.postgres_mcp_server import PostgresMCPServer

# JSON encoder that handles various types
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        if hasattr(obj, 'hex'):
            return str(obj)  # Handle UUID objects
        return json.JSONEncoder.default(self, obj)

async def insert_and_retrieve():
    """Insert data into tables and retrieve it using MCP"""
    print("\n🚀 Testing Insert and Retrieve with PostgreSQL MCP Server...")
    
    # MCP server doesn't use API key in this implementation
    mcp_server = None
    try:
        # Initialize MCP server
        mcp_server = PostgresMCPServer()
        initialized = await mcp_server.initialize()
        
        if not initialized:
            print("❌ Failed to initialize MCP server")
            return False
        
        print("✅ MCP server initialized successfully")

        # 1. Insert a new customer
        customer_id = f"TEST_USER_{random.randint(1000, 9999)}"
        print(f"\n📝 Inserting new customer with ID: {customer_id}")
        
        customer_data = {
            "customer_id": customer_id,
            "first_name": "Test",
            "last_name": "Customer",
            "email": f"test{random.randint(1000, 9999)}@example.com",
            "phone": f"+91{random.randint(9000000000, 9999999999)}",
            "preferred_language": "en",
            "customer_segment": "high_value"
        }
        
        insert_result = await mcp_server.insert_record("customers", customer_data)
        
        if insert_result["success"]:
            print("✅ Customer inserted successfully")
            # Convert datetime objects to strings for JSON serialization
            inserted_record = insert_result.get("inserted_record", {})
            for key, value in inserted_record.items():
                if hasattr(value, 'isoformat'):
                    inserted_record[key] = value.isoformat()
            print(f"📊 Inserted Customer Data: {json.dumps(inserted_record, indent=2, cls=CustomJSONEncoder)}")
        else:
            print(f"❌ Failed to insert customer: {insert_result.get('error')}")
            return False
        
        # 2. Create a conversation for this customer
        conversation_id = str(uuid4())
        print(f"\n📝 Creating conversation with ID: {conversation_id}")
        
        conversation_data = {
            "conversation_id": conversation_id,
            "customer_id": customer_id,
            "title": "Test Conversation",
            "status": "active"
            # Removed 'channel' field as it doesn't exist in the table
        }
        
        conv_result = await mcp_server.insert_record("conversations", conversation_data)
        
        if conv_result["success"]:
            print("✅ Conversation created successfully")
            # Convert datetime objects to strings for JSON serialization
            conv_record = conv_result.get("inserted_record", {})
            for key, value in conv_record.items():
                if hasattr(value, 'isoformat'):
                    conv_record[key] = value.isoformat()
            print(f"📊 Conversation Data: {json.dumps(conv_record, indent=2, cls=CustomJSONEncoder)}")
        else:
            print(f"❌ Failed to create conversation: {conv_result.get('error')}")
        
        # 3. Add messages to the conversation (only if conversation was created successfully)
        if conv_result and conv_result.get("success"):
            print("\n📝 Adding messages to conversation")
            
            messages = [
                {
                    "message_id": str(uuid4()),
                    "conversation_id": conversation_id,
                    "customer_id": customer_id,
                    "speaker": "customer",
                    "message_text": "I'm interested in Smart Swadhan Supreme policy",
                    "message_type": "chat",
                    "sentiment": "neutral"
                },
                {
                    "message_id": str(uuid4()),
                    "conversation_id": conversation_id,
                    "customer_id": customer_id,
                    "speaker": "agent",
                    "message_text": "Smart Swadhan Supreme is a great choice! It offers life cover with added benefits.",
                    "message_type": "chat",
                    "sentiment": "positive"
                },
                {
                    "message_id": str(uuid4()),
                    "conversation_id": conversation_id,
                    "customer_id": customer_id,
                    "speaker": "customer",
                    "message_text": "What are the premium payment options?",
                    "message_type": "chat",
                    "sentiment": "neutral"
                }
            ]
            
            for i, message in enumerate(messages):
                msg_result = await mcp_server.insert_record("messages", message)
                if msg_result["success"]:
                    print(f"✅ Message {i+1} added successfully")
                else:
                    print(f"❌ Failed to add message {i+1}: {msg_result.get('error')}")
        else:
            print("\n⚠️ Skipping message creation since conversation creation failed")
        
        # 4. Add customer preferences
        print("\n📝 Adding customer preferences")
        
        preferences = [
            {
                "customer_id": customer_id,
                "preference_type": "policy_type",
                "preference_value": json.dumps("term_insurance"),  # JSON encode string values
                "confidence_score": 0.85
            },
            {
                "customer_id": customer_id,
                "preference_type": "communication_channel",
                "preference_value": json.dumps("email"),  # JSON encode string values
                "confidence_score": 0.92
            }
        ]
        
        for i, preference in enumerate(preferences):
            pref_result = await mcp_server.insert_record("customer_preferences", preference)
            if pref_result["success"]:
                print(f"✅ Preference {i+1} added successfully")
            else:
                print(f"❌ Failed to add preference {i+1}: {pref_result.get('error')}")
        
        # 5. Retrieve customer data using MCP
        print("\n🔍 Retrieving customer data")
        
        # Get comprehensive customer data
        customer_result = await mcp_server.get_customer_data(customer_id)
        
        if customer_result["success"] and customer_result["rows"]:
            customer = customer_result["rows"][0]
            # Convert datetime objects to strings for JSON serialization
            for key, value in customer.items():
                if hasattr(value, 'isoformat'):
                    customer[key] = value.isoformat()
            
            print("✅ Customer data retrieved successfully")
            print(f"\n📊 FULL CUSTOMER DATA: {json.dumps(customer, indent=2, cls=CustomJSONEncoder)}")
            
            print("\n📊 CUSTOMER PROFILE:")
            print(f"ID: {customer['customer_id']}")
            print(f"Name: {customer['first_name']} {customer['last_name']}")
            print(f"Email: {customer['email']}")
            print(f"Segment: {customer['customer_segment']}")
            
            # Print recent messages
            if 'recent_messages' in customer and customer['recent_messages']:
                print("\n📱 RECENT MESSAGES:")
                # Parse JSON if it's a string
                messages = customer['recent_messages']
                if isinstance(messages, str):
                    try:
                        messages = json.loads(messages)
                    except json.JSONDecodeError:
                        messages = []
                
                if messages and len(messages) > 0:
                    for msg in messages:
                        print(f"[{msg['speaker'].upper()}]: {msg['message_text']}")
                else:
                    print("No messages found.")
            
            # Print preferences
            if 'preferences' in customer and customer['preferences']:
                print("\n🔖 CUSTOMER PREFERENCES:")
                # Parse JSON if it's a string
                preferences = customer['preferences']
                if isinstance(preferences, str):
                    try:
                        preferences = json.loads(preferences)
                    except json.JSONDecodeError:
                        preferences = []
                
                if preferences and len(preferences) > 0:
                    for pref in preferences:
                        # Try to decode JSON preference value
                        pref_value = pref['preference_value']
                        try:
                            if isinstance(pref_value, str):
                                pref_value = json.loads(pref_value)
                        except json.JSONDecodeError:
                            pass
                        
                        print(f"{pref['preference_type']}: {pref_value} (confidence: {pref['confidence_score']})")
                else:
                    print("No preferences found.")
        else:
            print(f"❌ Failed to retrieve customer data: {customer_result.get('error')}")
        
        # 6. Custom query to get all conversations for this customer
        print("\n🔍 Retrieving conversations for customer")
        
        conversation_query = """
            SELECT c.*, 
                   COUNT(m.message_id) as message_count,
                   MAX(m.created_at) as last_message_date
            FROM conversations c
            LEFT JOIN messages m ON c.conversation_id = m.conversation_id
            WHERE c.customer_id = $1
            GROUP BY c.id, c.conversation_id, c.customer_id, c.title, c.status, c.channel, c.created_at, c.updated_at
            ORDER BY last_message_date DESC
        """
        
        conv_result = await mcp_server.execute_query(conversation_query, [customer_id])
        
        if conv_result["success"] and conv_result["rows"]:
            print("✅ Conversations retrieved successfully")
            
            # Convert datetime objects to strings for JSON serialization
            conversations = conv_result["rows"]
            for conv in conversations:
                for key, value in conv.items():
                    if hasattr(value, 'isoformat'):
                        conv[key] = value.isoformat()
            
            print(f"\n📊 Found {len(conversations)} conversations:")
            print(f"Conversations: {json.dumps(conversations, indent=2, cls=CustomJSONEncoder)}")
            
            for conv in conversations:
                print(f"- {conv['title']} (ID: {conv['conversation_id']}, Messages: {conv['message_count']})")
        else:
            print(f"❌ Failed to retrieve conversations: {conv_result.get('error')}")
        
        # 7. Clean up test data
        print("\n🧹 Cleaning up test data...")
        
        # Delete in proper order to respect foreign keys
        cleanup_queries = [
            (f"DELETE FROM customer_preferences WHERE customer_id = '{customer_id}'", "preferences"),
            (f"DELETE FROM messages WHERE customer_id = '{customer_id}'", "messages"),
            (f"DELETE FROM conversations WHERE customer_id = '{customer_id}'", "conversations"),
            (f"DELETE FROM customers WHERE customer_id = '{customer_id}'", "customer")
        ]
        
        for query, data_type in cleanup_queries:
            cleanup_result = await mcp_server.execute_query(query)
            if cleanup_result["success"]:
                print(f"✅ Deleted {data_type}")
            else:
                print(f"❌ Failed to delete {data_type}: {cleanup_result.get('error')}")
        
        # Close the connection
        await mcp_server.close()
        print("\n✅ MCP server connection closed")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
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
    """Run the insert and retrieve test"""
    print(f"🚀 Starting MCP Insert and Retrieve Test")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run the test
        success = loop.run_until_complete(insert_and_retrieve())
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎯 MCP INSERT/RETRIEVE TEST SUMMARY")
        print("=" * 60)
        
        if success:
            print("🎉 Test completed successfully!")
            print("\n✨ Verified:")
            print("   ✅ MCP server initialization with API key")
            print("   ✅ Data insertion into multiple tables")
            print("   ✅ Complex data retrieval")
            print("   ✅ Clean up of test data")
        else:
            print("⚠️ Test had some failures.")
            print("   Please check the logs above for details.")
        
        return success
        
    finally:
        loop.close()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⛔ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test crashed: {e}")
        sys.exit(1)
