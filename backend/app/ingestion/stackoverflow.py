import httpx
import urllib.parse

class StackOverflowRetriever:
    BASE_URL = "https://api.stackexchange.com/2.3"

    async def search_questions(self, query: str, max_results: int = 10):
        """Search StackOverflow questions based on query"""
        encoded_query = urllib.parse.quote(query)
        url = f"{self.BASE_URL}/search/advanced?order=desc&sort=relevance&q={encoded_query}&site=stackoverflow&filter=withbody"
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            
            results = []
            for item in data.get("items", [])[:max_results]:
                question_data = await self.fetch_post(item["question_id"])
                if question_data:
                    results.append(question_data)
            
            return results

    async def fetch_post(self, question_id: int):
        url = f"{self.BASE_URL}/questions/{question_id}?order=desc&sort=activity&site=stackoverflow&filter=withbody"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            if data["items"]:
                question = data["items"][0]
                answers_url = f"{self.BASE_URL}/questions/{question_id}/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody"
                ans_resp = await client.get(answers_url)
                ans_resp.raise_for_status()
                answers = ans_resp.json().get("items", [])
                return {
                    "title": question.get("title"),
                    "question_body": question.get("body"),
                    "answers": [a.get("body") for a in answers],
                    "link": question.get("link"),
                    "tags": question.get("tags"),
                    "score": question.get("score", 0),
                    "is_answered": question.get("is_answered", False),
                    "accepted_answer_id": question.get("accepted_answer_id"),
                }
            return None