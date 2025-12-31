"""
Text chunker utility for paragraph-level chunking with overlap
"""
from typing import List, Dict, Any
import re

class TextChunker:
    def __init__(self, default_chunk_size: int = 1000, default_overlap: int = 100):
        self.default_chunk_size = default_chunk_size
        self.default_overlap = default_overlap
    
    def chunk_content(self, content: str, chunk_size: int = None, overlap: int = None) -> List[Dict[str, Any]]:
        """
        Chunk content into smaller pieces with overlap
        """
        if chunk_size is None:
            chunk_size = self.default_chunk_size
        if overlap is None:
            overlap = self.default_overlap
        
        chunks = []
        
        # Split content into paragraphs first
        paragraphs = self._split_into_paragraphs(content)
        
        current_chunk = ""
        current_pos = 0
        
        for para in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                # Save the current chunk
                chunks.append({
                    'text': current_chunk.strip(),
                    'start_pos': current_pos,
                    'end_pos': current_pos + len(current_chunk),
                    'chunk_size': len(current_chunk)
                })
                
                # Start new chunk with overlap
                if overlap > 0:
                    # Take the end of the current chunk for overlap
                    overlap_text = current_chunk[-overlap:]
                    current_chunk = overlap_text + para
                    current_pos = current_pos + len(current_chunk) - len(para) - overlap
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
                'end_pos': current_pos + len(current_chunk),
                'chunk_size': len(current_chunk)
            })
        
        return chunks
    
    def _split_into_paragraphs(self, content: str) -> List[str]:
        """
        Split content into paragraphs
        """
        # Split on double newlines first
        paragraphs = content.split('\n\n')
        
        # Clean up paragraphs
        cleaned_paragraphs = []
        for para in paragraphs:
            # Remove extra whitespace but preserve the structure
            cleaned_para = para.strip()
            if cleaned_para:  # Only add non-empty paragraphs
                cleaned_paragraphs.append(cleaned_para)
        
        return cleaned_paragraphs
    
    def chunk_with_semantic_boundaries(self, content: str, max_chunk_size: int = None) -> List[Dict[str, Any]]:
        """
        Chunk content while trying to respect semantic boundaries (sentences, etc.)
        """
        if max_chunk_size is None:
            max_chunk_size = self.default_chunk_size
        
        chunks = []
        
        # Split into sentences first
        sentences = self._split_into_sentences(content)
        
        current_chunk = ""
        current_pos = 0
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
                # Save the current chunk
                chunks.append({
                    'text': current_chunk.strip(),
                    'start_pos': current_pos,
                    'end_pos': current_pos + len(current_chunk),
                    'chunk_size': len(current_chunk)
                })
                
                # Start a new chunk with this sentence
                current_chunk = sentence
                current_pos = current_pos + len(current_chunk) - len(sentence)
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the final chunk if it has content
        if current_chunk.strip():
            chunks.append({
                'text': current_chunk.strip(),
                'start_pos': current_pos,
                'end_pos': current_pos + len(current_chunk),
                'chunk_size': len(current_chunk)
            })
        
        return chunks
    
    def _split_into_sentences(self, content: str) -> List[str]:
        """
        Split content into sentences
        """
        # Use regex to split on sentence boundaries
        # This pattern looks for sentence endings followed by whitespace and capital letters
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(sentence_pattern, content)
        
        # Clean up sentences
        cleaned_sentences = []
        for sentence in sentences:
            cleaned_sentence = sentence.strip()
            if cleaned_sentence:
                cleaned_sentences.append(cleaned_sentence)
        
        return cleaned_sentences

# Global instance
text_chunker = TextChunker()
