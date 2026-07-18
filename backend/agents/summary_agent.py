from google import genai

from backend.config import GOOGLE_API_KEY
from backend.agents.retrieval_agent import RetrievalAgent


class SummaryAgent:

    def __init__(self):

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        self.retriever = RetrievalAgent()

    def summarize(self, title: str):

        # Retrieve chunks related to the paper title
        retrieved = self.retriever.retrieve(
            query=title,
            top_k=10
        )

        docs = retrieved.get("documents", [])

        if len(docs) == 0:
            return "No content found for this paper."

        context = "\n\n".join(docs)

        prompt = f"""
You are an expert AI Research Assistant.

Read the following research paper excerpts and generate a structured summary.

Your summary must contain exactly these sections:

## Overview

## Problem Addressed

## Methodology

## Key Contributions

## Results

## Limitations

Keep the summary concise (around 300–500 words).

Research Paper:

{context}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text