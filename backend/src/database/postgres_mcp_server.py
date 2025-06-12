"""
PostgreSQL MCP Server for SBI Personalization Engine

This module implements the Model Context Protocol (MCP) server for PostgreSQL operations,
providing a standardized interface for database interactions.
"""
import asyncio
import asyncpg
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from src.config.config import (
    POSTGRES_HOST, 
    POSTGRES_PORT, 
    POSTGRES_DB, 
    POSTGRES_USER, 
    POSTGRES_PASSWORD,
    DATABASE_URL
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgresMCPServer:
    """
    PostgreSQL MCP Server implementation for handling database operations
    """
    
    def __init__(self):
        self.pool = None
        self.server_name = "sbi-postgres-mcp"
        self.version = "1.0.0"
        
    async def initialize(self):
        """Initialize the database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            logger.info(f"PostgreSQL MCP Server '{self.server_name}' initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL MCP Server: {e}")
            return False
    
    async def close(self):
        """Close the database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL MCP Server connection pool closed")
    
    async def execute_query(self, query: str, params: List[Any] = None) -> Dict[str, Any]:
        """
        Execute a SQL query and return results
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Dict containing query results and metadata
        """
        if not self.pool:
            raise Exception("Database pool not initialized")
        
        operation_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        try:
            async with self.pool.acquire() as connection:
                # Log the operation
                await self._log_operation(
                    connection, 
                    operation_id, 
                    "query", 
                    {"query": query, "params": params}
                )
                
                if params:
                    result = await connection.fetch(query, *params)
                else:
                    result = await connection.fetch(query)
                
                # Convert asyncpg.Record objects to dictionaries
                rows = [dict(row) for row in result]
                
                execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                # Update operation log with success
                await self._update_operation_status(
                    connection, 
                    operation_id, 
                    "completed", 
                    execution_time_ms=int(execution_time)
                )
                
                return {
                    "success": True,
                    "operation_id": operation_id,
                    "rows": rows,
                    "row_count": len(rows),
                    "execution_time_ms": int(execution_time)
                }
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Log the error
            try:
                async with self.pool.acquire() as connection:
                    await self._update_operation_status(
                        connection, 
                        operation_id, 
                        "failed", 
                        error_message=str(e),
                        execution_time_ms=int(execution_time)
                    )
            except:
                pass  # Don't fail if logging fails
            
            return {
                "success": False,
                "operation_id": operation_id,
                "error": str(e),
                "execution_time_ms": int(execution_time)
            }
    
    async def insert_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new record into the specified table
        
        Args:
            table: Table name
            data: Dictionary of column-value pairs
            
        Returns:
            Dict containing operation result
        """
        if not self.pool:
            raise Exception("Database pool not initialized")
        
        operation_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        try:
            # Build insert query
            columns = list(data.keys())
            placeholders = [f"${i+1}" for i in range(len(columns))]
            values = list(data.values())
            
            query = f"""
                INSERT INTO {table} ({', '.join(columns)}) 
                VALUES ({', '.join(placeholders)}) 
                RETURNING *
            """
            
            async with self.pool.acquire() as connection:
                # Log the operation
                await self._log_operation(
                    connection, 
                    operation_id, 
                    "insert", 
                    {"table": table, "data": data}
                )
                
                result = await connection.fetchrow(query, *values)
                execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                # Update operation log with success
                await self._update_operation_status(
                    connection, 
                    operation_id, 
                    "completed", 
                    execution_time_ms=int(execution_time)
                )
                
                return {
                    "success": True,
                    "operation_id": operation_id,
                    "inserted_record": dict(result) if result else None,
                    "execution_time_ms": int(execution_time)
                }
                
        except Exception as e:
            logger.error(f"Insert operation failed: {e}")
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Log the error
            try:
                async with self.pool.acquire() as connection:
                    await self._update_operation_status(
                        connection, 
                        operation_id, 
                        "failed", 
                        error_message=str(e),
                        execution_time_ms=int(execution_time)
                    )
            except:
                pass
            
            return {
                "success": False,
                "operation_id": operation_id,
                "error": str(e),
                "execution_time_ms": int(execution_time)
            }
    
    async def update_record(self, table: str, where_clause: str, where_params: List[Any], 
                          update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update records in the specified table
        
        Args:
            table: Table name
            where_clause: WHERE clause (without 'WHERE' keyword)
            where_params: Parameters for WHERE clause
            update_data: Dictionary of column-value pairs to update
            
        Returns:
            Dict containing operation result
        """
        if not self.pool:
            raise Exception("Database pool not initialized")
        
        operation_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        try:
            # Build update query
            set_clauses = []
            set_values = []
            param_index = 1
            
            for column, value in update_data.items():
                set_clauses.append(f"{column} = ${param_index}")
                set_values.append(value)
                param_index += 1
            
            # Add WHERE parameters
            all_params = set_values + where_params
            
            # Update WHERE clause parameter indices
            where_clause_updated = where_clause
            for i, _ in enumerate(where_params):
                where_clause_updated = where_clause_updated.replace(f"${i+1}", f"${param_index + i}")
            
            query = f"""
                UPDATE {table} 
                SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP 
                WHERE {where_clause_updated}
                RETURNING *
            """
            
            async with self.pool.acquire() as connection:
                # Log the operation
                await self._log_operation(
                    connection, 
                    operation_id, 
                    "update", 
                    {"table": table, "where": where_clause, "data": update_data}
                )
                
                results = await connection.fetch(query, *all_params)
                execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                # Update operation log with success
                await self._update_operation_status(
                    connection, 
                    operation_id, 
                    "completed", 
                    execution_time_ms=int(execution_time)
                )
                
                return {
                    "success": True,
                    "operation_id": operation_id,
                    "updated_records": [dict(row) for row in results],
                    "updated_count": len(results),
                    "execution_time_ms": int(execution_time)
                }
                
        except Exception as e:
            logger.error(f"Update operation failed: {e}")
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Log the error
            try:
                async with self.pool.acquire() as connection:
                    await self._update_operation_status(
                        connection, 
                        operation_id, 
                        "failed", 
                        error_message=str(e),
                        execution_time_ms=int(execution_time)
                    )
            except:
                pass
            
            return {
                "success": False,
                "operation_id": operation_id,
                "error": str(e),
                "execution_time_ms": int(execution_time)
            }
    
    async def get_customer_data(self, customer_id: str) -> Dict[str, Any]:
        """Get comprehensive customer data including conversations and preferences"""
        query = """
            WITH customer_summary AS (
                SELECT 
                    c.*,
                    COUNT(DISTINCT conv.id) as conversation_count,
                    COUNT(DISTINCT m.id) as message_count,
                    MAX(m.created_at) as last_interaction
                FROM customers c
                LEFT JOIN conversations conv ON c.customer_id = conv.customer_id
                LEFT JOIN messages m ON c.customer_id = m.customer_id
                WHERE c.customer_id = $1
                GROUP BY c.id
            ),
            recent_messages AS (
                SELECT m.*, conv.title as conversation_title
                FROM messages m
                JOIN conversations conv ON m.conversation_id = conv.conversation_id
                WHERE m.customer_id = $1
                ORDER BY m.created_at DESC
                LIMIT 10
            ),
            preferences AS (
                SELECT preference_type, preference_value, confidence_score
                FROM customer_preferences
                WHERE customer_id = $1
                ORDER BY updated_at DESC
            )
            SELECT 
                cs.*,
                COALESCE(
                    json_agg(
                        json_build_object(
                            'message_id', rm.message_id,
                            'speaker', rm.speaker,
                            'message_text', rm.message_text,
                            'sentiment', rm.sentiment,
                            'conversation_title', rm.conversation_title,
                            'created_at', rm.created_at
                        ) ORDER BY rm.created_at DESC
                    ) FILTER (WHERE rm.message_id IS NOT NULL),
                    '[]'::json
                ) as recent_messages,
                COALESCE(
                    json_agg(
                        json_build_object(
                            'preference_type', p.preference_type,
                            'preference_value', p.preference_value,
                            'confidence_score', p.confidence_score
                        )
                    ) FILTER (WHERE p.preference_type IS NOT NULL),
                    '[]'::json
                ) as preferences
            FROM customer_summary cs
            LEFT JOIN recent_messages rm ON true
            LEFT JOIN preferences p ON true
            GROUP BY cs.id, cs.customer_id, cs.first_name, cs.last_name, cs.email, 
                     cs.phone, cs.date_of_birth, cs.preferred_language, cs.customer_segment, 
                     cs.risk_profile, cs.created_at, cs.updated_at, cs.conversation_count, 
                     cs.message_count, cs.last_interaction
        """
        
        return await self.execute_query(query, [customer_id])
    
    async def store_conversation_message(self, customer_id: str, conversation_id: str, 
                                      message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store a new conversation message with proper relationships"""
        try:
            # Ensure customer exists
            await self._ensure_customer_exists(customer_id)
            
            # Ensure conversation exists
            await self._ensure_conversation_exists(conversation_id, customer_id)
            
            # Insert the message
            message_record = {
                "message_id": message_data.get("message_id", str(uuid.uuid4())),
                "conversation_id": conversation_id,
                "customer_id": customer_id,
                "speaker": message_data["speaker"],
                "message_text": message_data["message_text"],
                "message_type": message_data.get("message_type", "chatbot"),
                "sentiment": message_data.get("sentiment"),
                "language": message_data.get("language", "en"),
                "embedding_id": message_data.get("embedding_id"),
                "metadata": json.dumps(message_data.get("metadata", {})) if message_data.get("metadata") else None
            }
            
            return await self.insert_record("messages", message_record)
            
        except Exception as e:
            logger.error(f"Failed to store conversation message: {e}")
            return {"success": False, "error": str(e)}
    
    async def _ensure_customer_exists(self, customer_id: str):
        """Ensure customer record exists, create if not"""
        check_query = "SELECT customer_id FROM customers WHERE customer_id = $1"
        result = await self.execute_query(check_query, [customer_id])
        
        if not result["rows"]:
            customer_data = {
                "customer_id": customer_id,
                "preferred_language": "en",
                "customer_segment": "unknown"
            }
            await self.insert_record("customers", customer_data)
    
    async def _ensure_conversation_exists(self, conversation_id: str, customer_id: str):
        """Ensure conversation record exists, create if not"""
        check_query = "SELECT conversation_id FROM conversations WHERE conversation_id = $1"
        result = await self.execute_query(check_query, [conversation_id])
        
        if not result["rows"]:
            conversation_data = {
                "conversation_id": conversation_id,
                "customer_id": customer_id,
                "title": "Chat Session",
                "status": "active"
            }
            await self.insert_record("conversations", conversation_data)
    
    async def _log_operation(self, connection, operation_id: str, operation_type: str, 
                           operation_data: Dict[str, Any]):
        """Log MCP operation"""
        try:
            await connection.execute(
                """
                INSERT INTO mcp_operations (operation_id, operation_type, operation_data, status) 
                VALUES ($1, $2, $3, $4)
                """,
                operation_id, operation_type, json.dumps(operation_data), "pending"
            )
        except Exception as e:
            logger.error(f"Failed to log operation: {e}")
    
    async def _update_operation_status(self, connection, operation_id: str, status: str, 
                                     error_message: str = None, execution_time_ms: int = None):
        """Update MCP operation status"""
        try:
            await connection.execute(
                """
                UPDATE mcp_operations 
                SET status = $2, error_message = $3, execution_time_ms = $4, completed_at = CURRENT_TIMESTAMP
                WHERE operation_id = $1
                """,
                operation_id, status, error_message, execution_time_ms
            )
        except Exception as e:
            logger.error(f"Failed to update operation status: {e}")

# Global MCP server instance
mcp_server = PostgresMCPServer()

async def initialize_mcp_server():
    """Initialize the global MCP server"""
    return await mcp_server.initialize()

async def close_mcp_server():
    """Close the global MCP server"""
    await mcp_server.close()

# Convenience functions for common operations
async def mcp_execute_query(query: str, params: List[Any] = None) -> Dict[str, Any]:
    """Execute a query using the global MCP server"""
    return await mcp_server.execute_query(query, params)

async def mcp_insert_record(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a record using the global MCP server"""
    return await mcp_server.insert_record(table, data)

async def mcp_get_customer_data(customer_id: str) -> Dict[str, Any]:
    """Get customer data using the global MCP server"""
    return await mcp_server.get_customer_data(customer_id)

async def mcp_store_message(customer_id: str, conversation_id: str, 
                          message_data: Dict[str, Any]) -> Dict[str, Any]:
    """Store a conversation message using the global MCP server"""
    return await mcp_server.store_conversation_message(customer_id, conversation_id, message_data)
