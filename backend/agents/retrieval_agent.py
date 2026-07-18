from google import genai
from google.genai import types
import chromadb

from backend.config import GOOGLE_API_KEY

EMBEDDING_MODEL = "gemini-embedding-001"


class RetrievalAgent:

    def __init__(self):

        self.client_ai = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        # ChromaDB
        self.client = chromadb.PersistentClient(
            path="data/embeddings"
        )

        self.collection = self.client.get_or_create_collection(
            name="research_papers"
        )

    # ---------------------------------------------------
    # Embed a query using Gemini
    # ---------------------------------------------------

    def embed_query(self, query: str):

        result = self.client_ai.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=query,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY"
            )
        )

        return result.embeddings[0].values

    # ---------------------------------------------------
    # Retrieve Documents
    # ---------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        if self.collection.count() == 0:

            return {
                "documents": [],
                "metadata": [],
                "distances": [],
                "rerank_scores": []
            }

        query_embedding = self.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        documents = results["documents"][0]
        metadata = results["metadatas"][0]
        distances = results["distances"][0]

        if len(documents) == 0:

            return {
                "documents": [],
                "metadata": [],
                "distances": [],
                "rerank_scores": []
            }

        # No CrossEncoder on Render Free
        rerank_scores = [1.0] * len(documents)

        return {
            "documents": documents,
            "metadata": metadata,
            "distances": distances,
            "rerank_scores": rerank_scores
        }