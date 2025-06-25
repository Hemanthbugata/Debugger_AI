from fastapi import APIRouter, HTTPException
from app.models.debug import DebugRequest, DebugResponse, SourceReference
from app.core.preprocessor import InputPreprocessor
from app.retrieval.embedder import Embedder
from app.retrieval.vector_db import VectorDB
from app.ingestion.stackoverflow import StackOverflowRetriever
from app.ingestion.reddit import RedditRetriever
from app.generation.rag import RAGPipeline
import logging
import httpx

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=DebugResponse)
async def debug_endpoint(request: DebugRequest):
    """
    Main debugging endpoint that:
    1. Preprocesses the error
    2. Searches StackOverflow and Reddit for similar issues (top 5)
    3. Uses vector database for semantic search (if available)
    4. Combines results with Google Gemini to generate a comprehensive solution
    5. Falls back to pure Gemini if no relevant results found
    6. If Gemini is rate limited, returns StackOverflow/Reddit results only
    """
    try:
        # Step 1: Preprocess the input
        preprocessor = InputPreprocessor()
        context = preprocessor.preprocess(request.error)

        # Step 2: Search StackOverflow and Reddit directly
        so_retriever = StackOverflowRetriever()
        reddit_retriever = RedditRetriever()

        # Create search query from error and context
        search_query = f"{context['clean_error']} {context.get('language', '')} {context.get('library', '')}"

        # Search both platforms (top 5 each)
        try:
            so_results = await so_retriever.search_questions(search_query, max_results=5)
        except Exception as e:
            logger.warning(f"StackOverflow search failed: {e}")
            so_results = []

        try:
            reddit_results = await reddit_retriever.search_posts(search_query, max_results=5)
        except Exception as e:
            logger.warning(f"Reddit search failed: {e}")
            reddit_results = []

        # Combine results (limit to 5 most relevant)
        all_results = (so_results + reddit_results)[:5]

        # Step 3: Try vector database search (if available)
        try:
            vectordb = VectorDB()
            if vectordb.is_available():
                embedder = Embedder()
                embedding = await embedder.embed(context['clean_error'])
                vector_results = vectordb.search(embedding, top_k=3)
                # Fetch full posts from vector search results
                for post_meta in vector_results:
                    if "stackoverflow.com" in post_meta.get('link', ''):
                        qid = int(post_meta['link'].split("/questions/")[1].split("/")[0])
                        full_post = await so_retriever.fetch_post(qid)
                        if full_post:
                            all_results.append(full_post)
                    elif "reddit.com" in post_meta.get('link', ''):
                        post_id = post_meta['link'].split("/comments/")[1].split("/")[0]
                        full_post = await reddit_retriever.fetch_post(post_id)
                        if full_post:
                            all_results.append(full_post)
                # Limit to 5 most relevant
                all_results = all_results[:5]
            else:
                logger.info("Vector database not available, skipping vector search")
        except Exception as e:
            logger.warning(f"Vector search failed, continuing with direct search: {e}")

        # Step 4: Generate response using RAG or fallback
        try:
            rag_pipeline = RAGPipeline()
            if all_results:
                # Use found results with RAG
                rag_result = await rag_pipeline.run(
                    user_query=request.error,
                    context_posts=all_results
                )
            else:
                # Fallback to pure Gemini if no results found
                logger.info("No relevant posts found, falling back to Gemini-only solution")
                rag_result = await rag_pipeline.run_gemini_only(
                    user_query=request.error
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                # Gemini rate limited - return results from StackOverflow/Reddit only
                logger.warning("Gemini rate limited, returning StackOverflow/Reddit results only")
                rag_result = _create_fallback_response(request, all_results, context)
            else:
                raise e
        except Exception as e:
            # Any other error with Gemini - try fallback
            logger.error(f"Gemini error, using fallback: {e}")
            rag_result = _create_fallback_response(request, all_results, context)

        # Step 5: Return structured response
        return DebugResponse(
            summary=rag_result.get("summary", ""),
            fix=rag_result.get("fix", ""),
            sources=[
                SourceReference(**src) for src in rag_result.get("sources", [])
            ]
        )

    except Exception as e:
        logger.error(f"Error in debug endpoint: {e}")
        # Return a basic error response instead of HTTP 500
        return DebugResponse(
            summary=f"Error processing request: {str(e)}",
            fix="Please try again or check your input format.",
            sources=[]
        )

def _create_fallback_response(request: DebugRequest, all_results: list, context: dict) -> dict:
    """Create a response when Gemini is not available"""
    if all_results:
        # Summarize StackOverflow/Reddit results
        summary = f"Found {len(all_results)} similar issues on StackOverflow and Reddit for error: {context['clean_error']}"
        # Use the first result as the most accurate
        first = all_results[0]
        fix = first.get('answer', 'See the linked post for details.')
        sources = [{
            'title': first.get('title', 'Source'),
            'link': first.get('link', '#')
        }]
    else:
        summary = "No relevant results found."
        fix = "No solution found. Please try rephrasing your error."
        sources = []
    return {
        "summary": summary,
        "fix": fix,
        "sources": sources
    }