import asyncio
import os
import sys
import hashlib
from datetime import datetime, timezone

# Add BACKEND to path so imports work
sys.path.append(os.getcwd())

from src.db.postgres_client import postgres_client

async def add_dummy_book():
    print("Adding dummy book...")
    try:
        await postgres_client.initialize_pool()
        
        book_id = "physical_ai_textbook"
        title = "Physical AI Textbook"
        author = "Admin"
        content = "This is a placeholder for the Physical AI Textbook content. It needs to be at least 100 characters long to pass validation. Robotics and AI are converging into Physical AI where agents interact with the real world."
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Check if exists
        row = await postgres_client.execute_query_row("SELECT id FROM book_content WHERE id = $1", book_id)
        if row:
            print("Book already exists. Updating status to ready...")
            await postgres_client.execute_command("UPDATE book_content SET status = 'ready' WHERE id = $1", book_id)
        else:
            print("Inserting new book...")
            await postgres_client.execute_command("""
                INSERT INTO book_content (id, title, author, isbn, content, content_hash, created_at, updated_at, status)
                VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW(), 'ready')
            """, book_id, title, author, None, content, content_hash)
        
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await postgres_client.close_pool()

if __name__ == "__main__":
    asyncio.run(add_dummy_book())
