from google import genai

from backend.config import GOOGLE_API_KEY
from backend.agents.retrieval_agent import RetrievalAgent


class ComparisonAgent:

    def __init__(self):
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.retriever = RetrievalAgent()

    def compare(self, query: str):

        retrieved = self.retriever.retrieve(query, top_k=10)

        docs = retrieved["documents"]

        metadata = retrieved["metadata"]

        context = "\n\n".join(docs)

        prompt = f"""
You are an AI Research Assistant.

Using ONLY the research paper excerpts below,
compare the different approaches, methods,
advantages and limitations.

Context:

{context}

User Query:

{query}

Return the comparison in markdown table format.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "comparison": response.text,
            "sources": metadata
        }