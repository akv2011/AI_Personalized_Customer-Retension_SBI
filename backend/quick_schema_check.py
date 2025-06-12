#!/usr/bin/env python3
"""
Quick SQL Script to check PostgreSQL Schema
"""

import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.postgres_mcp_server import PostgresMCPServer

async def check_schema():
    """Run SQL queries to check schema"""
    mcp_server = PostgresMCPServer()
    await mcp_server.initialize()
    
    try:
        # List all tables
        print("\n=== DATABASE TABLES ===")
        tables_query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
        result = await mcp_server.execute_query(tables_query)
        if result["success"]:
            for row in result["rows"]:
                print(f"- {row['tablename']}")
        else:
            print(f"Error: {result.get('error')}")
            
        # Get detailed schema information
        print("\n=== DETAILED SCHEMA ===")
        schema_query = """
        SELECT
            t.table_name,
            c.column_name,
            c.data_type,
            c.character_maximum_length,
            c.is_nullable,
            c.column_default
        FROM
            information_schema.tables t
        JOIN
            information_schema.columns c ON t.table_name = c.table_name
        WHERE
            t.table_schema = 'public'
            AND c.table_schema = 'public'
        ORDER BY
            t.table_name,
            c.ordinal_position;
        """
        
        result = await mcp_server.execute_query(schema_query)
        if result["success"]:
            current_table = None
            for row in result["rows"]:
                if current_table != row["table_name"]:
                    current_table = row["table_name"]
                    print(f"\nTable: {current_table}")
                    print("-" * 80)
                    print(f"{'Column':<20} {'Type':<20} {'Nullable':<10} {'Default':<20}")
                    print("-" * 80)
                
                data_type = row["data_type"]
                if row["character_maximum_length"]:
                    data_type += f"({row['character_maximum_length']})"
                    
                print(f"{row['column_name']:<20} {data_type:<20} {row['is_nullable']:<10} {row['column_default'] or '':<20}")
        else:
            print(f"Error: {result.get('error')}")
            
    finally:
        await mcp_server.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_schema())
