"""
Book ingestion pipeline to process and index content
"""
from typing import Optional
from src.services.book_content_service import BookContentService
from src.services.qdrant_service import QdrantService
from src.utils.text_chunker import TextChunker
from src.utils.embedding_utils import cohere_embedding_service
from src.utils.logging import logger
import asyncio
import uuid

class BookIngestionPipeline:
    def __init__(self):
        self.book_content_service = BookContentService()
        self.qdrant_service = QdrantService()
        self.text_chunker = TextChunker()
    
    async def ingest_book(self, title: str, author: str, content: str, isbn: Optional[str] = None) -> str:
        """
        Ingest a book into the system: validate, process, chunk, embed, and index
        """
        try:
            logger.info(f"Starting ingestion for book: '{title}' by {author}")
            
            # Validate input
            if not title or not title.strip():
                raise ValueError("Book title is required")
            if not author or not author.strip():
                raise ValueError("Book author is required")
            if not content or len(content) < 100:
                raise ValueError("Book content is required and must be at least 100 characters")
            
            # Create the book record in the database (status: processing)
            from src.models.book_content import BookContentCreate
            book_data = BookContentCreate(
                title=title,
                author=author,
                isbn=isbn,
                content=content
            )
            
            book = await self.book_content_service.create_book(book_data)
            book_id = book.id
            
            logger.info(f"Book record created with ID: {book_id}")
            
            # Process the book content (chunk, embed, index)
            await self._process_book_content(book_id, content)
            
            logger.info(f"Successfully ingested book: '{title}' with ID: {book_id}")
            return book_id
            
        except Exception as e:
            logger.error(f"Error ingesting book: {e}")
            # In a real implementation, you might want to update the book status to "failed"
            raise
    
    async def _process_book_content(self, book_id: str, content: str):
        """
        Process book content: chunk, embed, and store in Qdrant
        """
        try:
            logger.info(f"Processing content for book {book_id}")
            
            # Chunk the content
            chunks = self.text_chunker.chunk_content(content)
            logger.info(f"Content chunked into {len(chunks)} pieces")
            
            # Generate embeddings for chunks
            chunk_texts = [chunk['text'] for chunk in chunks]
            logger.info(f"Generating embeddings for {len(chunk_texts)} chunks...")
            
            embeddings = cohere_embedding_service.embed_text(chunk_texts)
            logger.info(f"Generated embeddings for {len(embeddings)} chunks")
            
            # Store chunks and embeddings in Qdrant
            await self._store_in_qdrant(book_id, chunks, embeddings)
            
            logger.info(f"Successfully processed and indexed content for book {book_id}")
            
        except Exception as e:
            logger.error(f"Error processing book content for book {book_id}: {e}")
            raise
    
    async def _store_in_qdrant(self, book_id: str, chunks: list, embeddings: list):
        """
        Store content chunks and their embeddings in Qdrant
        """
        try:
            # Prepare points for Qdrant
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point = {
                    "id": f"{book_id}_chunk_{i}",
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
            self.qdrant_service.client.upsert(
                collection_name=self.qdrant_service.collection_name,
                points=points
            )
            
            logger.info(f"Stored {len(points)} chunks in Qdrant for book {book_id}")
            
        except Exception as e:
            logger.error(f"Error storing chunks in Qdrant for book {book_id}: {e}")
            raise
    
    async def update_book(self, book_id: str, title: Optional[str] = None, author: Optional[str] = None, 
                         content: Optional[str] = None, isbn: Optional[str] = None):
        """
        Update an existing book and re-index its content if changed
        """
        try:
            logger.info(f"Updating book with ID: {book_id}")
            
            # Get the current book to check if content changed
            current_book = await self.book_content_service.get_book(book_id)
            if not current_book:
                raise ValueError(f"Book with ID {book_id} not found")
            
            # If content is being updated, we need to reprocess it
            if content:
                # Delete existing chunks from Qdrant
                self.qdrant_service.delete_book_chunks(book_id)
                
                # Update the book content in the database
                # In a real implementation, you would have an update method in BookContentService
                # For now, we'll just process the new content
                await self._process_book_content(book_id, content)
            
            logger.info(f"Successfully updated book with ID: {book_id}")
            
        except Exception as e:
            logger.error(f"Error updating book {book_id}: {e}")
            raise
    
    async def delete_book(self, book_id: str):
        """
        Delete a book and its associated data
        """
        try:
            logger.info(f"Deleting book with ID: {book_id}")
            
            # Delete chunks from Qdrant
            self.qdrant_service.delete_book_chunks(book_id)
            
            # In a real implementation, you would also delete the book record from PostgreSQL
            # For now, we'll just log the action
            
            logger.info(f"Successfully deleted book with ID: {book_id}")
            
        except Exception as e:
            logger.error(f"Error deleting book {book_id}: {e}")
            raise

# Global instance
book_ingestion_pipeline = BookIngestionPipeline()