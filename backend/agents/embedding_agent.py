from sentence_transformers import SentenceTransformer
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid


class EmbeddingAgent:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path="data/embeddings"
        )

        self.collection = self.client.get_or_create_collection(
            name="research_papers"
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def store_document(
        self,
        text: str,
        title: str,
        authors: list,
        published: str,
        pdf_url: str
    ):

        chunks = self.splitter.split_text(text)

        embeddings = self.model.encode(chunks).tolist()

        ids = [str(uuid.uuid4()) for _ in chunks]

        metadata = []

        for i in range(len(chunks)):

            metadata.append(
                {
                    "title": title,
                    "authors": ", ".join(authors),
                    "published": published,
                    "pdf_url": pdf_url,
                    "chunk": str(i + 1)
                }
            )

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata
        )

        return len(chunks)