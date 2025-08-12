"""
VectorDB: Wrapper for vector database operations using ChromaDB
ChromaDB provides persistent local vector storage with embedding capabilities.
"""

import os
import logging
import chromadb
from chromadb.config import Settings
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self):
        self.client = None
        self.collection = None
        self.available = False
        self.collection_name = settings.CHROMA_COLLECTION_NAME
        
        try:
            # Initialize ChromaDB with persistent storage and disabled telemetry
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_DB_PATH,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                    chroma_server_nofile=True
                )
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(
                    name=self.collection_name
                )
                logger.info(f"Connected to existing ChromaDB collection: {self.collection_name}")
            except Exception:
                # Collection doesn't exist, create it
                self.collection = self.client.create_collection(
                    name=self.collection_name
                )
                logger.info(f"Created new ChromaDB collection: {self.collection_name}")
            
            # Test the collection
            self.collection.count()
            self.available = True
            logger.info("ChromaDB vector database initialized successfully")
                
        except Exception as e:
            logger.warning(f"Failed to initialize ChromaDB: {e}")
            logger.warning("Vector search will be disabled. System will fallback to direct search.")

    def search(self, query_text: str, top_k: int = 5):
        """Search for similar content using text query. Returns empty list if ChromaDB is unavailable."""
        if not self.available or not self.collection:
            logger.debug("Vector search skipped - ChromaDB not available")
            return []
        
        # Validate input
        if not query_text or not isinstance(query_text, str):
            logger.warning(f"Invalid query text for vector search: {query_text}")
            return []
        
        # Clean the query text
        query_text = str(query_text).strip()
        if not query_text:
            logger.warning("Empty query text after cleaning")
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=min(top_k, 10),  # Limit to reasonable number
                include=['metadatas', 'documents', 'distances']
            )
            
            # Format results
            formatted_results = []
            if results and 'metadatas' in results and results['metadatas'] and results['metadatas'][0]:
                for i, metadata in enumerate(results['metadatas'][0]):
                    result = {
                        'content': results['documents'][0][i] if results.get('documents') and results['documents'][0] else "",
                        'distance': results['distances'][0][i] if results.get('distances') and results['distances'][0] else 1.0,
                        **metadata
                    }
                    formatted_results.append(result)
            
            logger.debug(f"Vector search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.warning(f"Vector search failed: {e}")
            return []
    
    def store(self, documents: list, metadatas: list, ids: list):
        """Store documents with metadata in the database"""
        if not self.available or not self.collection:
            logger.warning("Vector storage skipped - ChromaDB not available")
            return False
        
        if not documents or not ids:
            logger.warning("Cannot store empty documents or ids")
            return False
        
        try:
            # Ensure all documents are strings
            clean_documents = [str(doc) for doc in documents]
            clean_ids = [str(id_val) for id_val in ids]
            
            self.collection.add(
                documents=clean_documents,
                metadatas=metadatas if metadatas else [{}] * len(documents),
                ids=clean_ids
            )
            logger.info(f"Successfully stored {len(documents)} documents")
            return True
        except Exception as e:
            logger.error(f"Failed to store documents: {e}")
            return False
    
    def store_with_embeddings(self, documents: list, embeddings: list, metadatas: list, ids: list):
        """Store documents with pre-computed embeddings"""
        if not self.available or not self.collection:
            logger.warning("Vector storage skipped - ChromaDB not available")
            return False
        
        if not documents or not ids or not embeddings:
            logger.warning("Cannot store empty documents, ids, or embeddings")
            return False
        
        try:
            # Ensure all documents are strings
            clean_documents = [str(doc) for doc in documents]
            clean_ids = [str(id_val) for id_val in ids]
            
            self.collection.add(
                documents=clean_documents,
                embeddings=embeddings,
                metadatas=metadatas if metadatas else [{}] * len(documents),
                ids=clean_ids
            )
            logger.info(f"Successfully stored {len(documents)} documents with embeddings")
            return True
        except Exception as e:
            logger.error(f"Failed to store documents with embeddings: {e}")
            return False
    
    def is_available(self):
        """Check if vector database is available for use"""
        return self.available
    
    def get_collection_info(self):
        """Get information about the collection"""
        if not self.available or not self.collection:
            return {"available": False, "count": 0, "name": self.collection_name, "path": settings.CHROMA_DB_PATH}
        
        try:
            count = self.collection.count()
            return {
                "available": True,
                "count": count,
                "name": self.collection_name,
                "path": settings.CHROMA_DB_PATH
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {"available": False, "count": 0, "error": str(e), "name": self.collection_name, "path": settings.CHROMA_DB_PATH}
    
    def reset_collection(self):
        """Reset the collection (delete all data)"""
        if not self.available or not self.client:
            logger.warning("Cannot reset collection - ChromaDB not available")
            return False
        
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name
            )
            logger.info(f"Reset ChromaDB collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to reset collection: {e}")
            return False