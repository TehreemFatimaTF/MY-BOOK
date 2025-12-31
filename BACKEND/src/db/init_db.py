import asyncio
import os
import sys

# Add BACKEND to path so imports work
sys.path.append(os.getcwd())

from src.db.postgres_client import postgres_client
# Mock logger if needed or import
from src.utils.logging import logger

async def init_db():
    print("Initializing database...")
    try:
        await postgres_client.initialize_pool()
        
        # user_queries
        print("Creating user_queries table...")
        await postgres_client.execute_command("""
            CREATE TABLE IF NOT EXISTS user_queries (
                id TEXT PRIMARY KEY,
                book_id TEXT NOT NULL,
                query_text TEXT NOT NULL,
                selected_text TEXT,
                session_id TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # retrieved_contexts
        print("Creating retrieved_contexts table...")
        await postgres_client.execute_command("""
            CREATE TABLE IF NOT EXISTS retrieved_contexts (
                id TEXT PRIMARY KEY,
                query_id TEXT REFERENCES user_queries(id),
                content_chunk TEXT,
                chunk_id TEXT,
                relevance_score FLOAT,
                retrieved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # generated_responses
        print("Creating generated_responses table...")
        await postgres_client.execute_command("""
            CREATE TABLE IF NOT EXISTS generated_responses (
                id TEXT PRIMARY KEY,
                query_id TEXT REFERENCES user_queries(id),
                response_text TEXT,
                confidence_score FLOAT,
                source_chunks TEXT[],
                generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # query_history
        print("Creating query_history table...")
        await postgres_client.execute_command("""
            CREATE TABLE IF NOT EXISTS query_history (
                id TEXT PRIMARY KEY,
                query_id TEXT REFERENCES user_queries(id),
                user_id TEXT,
                query_text TEXT,
                response_text TEXT,
                accuracy_score FLOAT,
                feedback TEXT,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)

        # Ensure book_content exists (just in case)
        print("Verifying book_content table...")
        await postgres_client.execute_command("""
            CREATE TABLE IF NOT EXISTS book_content (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                chunked_content TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                status TEXT DEFAULT 'processing'
            )
        """)
        
        print("Database initialization complete.")
    except Exception as e:
        print(f"Error initializing DB: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await postgres_client.close_pool()

if __name__ == "__main__":
    asyncio.run(init_db())
