"""
Data ingestion script to populate the vector database with StackOverflow and Reddit posts
This should be run periodically to keep the database updated with fresh content
"""

import asyncio
import logging
from typing import List
from app.ingestion.stackoverflow import StackOverflowRetriever
from app.ingestion.reddit import RedditRetriever
from app.retrieval.embedder import Embedder
from app.retrieval.vector_db import VectorDB

logger = logging.getLogger(__name__)

class DataIngestion:
    def __init__(self):
        self.so_retriever = StackOverflowRetriever()
        self.reddit_retriever = RedditRetriever()
        self.embedder = Embedder()
        self.vectordb = VectorDB()
        
        # Check if vector database is available
        if not self.vectordb.is_available():
            logger.warning("Vector database not available. Data ingestion will be disabled.")

    async def ingest_stackoverflow_data(self, queries: List[str], max_per_query: int = 20):
        """Ingest StackOverflow data for common programming errors"""
        if not self.vectordb.is_available():
            logger.warning("Vector database not available, skipping StackOverflow data ingestion")
            return 0
            
        all_vectors = []
        
        for query in queries:
            try:
                logger.info(f"Ingesting StackOverflow data for query: {query}")
                posts = await self.so_retriever.search_questions(query, max_results=max_per_query)
                
                for post in posts:
                    try:
                        # Create text for embedding
                        text_for_embedding = f"{post['title']} {post.get('question_body', '')} {' '.join(post.get('answers', [])[:2])}"
                        
                        # Generate embedding
                        embedding = await self.embedder.embed(text_for_embedding)
                        
                        # Prepare vector data
                        vector_data = {
                            "id": f"so_{post['link'].split('/')[-2]}",
                            "values": embedding,
                            "metadata": {
                                "title": post['title'],
                                "link": post['link'],
                                "source": "stackoverflow",
                                "tags": post.get('tags', []),
                                "score": post.get('score', 0),
                                "is_answered": post.get('is_answered', False)
                            }
                        }
                        all_vectors.append(vector_data)
                        
                    except Exception as e:
                        logger.error(f"Error processing StackOverflow post: {e}")
                        continue
                        
            except Exception as e:
                logger.error(f"Error searching StackOverflow for '{query}': {e}")
                continue        
        # Store vectors in batches
        if all_vectors:
            await self._store_vectors_in_batches(all_vectors)
        
        return len(all_vectors)

    async def ingest_reddit_data(self, queries: List[str], max_per_query: int = 20):
        """Ingest Reddit data for common programming discussions"""
        if not self.vectordb.is_available():
            logger.warning("Vector database not available, skipping Reddit data ingestion")
            return 0
            
        all_vectors = []
        
        for query in queries:
            try:
                logger.info(f"Ingesting Reddit data for query: {query}")
                posts = await self.reddit_retriever.search_posts(query, max_results=max_per_query)
                
                for post in posts:
                    try:
                        # Create text for embedding
                        text_for_embedding = f"{post['title']} {post.get('body', '')} {' '.join(post.get('comments', [])[:3])}"
                        
                        # Generate embedding
                        embedding = await self.embedder.embed(text_for_embedding)
                        
                        # Prepare vector data
                        vector_data = {
                            "id": f"reddit_{post['link'].split('/')[-3]}",
                            "values": embedding,
                            "metadata": {
                                "title": post['title'],
                                "link": post['link'],
                                "source": "reddit",
                                "subreddit": post.get('subreddit', ''),
                                "score": post.get('score', 0),
                                "upvote_ratio": post.get('upvote_ratio', 0)
                            }
                        }
                        all_vectors.append(vector_data)
                        
                    except Exception as e:
                        logger.error(f"Error processing Reddit post: {e}")
                        continue
                        
            except Exception as e:
                logger.error(f"Error searching Reddit for '{query}': {e}")
                continue
        
        # Store vectors in batches
        if all_vectors:
            await self._store_vectors_in_batches(all_vectors)
        
        return len(all_vectors)

    async def _store_vectors_in_batches(self, vectors: List[dict], batch_size: int = 100):
        """Store vectors in batches to avoid API limits"""
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            try:
                self.vectordb.store(batch)
                logger.info(f"Stored batch of {len(batch)} vectors")
            except Exception as e:
                logger.error(f"Error storing batch: {e}")

    async def run_full_ingestion(self):
        """Run complete data ingestion for common programming errors and topics"""
        
        # Common programming error queries
        error_queries = [
            "TypeError python",
            "AttributeError python",
            "SyntaxError python",
            "ImportError python",
            "KeyError python",
            "IndexError python",
            "ValueError python",
            "NameError python",
            "ReferenceError javascript",
            "TypeError javascript",
            "SyntaxError javascript",
            "RangeError javascript",
            "NullPointerException java",
            "ArrayIndexOutOfBoundsException java",
            "ClassNotFoundException java",
            "NoSuchMethodError java",
            "SegmentationFault c++",
            "CompileError c++",
            "MemoryLeak c++",
            "react error",
            "node.js error",
            "django error",
            "flask error",
            "express error",
            "database connection error",
            "SQL error",
            "API error",
            "authentication error",
            "CORS error",
            "deployment error"
        ]
        
        logger.info("Starting full data ingestion...")
        
        # Ingest StackOverflow data
        so_count = await self.ingest_stackoverflow_data(error_queries, max_per_query=15)
        logger.info(f"Ingested {so_count} StackOverflow posts")
        
        # Ingest Reddit data
        reddit_count = await self.ingest_reddit_data(error_queries, max_per_query=10)
        logger.info(f"Ingested {reddit_count} Reddit posts")
        
        total_count = so_count + reddit_count
        logger.info(f"Total ingestion complete: {total_count} posts")
        
        return total_count

# CLI script to run ingestion
async def main():
    logging.basicConfig(level=logging.INFO)
    ingestion = DataIngestion()
    await ingestion.run_full_ingestion()

if __name__ == "__main__":
    asyncio.run(main())
