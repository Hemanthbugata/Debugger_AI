import httpx
import google.generativeai as genai
from app.core.config import settings
import json as pyjson
import re

class RAGPipeline:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def run(self, user_query: str, context_posts: list) -> dict:
        """Run RAG with context from StackOverflow/Reddit posts"""
        context_text = ""
        sources = []
        
        for post in context_posts:
            context_text += f"\nTitle: {post.get('title','')}\n"
            if 'question_body' in post:
                context_text += f"Question: {post['question_body']}\n"
            elif 'body' in post:
                context_text += f"Post: {post['body']}\n"
            
            # Add answers/comments
            for idx, answer in enumerate(post.get('answers', [])):
                context_text += f"Answer {idx+1}: {answer}\n"
            for idx, comment in enumerate(post.get('comments', [])):
                if idx < 3:  # Limit comments to avoid token overflow
                    context_text += f"Comment {idx+1}: {comment}\n"
            
            context_text += f"Link: {post.get('link','')}\n---\n"
            
            # Collect sources
            if post.get('link') and post.get('title'):
                sources.append({
                    "title": post['title'],
                    "link": post['link']
                })

        prompt = (
            "You are an expert programming assistant. "
            "Given the following error or debugging query from a developer and real solutions from Stack Overflow and Reddit below, "
            "provide a comprehensive solution that includes:\n"
            "1. A clear summary of the problem\n"
            "2. A detailed fix with code examples if applicable\n"
            "3. Best practices and preventive measures\n"
            "\nDeveloper Input:\n"
            f"{user_query}\n"
            "\nRelevant Posts from StackOverflow and Reddit:\n"
            f"{context_text}\n"            "\nPlease provide a JSON response with keys: 'summary', 'fix', and 'sources' (empty list since sources will be added separately)."
        )

        return await self._call_gemini(prompt, sources)

    async def run_gemini_only(self, user_query: str) -> dict:
        """Fallback to Gemini-only solution when no relevant posts found"""
        prompt = (
            "You are an expert programming assistant. "
            "A developer has encountered an error or needs debugging help. "
            "Since no relevant solutions were found in StackOverflow or Reddit, "
            "please provide a comprehensive solution based on your knowledge:\n"
            "\nDeveloper Input:\n"
            f"{user_query}\n"
            "\nPlease provide:\n"
            "1. A clear analysis of the problem\n"
            "2. A detailed solution with code examples if applicable\n"
            "3. Best practices and preventive measures\n"
            "4. Common causes and troubleshooting steps\n"
            "\nRespond in JSON format with keys: 'summary', 'fix', and 'sources' (empty list)."
        )

        return await self._call_gemini(prompt, [])

    async def _call_gemini(self, prompt: str, sources: list) -> dict:
        """Make API call to Google Gemini"""
        try:
            # Use async approach for Gemini
            import asyncio
            loop = asyncio.get_event_loop()
            
            def _sync_generate():
                response = self.model.generate_content(prompt)
                return response.text
            
            # Run the sync function in a thread pool
            content = await loop.run_in_executor(None, _sync_generate)
            
            try:
                result = pyjson.loads(content)
            except Exception:
                # Try to extract JSON from the response
                match = re.search(r"\{.*\}", content, re.DOTALL)
                if match:
                    try:
                        result = pyjson.loads(match.group(0))
                    except:
                        result = {
                            "summary": "Error parsing AI response",
                            "fix": content,
                            "sources": []
                        }
                else:
                    result = {
                        "summary": "AI-generated solution",
                        "fix": content,
                        "sources": []
                    }
            
            # Add sources from context
            if sources:
                result["sources"] = sources
            
            return result
        
        except Exception as e:
            # Fallback response if Gemini fails
            return {
                "summary": f"Error calling Gemini API: {str(e)}",
                "fix": "Please check your Gemini API key and try again. If the issue persists, check the error logs.",
                "sources": sources if sources else []
            }