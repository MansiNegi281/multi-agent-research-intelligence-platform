from google import genai

from backend.config import GOOGLE_API_KEY
from backend.agents.retrieval_agent import RetrievalAgent


class CompareAgent:

    def __init__(self):

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        self.retriever = RetrievalAgent()

    def compare(
        self,
        paper1: str,
        paper2: str
    ):

        first = self.retriever.retrieve(
            paper1,
            top_k=8
        )

        second = self.retriever.retrieve(
            paper2,
            top_k=8
        )

        docs1 = "\n\n".join(
            first["documents"]
        )

        docs2 = "\n\n".join(
            second["documents"]
        )

        prompt = f"""
You are an expert research assistant.

Compare the following two research papers.

Return the comparison as a markdown table.

Use these rows:

| Aspect | Paper 1 | Paper 2 |
|---------|---------|---------|
| Problem Addressed |
| Methodology |
| Dataset |
| Model |
| Key Contributions |
| Results |
| Advantages |
| Limitations |

Paper 1:
{docs1}

Paper 2:
{docs2}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text