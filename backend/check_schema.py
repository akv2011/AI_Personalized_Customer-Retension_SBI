#!/usr/bin/env python3
"""
Script to check PostgreSQL DB Schema using MCP Server
This script uses the PostgreSQL MCP Server to query schema information.
"""

import asyncio
import sys
import os
from datetime import datetime
import json
from prettytable import PrettyTable

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.postgres_mcp_server import PostgresMCPServer

async def check_db_schema(api_key=None):
    """Query and display database schema information"""
    print("\n🔍 Checking PostgreSQL Database Schema with MCP Server...")
    
    mcp_server = None
    try:
        # Initialize MCP server with optional API key
        mcp_server = PostgresMCPServer(api_key=api_key) if api_key else PostgresMCPServer()
        initialized = await mcp_server.initialize()
        
        if not initialized:
            print("❌ Failed to initialize MCP server")
            return False
        
        print("✅ MCP server initialized successfully")
        
        # 1. List all tables in the database
        print("\n📋 Database Tables:")
        tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """
        tables_result = await mcp_server.execute_query(tables_query)
        
        if not tables_result["success"]:
            print(f"❌ Failed to retrieve tables: {tables_result.get('error')}")
            return False
        
        tables = [row["table_name"] for row in tables_result["rows"]]
        
        if not tables:
            print("⚠️ No tables found in the database")
            return False
        
        # Print tables as a list
        table = PrettyTable()
        table.field_names = ["Table Name"]
        for table_name in tables:
            table.add_row([table_name])
        print(table)
        
        # 2. For each table, get its columns and data types
        for table_name in tables:
            print(f"\n📊 Schema for table '{table_name}':")
            
            columns_query = """
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable, 
                    column_default
                FROM 
                    information_schema.columns 
                WHERE 
                    table_schema = 'public' AND 
                    table_name = $1
                ORDER BY 
                    ordinal_position;
            """
            
            columns_result = await mcp_server.execute_query(columns_query, [table_name])
            
            if not columns_result["success"]:
                print(f"❌ Failed to retrieve columns for {table_name}: {columns_result.get('error')}")
                continue
            
            columns = columns_result["rows"]
            
            if not columns:
                print(f"⚠️ No columns found for table {table_name}")
                continue
            
            # Print columns as a formatted table
            table = PrettyTable()
            table.field_names = ["Column Name", "Data Type", "Nullable", "Default"]
            for column in columns:
                table.add_row([
                    column["column_name"],
                    column["data_type"],
                    column["is_nullable"],
                    column["column_default"] or ""
                ])
            print(table)
            
            # 3. Get primary key information
            pk_query = """
                SELECT 
                    tc.constraint_name, 
                    kcu.column_name
                FROM 
                    information_schema.table_constraints tc
                JOIN 
                    information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                WHERE 
                    tc.constraint_type = 'PRIMARY KEY' AND
                    tc.table_schema = 'public' AND
                    tc.table_name = $1
                ORDER BY 
                    kcu.ordinal_position;
            """
            
            pk_result = await mcp_server.execute_query(pk_query, [table_name])
            
            if pk_result["success"] and pk_result["rows"]:
                pk_columns = [row["column_name"] for row in pk_result["rows"]]
                print(f"🔑 Primary Key: {', '.join(pk_columns)}")
        
        await mcp_server.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking database schema: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if mcp_server:
            try:
                await mcp_server.close()
                print("\n✅ MCP server connection closed")
            except Exception as e:
                print(f"⚠️ Error closing MCP server: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check PostgreSQL Database Schema using MCP Server")
    parser.add_argument("--api-key", help="API key for MCP server authentication")
    parser.add_argument("--gemini", action="store_true", help="Use Gemini API key for authentication")
    args = parser.parse_args()
    
    # Set API key
    api_key = None
    if args.api_key:
        api_key = args.api_key
    elif args.gemini:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ GEMINI_API_KEY environment variable not set.")
    else:
        api_key = os.getenv("MCP_API_KEY")
    
    # Run the schema check
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(check_db_schema(api_key))
    finally:
        loop.close()
