"""
Utility functions and setup helpers for the Debugger AI project
"""

import asyncio
import logging
from typing import Dict, Any
from app.core.config import settings
from app.ingestion.stackoverflow import StackOverflowRetriever
from app.ingestion.reddit import RedditRetriever
from app.generation.rag import RAGPipeline

logger = logging.getLogger(__name__)

class DebuggerAIUtils:
    """Utility class for testing and setup"""
    
    @staticmethod
    async def test_gemini_connection():
        """Test Google Gemini API connection"""
        try:
            rag = RAGPipeline()
            result = await rag.run_gemini_only("print('hello world') gives NameError")
            if result and 'summary' in result:
                return True, "Gemini connection successful"
            else:
                return False, "Gemini returned invalid response"
        except Exception as e:
            return False, f"Gemini connection failed: {e}"
    
    @staticmethod
    async def test_stackoverflow_api():
        """Test StackOverflow API connection"""
        try:
            so = StackOverflowRetriever()
            results = await so.search_questions("python error", max_results=1)
            return True, f"StackOverflow API working, found {len(results)} results"
        except Exception as e:
            return False, f"StackOverflow API failed: {e}"
    
    @staticmethod
    async def test_reddit_api():
        """Test Reddit API connection"""
        try:
            reddit = RedditRetriever()
            results = await reddit.search_posts("python help", max_results=1)
            return True, f"Reddit API working, found {len(results)} results"
        except Exception as e:
            return False, f"Reddit API failed: {e}"
    
    @staticmethod
    async def test_vector_database():
        """Test vector database (Pinecone) connection"""
        try:
            from app.retrieval.vector_db import VectorDB
            vectordb = VectorDB()
            if vectordb.is_available():
                return True, "Vector database (Pinecone) connected successfully"
            else:
                return False, "Vector database not available (API key missing or service unavailable)"
        except Exception as e:
            return False, f"Vector database connection failed: {e}"
    
    @staticmethod
    async def test_all_connections():
        """Test all API connections"""
        results = {}
        
        print("Testing API connections...")
        
        # Test Gemini
        success, message = await DebuggerAIUtils.test_gemini_connection()
        results['gemini'] = {'success': success, 'message': message}
        print(f"Gemini: {'✓' if success else '✗'} {message}")
        
        # Test StackOverflow
        success, message = await DebuggerAIUtils.test_stackoverflow_api()
        results['stackoverflow'] = {'success': success, 'message': message}
        print(f"StackOverflow: {'✓' if success else '✗'} {message}")
        
        # Test Reddit
        success, message = await DebuggerAIUtils.test_reddit_api()
        results['reddit'] = {'success': success, 'message': message}
        print(f"Reddit: {'✓' if success else '✗'} {message}")
        
        # Test Vector Database
        success, message = await DebuggerAIUtils.test_vector_database()
        results['vector_database'] = {'success': success, 'message': message}
        print(f"Vector Database: {'✓' if success else '✗'} {message}")
        
        return results
    
    @staticmethod
    async def demo_debug_request(error_message: str, code: str = None):
        """Demo a complete debug request"""
        print(f"\n=== Debug Demo ===")
        print(f"Error: {error_message}")
        if code:
            print(f"Code: {code}")
        
        try:
            # Import here to avoid circular imports
            from app.api.debug import debug_endpoint
            from app.models.debug import DebugRequest
            
            request = DebugRequest(error=error_message, code=code)
            result = await debug_endpoint(request)
            
            print(f"\n=== Results ===")
            print(f"Summary: {result.summary}")
            print(f"Fix: {result.fix}")
            print(f"Sources: {len(result.sources)} found")
            for i, source in enumerate(result.sources):
                print(f"  {i+1}. {source.title} - {source.link}")
            
            return result
            
        except Exception as e:
            print(f"Demo failed: {e}")
            return None

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

async def main():
    """Main utility script"""
    setup_logging()
    
    print("=== Debugger AI Utility Script ===\n")
    
    # Test connections
    await DebuggerAIUtils.test_all_connections()
    
    # Demo requests
    print("\n=== Running Demo ===")
    
    demo_cases = [
        {
            "error": "NameError: name 'pd' is not defined",
            "code": "df = pd.DataFrame({'A': [1, 2, 3]})"
        },
        {
            "error": "TypeError: 'str' object has no attribute 'append'",
            "code": "my_list = 'hello'\nmy_list.append('world')"
        }
    ]
    
    for case in demo_cases:
        await DebuggerAIUtils.demo_debug_request(case["error"], case.get("code"))
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())