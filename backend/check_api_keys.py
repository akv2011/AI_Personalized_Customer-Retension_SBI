#!/usr/bin/env python3
"""
Check API Keys Configuration in PostgreSQL
"""

import asyncio
import sys
import os
import json

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.postgres_mcp_server import PostgresMCPServer

async def check_api_keys():
    """Check for API key related tables and configurations"""
    mcp_server = PostgresMCPServer()
    await mcp_server.initialize()
    
    try:
        # Search for tables that might contain API keys
        print("\n=== SEARCHING FOR API KEY TABLES ===")
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND (
            table_name ILIKE '%api%' OR 
            table_name ILIKE '%key%' OR 
            table_name ILIKE '%auth%' OR 
            table_name ILIKE '%token%' OR
            table_name ILIKE '%credential%'
        );
        """
        
        tables_result = await mcp_server.execute_query(tables_query)
        
        if tables_result["success"] and tables_result["rows"]:
            print("Found potential API key tables:")
            for row in tables_result["rows"]:
                print(f"- {row['table_name']}")
                
                # Get schema for this table
                columns_query = """
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = $1
                ORDER BY ordinal_position;
                """
                
                columns_result = await mcp_server.execute_query(columns_query, [row['table_name']])
                
                if columns_result["success"]:
                    print("  Columns:")
                    for col in columns_result["rows"]:
                        print(f"  - {col['column_name']} ({col['data_type']}, nullable: {col['is_nullable']})")
                    
                    # Check for sample data (first row)
                    try:
                        sample_query = f"SELECT * FROM {row['table_name']} LIMIT 1;"
                        sample_result = await mcp_server.execute_query(sample_query)
                        
                        if sample_result["success"] and sample_result["rows"]:
                            print("  Sample data (first row, sensitive data masked):")
                            sample_data = sample_result["rows"][0]
                            masked_data = {}
                            
                            for key, value in sample_data.items():
                                if key.lower() in ['api_key', 'key', 'token', 'password', 'secret']:
                                    if value and isinstance(value, str):
                                        masked_data[key] = value[:3] + "****" + (value[-3:] if len(value) > 6 else "")
                                    else:
                                        masked_data[key] = value
                                else:
                                    masked_data[key] = value
                                    
                            print(f"  {json.dumps(masked_data, indent=2, default=str)}")
                    except Exception as e:
                        print(f"  Error checking sample data: {e}")
        else:
            print("No API key related tables found in the database.")
        
        # Check for configuration table that might contain API keys
        print("\n=== CHECKING FOR SYSTEM CONFIGURATION ===")
        config_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND (
            table_name ILIKE '%config%' OR 
            table_name ILIKE '%setting%' OR 
            table_name ILIKE '%system%' OR
            table_name ILIKE '%param%'
        );
        """
        
        config_result = await mcp_server.execute_query(config_query)
        
        if config_result["success"] and config_result["rows"]:
            print("Found potential configuration tables:")
            for row in config_result["rows"]:
                print(f"- {row['table_name']}")
                
                # Check for API key related columns
                try:
                    # Count rows to check if table has data
                    count_query = f"SELECT COUNT(*) FROM {row['table_name']};"
                    count_result = await mcp_server.execute_query(count_query)
                    
                    if count_result["success"] and count_result["rows"]:
                        row_count = count_result["rows"][0]["count"]
                        print(f"  Contains {row_count} rows")
                except:
                    pass
        else:
            print("No configuration tables found in the database.")
            
    finally:
        await mcp_server.close()
        print("\nQuery complete. MCP server connection closed.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_api_keys())
