"""
BookContentService implementation
"""
from typing import List, Optional
from src.models.book_content import BookContent, BookContentCreate, BookContentUpdate
from src.db.postgres_client import postgres_client
from src.utils.embedding_utils import cohere_embedding_service
from src.db.qdrant_setup import QdrantSetup
import hashlib
from src.utils.logging import logger
import uuid
class BookContentService:
    def __init__(self):
        self.qdrant_setup = QdrantSetup()
    
    async def create_book(self, book_data: BookContentCreate) -> BookContent:
        """
        Create a new book entry and process its content
        """
        try:
            # Calculate content hash
            content_hash = hashlib.sha256(book_data.content.encode()).hexdigest()
            
            # Create book entry in database
            query = """
                INSERT INTO book_content (id, title, author, isbn, content, content_hash, created_at, updated_at, status)
                VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW(), 'processing')
                RETURNING id, title, author, isbn, content_hash, created_at, updated_at, status
            """
            
            # Generate a new UUID for the book
            import uuid
            book_id = str(uuid.uuid4())
            
            # Execute the query
            result = await postgres_client.execute_query_row(
                query,
                book_id,
                book_data.title,
                book_data.author,
                book_data.isbn,
                book_data.content,
                content_hash
            )
            
            # Create a BookContent instance from the result
            book = BookContent(
                id=result['id'],
                title=result['title'],
                author=result['author'],
                isbn=result['isbn'],
                content=book_data.content,
                content_hash=result['content_hash'],
                created_at=result['created_at'],
                updated_at=result['updated_at'],
                status=result['status']
            )
            
            # Process the book content in the background
            await self.process_book_content(book.id, book_data.content)
            
            logger.info(f"Book created successfully with ID: {book.id}")
            return book
            
        except Exception as e:
            logger.error(f"Error creating book: {e}")
            raise
    
    async def process_book_content(self, book_id: str, content: str):
        """
        Process book content: chunk it, create embeddings, and store in Qdrant
        """
        try:
            # Update status to processing
            await self.update_book_status(book_id, "processing")
            
            # Chunk the content (using paragraph-level chunking with overlap)
            chunks = self.chunk_content(content)
            
            # Generate embeddings for chunks
            chunk_texts = [chunk['text'] for chunk in chunks]
            embeddings = cohere_embedding_service.embed_text(chunk_texts)
            
            # Store chunks and embeddings in Qdrant
            await self.store_chunks_in_qdrant(book_id, chunks, embeddings)
            
            # Update status to ready
            await self.update_book_status(book_id, "ready")
            
            logger.info(f"Book content processed successfully for book ID: {book_id}")
            
        except Exception as e:
            logger.error(f"Error processing book content for book ID {book_id}: {e}")
            await self.update_book_status(book_id, "failed")
            raise
    
    def chunk_content(self, content: str, chunk_size: int = 1000, overlap: int = 100) -> List[dict]:
        """
        Chunk book content into smaller pieces with overlap
        """
        chunks = []
        
        # Split content into paragraphs first
        paragraphs = content.split('\n\n')
        
        current_chunk = ""
        current_pos = 0
        
        for para in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                # Save the current chunk
                chunks.append({
                    'text': current_chunk.strip(),
                    'start_pos': current_pos,
                    'end_pos': current_pos + len(current_chunk)
                })
                
                # Start new chunk with overlap
                if overlap > 0:
                    # Take the end of the current chunk for overlap
                    overlap_text = current_chunk[-overlap:]
                    current_chunk = overlap_text + para
                else:
                    current_chunk = para
                current_pos = current_pos + len(current_chunk) - len(para)
            else:
                current_chunk += para + '\n\n'
        
        # Add the final chunk if it has content
        if current_chunk.strip():
            chunks.append({
                'text': current_chunk.strip(),
                'start_pos': current_pos,
                'end_pos': current_pos + len(current_chunk)
            })
        
        return chunks
    
    async def store_chunks_in_qdrant(self, book_id: str, chunks: List[dict], embeddings: List[List[float]]):
        """
        Store content chunks and their embeddings in Qdrant
        """
        # Prepare points for Qdrant
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = {
                "id": str(uuid.uuid4()), # Is line ko update karein
                "vector": embedding,
                "payload": {
                    "book_id": book_id,
                    "chunk_text": chunk['text'],
                    "start_pos": chunk['start_pos'],
                    "end_pos": chunk['end_pos'],
                    "chunk_index": i
                }
            }
            points.append(point)
        
        # Add points to Qdrant collection
        # Note: In a real implementation, we would use the Qdrant client to add these points
        # For now, we'll just log that this would happen
        logger.info(f"Would store {len(points)} chunks in Qdrant for book {book_id}")
    
    async def update_book_status(self, book_id: str, status: str):
        """
        Update the processing status of a book
        """
        query = """
            UPDATE book_content
            SET status = $1, updated_at = NOW()
            WHERE id = $2
        """
        await postgres_client.execute_command(query, status, book_id)
    
    async def get_book(self, book_id: str) -> Optional[BookContent]:
        """
        Retrieve a book by ID
        """
        query = """
            SELECT id, title, author, isbn, content_hash, created_at, updated_at, status
            FROM book_content
            WHERE id = $1
        """
        result = await postgres_client.execute_query_row(query, book_id)
        
        if result:
            return BookContent(
                id=result['id'],
                title=result['title'],
                author=result['author'],
                isbn=result['isbn'],
                content="",  # Don't return full content for efficiency
                content_hash=result['content_hash'],
                created_at=result['created_at'],
                updated_at=result['updated_at'],
                status=result['status']
            )
        return None
    
    async def get_book_content(self, book_id: str) -> Optional[str]:
        """
        Retrieve the full content of a book by ID
        """
        query = """
            SELECT content
            FROM book_content
            WHERE id = $1
        """
        result = await postgres_client.execute_query_row(query, book_id)
        
        if result:
            return result['content']
        return None
    
    async def list_books(self) -> List[BookContent]:
        """
        List all books
        """
        query = """
            SELECT id, title, author, isbn, content_hash, created_at, updated_at, status
            FROM book_content
        """
        results = await postgres_client.execute_query(query)
        
        books = []
        for result in results:
            book = BookContent(
                id=result['id'],
                title=result['title'],
                author=result['author'],
                isbn=result['isbn'],
                content="",  # Don't return full content for efficiency
                content_hash=result['content_hash'],
                created_at=result['created_at'],
                updated_at=result['updated_at'],
                status=result['status']
            )
            books.append(book)
        
        return books


# Global instance
book_content_service = BookContentService()
