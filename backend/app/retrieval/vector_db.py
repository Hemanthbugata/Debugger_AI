"""
VectorDB: Wrapper for vector database operations (Pinecone, FAISS, etc.)
This example uses Pinecone for illustration with graceful fallback handling.
"""

import os
import logging
import pinecone
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self):
        self.index = None
        self.available = False
        self.index_name = "agent-debugger"
        
        # Only initialize if Pinecone API key is available
        if not settings.PINECONE_API_KEY:
            logger.info("Pinecone API key not provided, vector search disabled")
            return
        
        try:
            pinecone.init(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENV)
            
            # Check if index exists and try to create if not
            try:
                existing_indexes = pinecone.list_indexes()
                if self.index_name not in existing_indexes:
                    logger.info(f"Creating Pinecone index: {self.index_name}")
                    pinecone.create_index(self.index_name, dimension=768)
                
                self.index = pinecone.Index(self.index_name)
                # Test the connection with a simple describe call
                self.index.describe_index_stats()
                self.available = True
                logger.info("Pinecone vector database initialized successfully")
                
            except Exception as e:
                logger.warning(f"Failed to create/access Pinecone index: {e}")
                # Check if this is a pod limit error
                if "max pods allowed" in str(e).lower():
                    logger.warning("Pinecone pod limit reached. Consider upgrading your plan or using a different project.")
                elif "quota" in str(e).lower():
                    logger.warning("Pinecone quota exceeded. Vector search will be disabled.")
                else:
                    logger.warning(f"Pinecone initialization failed: {e}")
                
        except Exception as e:
            logger.warning(f"Failed to initialize Pinecone: {e}")

    def search(self, embedding: list, top_k: int = 5):
        """Search for similar vectors. Returns empty list if Pinecone is unavailable."""
        if not self.available or not self.index:
            logger.debug("Vector search skipped - Pinecone not available")
            return []
        
        try:
            res = self.index.query(vector=embedding, top_k=top_k, include_metadata=True)
            return [match["metadata"] for match in res["matches"]]
        except Exception as e:
            logger.warning(f"Vector search failed: {e}")
            return []
    
    def store(self, vectors_data: list):
        """Store vectors with metadata in the database"""
        if not self.available or not self.index:
            logger.warning("Vector storage skipped - Pinecone not available")
            return False
        
        try:
            self.index.upsert(vectors_data)
            logger.info(f"Successfully stored {len(vectors_data)} vectors")
            return True
        except Exception as e:
            logger.error(f"Failed to store vectors: {e}")
            return False
    
    def is_available(self):
        """Check if vector database is available for use"""
        return self.available