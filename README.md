# 📚 Multi-Agent Research Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit)
![Gemini](https://img.shields.io/badge/Google-Gemini-blue?logo=google)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-purple)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-Embeddings-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

An end-to-end **AI-powered Multi-Agent Research Assistant** that enables users to search research papers, upload PDFs, build a vector knowledge base, generate AI summaries, compare research papers, and ask context-aware questions using **Retrieval-Augmented Generation (RAG)**.

The system combines **FastAPI**, **Streamlit**, **Gemini 2.5 Flash**, **ChromaDB**, **Sentence Transformers**, and **Cross-Encoder Re-ranking** to deliver accurate, explainable, and conversational responses from research papers.

---

## 🚀 Features

### 🔍 Research Paper Search
- Search research papers using the Semantic Scholar API.
- View paper title, authors, publication date, abstract, and PDF link.

### 📄 PDF Upload & Processing
- Upload your own research papers.
- Automatically extract text from PDFs.
- Chunk documents for efficient retrieval.

### 🧠 Vector Knowledge Base
- Store document embeddings in ChromaDB.
- Semantic search using Sentence Transformers.
- Persistent vector database for future queries.

### 🤖 AI Question Answering
- Retrieval-Augmented Generation (RAG)
- Context-aware answers using Gemini 2.5 Flash
- Multi-turn conversational memory
- Answers grounded in retrieved research papers

### 📊 Paper Comparison
- Compare two research papers.
- Highlight similarities, differences, methodologies, and contributions.

### 📝 AI Paper Summarization
- Generate concise summaries of research papers.
- Easy understanding of long technical documents.

### 🔎 Explainable Retrieval
- Cross-Encoder Re-ranking
- Retrieved evidence display
- Confidence scores
- Source attribution for every answer

### 💬 Conversation History
- Maintain chat history
- Follow-up questions supported
- Clear conversation option

---

# 🏗️ System Architecture

```
                     User
                       │
                       ▼
              Streamlit Frontend
                       │
                       ▼
                 FastAPI Backend
       ┌────────────┼────────────┐
       ▼            ▼            ▼
 Search Agent   Reader Agent   QA Agent
       │            │            │
       ▼            ▼            ▼
Semantic      PDF Extraction  Retrieval
Scholar API                    Agent
                                │
                                ▼
                     Sentence Transformer
                                │
                                ▼
                           ChromaDB
                                │
                                ▼
                    CrossEncoder Re-ranking
                                │
                                ▼
                        Gemini 2.5 Flash
                                │
                                ▼
                           Final Answer
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- Uvicorn

## Frontend

- Streamlit

## AI & NLP

- Google Gemini 2.5 Flash
- Sentence Transformers
- CrossEncoder
- LangChain Memory

## Vector Database

- ChromaDB

## PDF Processing

- PyMuPDF
- PyPDF2

## APIs

- Semantic Scholar API
- Gemini API

---

# 📂 Project Structure

```
multi-agent-research-assistant/

│

├── backend/
│   ├── agents/
│   │   ├── search_agent.py
│   │   ├── reader_agent.py
│   │   ├── embedding_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── qa_agent.py
│   │   ├── compare_agent.py
│   │   └── summary_agent.py
│   │
│   ├── uploads/
│   ├── data/
│   ├── app.py
│   └── config.py
│
├── frontend/
│   └── app.py
│
├── screenshots/
│
├── requirements.txt
├── README.md
├── Dockerfile
└── docker-compose.yml
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/multi-agent-research-assistant.git

cd multi-agent-research-assistant
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API Key

Create a `.env` file.

```
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## 5. Start FastAPI

```bash
uvicorn backend.app:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## 6. Start Streamlit

```bash
streamlit run frontend/app.py
```

Frontend:

```
http://localhost:8501
```

---

# 📖 Usage

## Search Papers

Search any research topic.

Example:

```
Vision Transformers
```

---

## Embed Paper

Select a paper.

Click

```
Embed Paper
```

The paper is stored inside ChromaDB.

---

## Upload Your Own PDF

Use the sidebar to upload custom research papers.

---

## Ask Questions

Example:

```
What is self attention?
```

The assistant retrieves relevant chunks and answers using Gemini.

---

## Compare Papers

Select two papers.

Click

```
Compare Papers
```

The AI generates a comparison highlighting methodologies, findings, and contributions.

---

# 📸 Screenshots

### Home Page

_Add screenshot here_

---

### Paper Search

_Add screenshot here_

---

### AI Summary

_Add screenshot here_

---

### Paper Comparison

_Add screenshot here_

---

### Question Answering

_Add screenshot here_

---

### Retrieved Evidence

_Add screenshot here_

---

# 📊 Future Improvements

- Hybrid Search (BM25 + Dense Retrieval)
- Literature Review Generator
- Citation-aware Responses
- User Authentication
- Research Workspace Management
- Docker Deployment
- Cloud Deployment
- Research Notes
- Export to PDF
- Export to Markdown

---

# 📈 Resume Highlights

- Developed an end-to-end Multi-Agent Research Assistant using FastAPI, Streamlit, Gemini API, ChromaDB, and Sentence Transformers.
- Implemented Retrieval-Augmented Generation (RAG) with semantic search, CrossEncoder re-ranking, and conversational memory for context-aware research assistance.
- Built AI-powered modules for paper summarization, comparison, PDF ingestion, semantic retrieval, and explainable question answering with source attribution.

---

# 🤝 Contributing

Contributions are welcome.

Feel free to fork the repository, create a feature branch, and submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👩‍💻 Author

**Mansi Negi**

B.Tech Computer Science (AI & ML)

Manipal University Jaipur
