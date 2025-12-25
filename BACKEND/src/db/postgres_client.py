"""
PostgreSQL connection client with connection pooling for Neon
"""
import asyncpg
from typing import Optional
from src.config.settings import settings
from src.utils.logging import logger
import os

class PostgresClient:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.connection_string = settings.neon_db_url
    
    async def initialize_pool(self):
        """Initialize the connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                dsn=self.connection_string,
                min_size=settings.postgres_pool_size // 4,  # Minimum connections
                max_size=settings.postgres_pool_size,        # Maximum connections
                command_timeout=60,                          # Timeout for commands
                server_settings={
                    "application_name": "book-rag-chatbot",
                    "statement_timeout": "30s"              # Timeout for statements
                }
            )
            logger.info(f"PostgreSQL connection pool initialized with {settings.postgres_pool_size} max connections")
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL connection pool: {e}")
            raise
    
    async def close_pool(self):
        """Close the connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL connection pool closed")
    
    async def get_connection(self):
        """Get a connection from the pool"""
        if not self.pool:
            raise RuntimeError("PostgreSQL pool not initialized. Call initialize_pool() first.")
        return self.pool.acquire()
    
    async def execute_query(self, query: str, *args):
        """Execute a query using a connection from the pool"""
        if not self.pool:
            raise RuntimeError("PostgreSQL pool not initialized. Call initialize_pool() first.")
        
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def execute_query_row(self, query: str, *args):
        """Execute a query and return a single row"""
        if not self.pool:
            raise RuntimeError("PostgreSQL pool not initialized. Call initialize_pool() first.")
        
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
    
    async def execute_command(self, command: str, *args):
        """Execute a command (INSERT, UPDATE, DELETE) using a connection from the pool"""
        if not self.pool:
            raise RuntimeError("PostgreSQL pool not initialized. Call initialize_pool() first.")
        
        async with self.pool.acquire() as conn:
            return await conn.execute(command, *args)

# Create a global instance
postgres_client = PostgresClient()

# Example usage:
# async def example_usage():
#     await postgres_client.initialize_pool()
#     try:
#         result = await postgres_client.execute_query("SELECT * FROM some_table WHERE id = $1", 123)
#         print(result)
#     finally:
#         await postgres_client.close_pool()