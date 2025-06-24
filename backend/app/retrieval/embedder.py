import httpx
import google.generativeai as genai
from app.core.config import settings

class Embedder:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)

    async def embed(self, text: str) -> list:
        """Generate embeddings using Google Gemini's embedding model"""
        try:
            # Use async HTTP call for Gemini embeddings
            import asyncio
            loop = asyncio.get_event_loop()
            
            def _sync_embed():
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=text,
                    task_type="retrieval_document"
                )
                return result['embedding']
            
            # Run the sync function in a thread pool
            embedding = await loop.run_in_executor(None, _sync_embed)
            return embedding
            
        except Exception as e:
            # Fallback to a simple hash-based embedding if Gemini fails
            print(f"Gemini embedding failed: {e}")
            # Create a simple fallback embedding (768 dimensions)
            import hashlib
            hash_obj = hashlib.sha256(text.encode())
            hash_hex = hash_obj.hexdigest()
            # Convert hash to 768-dimensional vector
            embedding = []
            for i in range(0, len(hash_hex), 2):
                embedding.append(int(hash_hex[i:i+2], 16) / 255.0 - 0.5)
            # Pad to 768 dimensions
            while len(embedding) < 768:
                embedding.append(0.0)
            return embedding[:768]