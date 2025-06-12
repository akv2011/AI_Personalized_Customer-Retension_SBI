#!/usr/bin/env python3
"""
Database initialization script for SBI Personalization Engine with PostgreSQL MCP
"""
import os
import sys
import asyncio
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config.config import (
    POSTGRES_HOST, 
    POSTGRES_PORT, 
    POSTGRES_DB, 
    POSTGRES_USER, 
    POSTGRES_PASSWORD,
    DATABASE_URL
)
from src.database.postgres_mcp_server import initialize_mcp_server
from src.database.database_service import initialize_database_service

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_database_and_user():
    """Create PostgreSQL database and user if they don't exist"""
    try:
        # Connect to PostgreSQL as superuser (usually 'postgres')
        superuser_conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user='postgres',  # Default superuser
            password=input("Enter PostgreSQL superuser (postgres) password: ")
        )
        superuser_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = superuser_conn.cursor()
        
        # Create user if not exists
        try:
            cursor.execute(f"CREATE USER {POSTGRES_USER} WITH PASSWORD '{POSTGRES_PASSWORD}';")
            logger.info(f"Created user: {POSTGRES_USER}")
        except psycopg2.errors.DuplicateObject:
            logger.info(f"User {POSTGRES_USER} already exists")
        
        # Create database if not exists
        try:
            cursor.execute(f"CREATE DATABASE {POSTGRES_DB} OWNER {POSTGRES_USER};")
            logger.info(f"Created database: {POSTGRES_DB}")
        except psycopg2.errors.DuplicateDatabase:
            logger.info(f"Database {POSTGRES_DB} already exists")
        
        # Grant privileges
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {POSTGRES_DB} TO {POSTGRES_USER};")
        logger.info(f"Granted privileges to {POSTGRES_USER}")
        
        cursor.close()
        superuser_conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Failed to create database and user: {e}")
        return False

def execute_schema():
    """Execute the schema SQL file"""
    try:
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'src', 'database', 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Connect to the target database
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Execute schema
        cursor.execute(schema_sql)
        logger.info("Schema executed successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Failed to execute schema: {e}")
        return False

def test_connection():
    """Test database connection"""
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        logger.info(f"Database connection successful. PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

async def test_mcp_server():
    """Test MCP server functionality"""
    try:
        logger.info("Testing MCP server initialization...")
        success = await initialize_mcp_server()
        
        if success:
            logger.info("MCP server initialized successfully")
            
            # Test database service
            logger.info("Testing database service...")
            db_service_success = await initialize_database_service()
            
            if db_service_success:
                logger.info("Database service initialized successfully")
                return True
            else:
                logger.error("Database service initialization failed")
                return False
        else:
            logger.error("MCP server initialization failed")
            return False
            
    except Exception as e:
        logger.error(f"MCP server test failed: {e}")
        return False

def insert_sample_data():
    """Insert sample data for testing"""
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()
        
        # Insert sample customer
        cursor.execute("""
            INSERT INTO customers (customer_id, first_name, last_name, email, preferred_language, customer_segment)
            VALUES ('SAMPLE_USER_001', 'John', 'Doe', 'john.doe@example.com', 'en', 'premium')
            ON CONFLICT (customer_id) DO NOTHING;
        """)
        
        # Insert sample product
        cursor.execute("""
            INSERT INTO products (product_id, product_name, product_type, description, is_active)
            VALUES (
                'SSS_001', 
                'Smart Swadhan Supreme', 
                'endowment_plan',
                'A comprehensive life insurance plan with return of premium benefits',
                true
            )
            ON CONFLICT (product_id) DO NOTHING;
        """)
        
        conn.commit()
        logger.info("Sample data inserted successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Failed to insert sample data: {e}")
        return False

def main():
    """Main initialization function"""
    logger.info("Starting SBI Personalization Engine Database Initialization...")
    
    # Step 1: Create database and user
    logger.info("Step 1: Creating database and user...")
    if not create_database_and_user():
        logger.error("Failed to create database and user. Exiting.")
        return False
    
    # Step 2: Execute schema
    logger.info("Step 2: Executing database schema...")
    if not execute_schema():
        logger.error("Failed to execute schema. Exiting.")
        return False
    
    # Step 3: Test connection
    logger.info("Step 3: Testing database connection...")
    if not test_connection():
        logger.error("Database connection test failed. Exiting.")
        return False
    
    # Step 4: Test MCP server
    logger.info("Step 4: Testing MCP server...")
    if not asyncio.run(test_mcp_server()):
        logger.error("MCP server test failed. Exiting.")
        return False
    
    # Step 5: Insert sample data
    logger.info("Step 5: Inserting sample data...")
    if not insert_sample_data():
        logger.error("Failed to insert sample data. Continuing anyway.")
    
    logger.info("✅ Database initialization completed successfully!")
    logger.info(f"Database URL: {DATABASE_URL}")
    logger.info("You can now start the application with: python run.py")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
