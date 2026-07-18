from google import genai

from langchain.memory import ConversationBufferMemory

from backend.config import GOOGLE_API_KEY
from backend.agents.retrieval_agent import RetrievalAgent


class QAAgent:

    def __init__(self):

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        self.retriever = RetrievalAgent()

        self.memory = ConversationBufferMemory(
            return_messages=False
        )

    def answer(
        self,
        question: str
    ):

        retrieved = self.retriever.retrieve(question)

        docs = retrieved["documents"]
        metadata = retrieved["metadata"]
        distances = retrieved["distances"]
        rerank_scores = retrieved["rerank_scores"]

        if len(docs) == 0:

            return {
                "answer": "No papers have been embedded yet.",
                "sources": [],
                "chunks": [],
                "scores": []
            }

        conversation = self.memory.load_memory_variables({})

        history = conversation.get(
            "history",
            ""
        )

        context = "\n\n".join(docs)

        print("=" * 80)
        print("Retrieved Context")
        print("=" * 80)
        print(context)

        print("=" * 80)
        print("CrossEncoder Scores")
        print("=" * 80)
        print(rerank_scores)

        prompt = f"""
You are an expert AI Research Assistant.

Previous Conversation:

{history}

Research Context:

{context}

Current Question:

{question}

Instructions:

1. Answer ONLY using the research context.

2. Explain naturally.

3. If multiple papers contribute,
combine their findings.

4. If the answer is not found,
say:

"I could not find the answer in the research papers."
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = (
            response.text
            if response.text
            else "No response generated."
        )

        self.memory.save_context(
            {"input": question},
            {"output": answer}
        )

        return {

            "answer": answer,

            "sources": metadata,

            "chunks": docs,

            "scores": rerank_scores,

            "distances": distances

        }