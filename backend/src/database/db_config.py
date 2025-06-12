"""
PostgreSQL Database Configuration for SBI Personalization Engine with MCP Integration
"""
import asyncio
import asyncpg
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Text, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import logging
import json
from src.config.config import (
    DATABASE_URL, 
    POSTGRES_HOST, 
    POSTGRES_PORT, 
    POSTGRES_DB, 
    POSTGRES_USER, 
    POSTGRES_PASSWORD
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy setup
Base = declarative_base()
engine = None
SessionLocal = None

class DatabaseManager:
    """Manages PostgreSQL database connections and operations"""
    
    def __init__(self):
        self.engine = None
        self.session_local = None
        self.async_pool = None
        
    def initialize_sync_connection(self):
        """Initialize synchronous database connection"""
        try:
            self.engine = create_engine(
                DATABASE_URL,
                echo=False,  # Set to True for SQL debugging
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=1800
            )
            self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info("Synchronous database connection initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize synchronous database connection: {e}")
            return False
    
    async def initialize_async_connection(self):
        """Initialize asynchronous database connection for MCP"""
        try:
            self.async_pool = await asyncpg.create_pool(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                min_size=5,
                max_size=20
            )
            logger.info("Asynchronous database connection pool initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize asynchronous database connection: {e}")
            return False
    
    def get_sync_session(self):
        """Get a synchronous database session"""
        if not self.session_local:
            self.initialize_sync_connection()
        return self.session_local()
    
    async def get_async_connection(self):
        """Get an asynchronous database connection"""
        if not self.async_pool:
            await self.initialize_async_connection()
        return await self.async_pool.acquire()
    
    async def release_async_connection(self, connection):
        """Release an asynchronous database connection"""
        if self.async_pool:
            await self.async_pool.release(connection)
    
    def test_connection(self):
        """Test database connectivity"""
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )
            conn.close()
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

# Global database manager instance
db_manager = DatabaseManager()

def get_database_session():
    """Get a database session for dependency injection"""
    return db_manager.get_sync_session()

async def get_async_database_connection():
    """Get an async database connection for MCP operations"""
    return await db_manager.get_async_connection()

def initialize_database():
    """Initialize database with all required configurations"""
    try:
        # Test connection first
        if not db_manager.test_connection():
            raise Exception("Database connection test failed")
        
        # Initialize sync connection
        if not db_manager.initialize_sync_connection():
            raise Exception("Failed to initialize synchronous connection")
        
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False