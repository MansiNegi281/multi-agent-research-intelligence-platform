from google import genai
from google.genai import types
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid

from backend.config import GOOGLE_API_KEY

EMBEDDING_MODEL = "gemini-embedding-001"


class EmbeddingAgent:

    def __init__(self):

        self.client_ai = genai.Client(
            api_key=GOOGLE_API_KEY
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

    def _embed_chunks(
        self,
        chunks: list,
        title: str,
        batch_size: int = 50
    ):

        all_embeddings = []

        for i in range(0, len(chunks), batch_size):

            batch = chunks[i:i + batch_size]

            result = self.client_ai.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                    title=title
                )
            )

            all_embeddings.extend(
                [e.values for e in result.embeddings]
            )

        return all_embeddings

    def store_document(
        self,
        text: str,
        title: str,
        authors: list,
        published: str,
        pdf_url: str
    ):

        chunks = self.splitter.split_text(text)

        embeddings = self._embed_chunks(chunks, title)

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