import asyncpraw
from app.core.config import settings

class RedditRetriever:
    def __init__(self):
        self.reddit = asyncpraw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USER_AGENT
        )

    async def search_posts(self, query: str, subreddits=None, max_results: int = 10):
        """Search Reddit posts based on query in programming-related subreddits"""
        if subreddits is None:
            subreddits = ["programming", "learnprogramming", "webdev", "javascript", "python", 
                         "reactjs", "MachineLearning", "datascience", "AskProgramming", "djangolearning"]
        
        results = []
        for subreddit_name in subreddits:
            try:
                subreddit = await self.reddit.subreddit(subreddit_name)
                async for submission in subreddit.search(query, limit=max_results//len(subreddits)):
                    post_data = await self.fetch_post(submission.id)
                    if post_data:
                        results.append(post_data)
                        if len(results) >= max_results:
                            break
            except Exception as e:
                print(f"Error searching in r/{subreddit_name}: {e}")
                continue
            
            if len(results) >= max_results:
                break
                
        return results

    async def fetch_post(self, post_id: str):
        try:
            submission = await self.reddit.submission(id=post_id)
            await submission.load()
            await submission.comments.replace_more(limit=0)
            return {
                "title": submission.title,
                "body": submission.selftext,
                "comments": [comment.body for comment in submission.comments.list()[:10]],  # Limit comments
                "link": f"https://reddit.com{submission.permalink}",
                "subreddit": str(submission.subreddit),
                "score": submission.score,
                "upvote_ratio": submission.upvote_ratio,
            }
        except Exception as e:
            print(f"Error fetching Reddit post {post_id}: {e}")
            return None
