from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb


class RetrievalAgent:

    def __init__(self):

        # Embedding model
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # Cross Encoder for re-ranking
        self.reranker = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        # ChromaDB
        self.client = chromadb.PersistentClient(
            path="data/embeddings"
        )

        self.collection = self.client.get_or_create_collection(
            name="research_papers"
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 15
    ):

        if self.collection.count() == 0:
            return {
                "documents": [],
                "metadata": [],
                "distances": [],
                "rerank_scores": []
            }

        # -----------------------------------------
        # Generate query embedding
        # -----------------------------------------

        query_embedding = self.model.encode(
            query
        ).tolist()

        # -----------------------------------------
        # Retrieve Top-K from ChromaDB
        # -----------------------------------------

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

        # -----------------------------------------
        # Cross Encoder Re-ranking
        # -----------------------------------------

        pairs = [
            (query, doc)
            for doc in documents
        ]

        scores = self.reranker.predict(
            pairs
        )

        ranked = sorted(
            zip(
                scores,
                documents,
                metadata,
                distances
            ),
            key=lambda x: x[0],
            reverse=True
        )

        # Keep Top-5 after reranking
        ranked = ranked[:5]

        documents = [
            item[1]
            for item in ranked
        ]

        metadata = [
            item[2]
            for item in ranked
        ]

        distances = [
            item[3]
            for item in ranked
        ]

        rerank_scores = [
            float(item[0])
            for item in ranked
        ]

        return {
            "documents": documents,
            "metadata": metadata,
            "distances": distances,
            "rerank_scores": rerank_scores
        }