from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb


class RetrievalAgent:

    def __init__(self):

        # Lazy-loaded models
        self.model = None
        self.reranker = None

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
                "all-MiniLM-L6-v2"
            )

        return self.model

    # ---------------------------------------------------
    # Lazy load CrossEncoder
    # ---------------------------------------------------

    def get_reranker(self):

        if self.reranker is None:

            self.reranker = CrossEncoder(
                "cross-encoder/ms-marco-MiniLM-L-6-v2"
            )

        return self.reranker

    # ---------------------------------------------------
    # Retrieve Documents
    # ---------------------------------------------------

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

        # Load embedding model only when needed
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

        # Load CrossEncoder only when needed
        reranker = self.get_reranker()

        pairs = [
            (query, doc)
            for doc in documents
        ]

        scores = reranker.predict(pairs)

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

        ranked = ranked[:5]

        documents = [x[1] for x in ranked]
        metadata = [x[2] for x in ranked]
        distances = [x[3] for x in ranked]
        rerank_scores = [float(x[0]) for x in ranked]

        return {
            "documents": documents,
            "metadata": metadata,
            "distances": distances,
            "rerank_scores": rerank_scores
        }