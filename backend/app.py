from fastapi import FastAPI, UploadFile, File

from backend.agents.search_agent import SearchAgent
from backend.agents.reader_agent import ReaderAgent
from backend.agents.embedding_agent import EmbeddingAgent
from backend.agents.retrieval_agent import RetrievalAgent
from backend.agents.qa_agent import QAAgent
from backend.agents.summary_agent import SummaryAgent
from backend.agents.compare_agent import CompareAgent

app = FastAPI(
    title="Multi-Agent Research Assistant",
    version="2.0.0"
)

# =====================================================
# Initialize Agents
# =====================================================

search_agent = SearchAgent()
reader = ReaderAgent()
embedding_agent = EmbeddingAgent()
retriever = RetrievalAgent()
qa_agent = QAAgent()
summary_agent = SummaryAgent()
compare_agent = CompareAgent()
# =====================================================
# Home
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Research Assistant API Running"
    }

# =====================================================
# Search Papers
# =====================================================

@app.get("/search")
def search(query: str):

    papers = search_agent.search_papers(query)

    return {
        "query": query,
        "results": papers
    }

# =====================================================
# Read PDF
# =====================================================

@app.get("/read")
def read_pdf(pdf_url: str):

    pdf_path = reader.download_pdf(pdf_url)

    text = reader.extract_text(pdf_path)

    return {
        "characters": len(text),
        "preview": text[:1000]
    }

# =====================================================
# Embed Paper from arXiv
# =====================================================

@app.post("/embed")
def embed_document(
    pdf_url: str,
    title: str,
    authors: str,
    published: str
):

    pdf_path = reader.download_pdf(pdf_url)

    text = reader.extract_text(pdf_path)

    if not text.strip():

        return {
            "error": "Could not extract text from PDF."
        }

    chunks = embedding_agent.store_document(
        text=text,
        title=title,
        authors=authors.split(", "),
        published=published,
        pdf_url=pdf_url
    )

    return {
        "paper": title,
        "chunks_created": chunks,
        "status": "Stored in ChromaDB"
    }

# =====================================================
# Upload PDF
# =====================================================

@app.post("/upload")
def upload_pdf(
    file: UploadFile = File(...)
):

    pdf_path = reader.save_uploaded_file(file)

    text = reader.extract_text(pdf_path)

    if not text.strip():

        return {
            "error": "Could not extract text from uploaded PDF."
        }

    chunks = embedding_agent.store_document(
        text=text,
        title=file.filename,
        authors=["Uploaded File"],
        published="Unknown",
        pdf_url="Uploaded by User"
    )

    return {
        "status": "PDF uploaded successfully.",
        "chunks_created": chunks
    }

# =====================================================
# Retrieve
# =====================================================

@app.get("/retrieve")
def retrieve(query: str):

    results = retriever.retrieve(query)

    return {
        "query": query,
        "results": results
    }

# =====================================================
# Ask
# =====================================================

@app.get("/ask")
def ask(question: str):

    result = qa_agent.answer(question)

    return {

        "question": question,

        "answer": result["answer"],

        "sources": result["sources"],

        "chunks": result["chunks"],

        "scores": result["scores"],

        "distances": result["distances"]

    }

# =====================================================
# Stats
# =====================================================

@app.get("/stats")
def stats():

    return {
        "chunks": embedding_agent.collection.count()
    }

# =====================================================
# Clear Memory
# =====================================================

@app.post("/clear_memory")
def clear_memory():

    qa_agent.memory.clear()

    return {
        "status": "Conversation cleared successfully."
    }


@app.get("/summary")
def summary(title: str):

    summary = summary_agent.summarize(title)

    return {
        "title": title,
        "summary": summary
    }

@app.get("/compare")
def compare(
    paper1: str,
    paper2: str
):

    comparison = compare_agent.compare(
        paper1,
        paper2
    )

    return {
        "paper1": paper1,
        "paper2": paper2,
        "comparison": comparison
    }