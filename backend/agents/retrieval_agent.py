from sentence_transformers import SentenceTransformer
import chromadb


class RetrievalAgent:

    def __init__(self):

        # Lazy-loaded embedding model
        self.model = None

        # ChromaDB
        self.client = chromadb.PersistentClient(
            path="data/embeddings"
        )

        self.collection = self.client.get_or_create_collection(
            name="research_papers"
        )

    # ---------------------------------------------------
    # Lazy load embedding model
    # ---------------------------------------------------

    def get_embedding_model(self):

        if self.model is None:

            self.model = SentenceTransformer(
                "paraphrase-MiniLM-L3-v2"
            )

        return self.model

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

        embedding_model = self.get_embedding_model()

        query_embedding = embedding_model.encode(
            query
        ).tolist()

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