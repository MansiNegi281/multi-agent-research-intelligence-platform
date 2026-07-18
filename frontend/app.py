import os
import streamlit as st
import requests

BACKEND = os.getenv(
    "BACKEND_URL",
    "https://multi-agent-research-intelligence.onrender.com"
)

st.set_page_config(
    page_title="Multi-Agent Research Intelligence Platform",
    layout="wide"
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Research Assistant")

# -----------------------------
# Statistics
# -----------------------------

try:

    response = requests.get(f"{BACKEND}/stats")

    if response.status_code == 200:

        stats = response.json()

        st.sidebar.metric(
            "Embedded Chunks",
            stats["chunks"]
        )

except:

    st.sidebar.error(
        "Backend not running."
    )

st.sidebar.divider()

# -----------------------------
# Clear Conversation
# -----------------------------

if st.sidebar.button("Clear Conversation"):

    response = requests.post(
        f"{BACKEND}/clear_memory"
    )

    if response.status_code == 200:

        st.sidebar.success(
            "Conversation cleared."
        )

st.sidebar.divider()

# -----------------------------
# Upload PDF
# -----------------------------

st.sidebar.subheader("Upload your own PDF")

uploaded_pdf = st.sidebar.file_uploader(
    "Choose a PDF",
    type=["pdf"]
)

if uploaded_pdf:

    if st.sidebar.button("Upload & Embed"):

        with st.spinner("Uploading PDF..."):

            response = requests.post(
                f"{BACKEND}/upload",
                files={
                    "file": (
                        uploaded_pdf.name,
                        uploaded_pdf,
                        "application/pdf"
                    )
                }
            )

            if response.status_code == 200:

                result = response.json()

                st.sidebar.success(
                    result["status"]
                )

                st.sidebar.info(
                    f"Stored {result['chunks_created']} chunks."
                )

            else:

                st.sidebar.error(
                    "Upload failed."
                )

# ==========================================================
# MAIN PAGE
# ==========================================================

st.title("Multi-Agent Research Intelligence Platform")

st.write(
    "Search research papers, embed them into your knowledge base, and ask questions."
)

# ==========================================================
# SEARCH PAPERS
# ==========================================================

st.header("Search Research Papers")

query = st.text_input(
    "Enter a research topic"
)

if st.button("Search"):

    if query.strip() == "":

        st.warning(
            "Please enter a search query."
        )

    else:

        with st.spinner("Searching papers..."):

            response = requests.get(
                f"{BACKEND}/search",
                params={
                    "query": query
                }
            )

            if response.status_code == 200:

                papers = response.json()["results"]

                if len(papers) == 0:

                    st.warning(
                        "No papers found."
                    )

                else:

                    st.session_state["papers"] = papers

            else:

                st.error(
                    "Backend error."
                )
# ==========================================================
# DISPLAY SEARCH RESULTS
# ==========================================================

if "papers" in st.session_state:

    papers = st.session_state["papers"]

    titles = [
        paper["title"]
        for paper in papers
    ]

    st.subheader("Select Papers")

    col1, col2 = st.columns(2)

    with col1:

        selected = st.selectbox(
            "Paper 1",
            titles,
            key="paper1"
        )

    with col2:

        remaining = [
            title
            for title in titles
            if title != selected
        ]

        if len(remaining) == 0:
            remaining = titles

        selected2 = st.selectbox(
            "Paper 2",
            remaining,
            key="paper2"
        )

    paper = papers[
        titles.index(selected)
    ]

    st.subheader(paper["title"])

    st.markdown(
        f"**Authors:** {', '.join(paper['authors'])}"
    )

    st.markdown(
        f"**Published:** {paper['published']}"
    )

    st.markdown("### Abstract")

    st.write(
        paper["summary"]
    )

    st.markdown(
        f"**PDF:** {paper['pdf_url']}"
    )

    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    # -----------------------------------------------------
    # Embed Paper
    # -----------------------------------------------------

    with col1:

        if st.button(
            "Embed Paper"
        ):

            with st.spinner(
                "Embedding paper..."
            ):

                response = requests.post(
                    f"{BACKEND}/embed",
                    params={
                        "pdf_url": paper["pdf_url"],
                        "title": paper["title"],
                        "authors": ", ".join(
                            paper["authors"]
                        ),
                        "published": paper["published"]
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        result["status"]
                    )

                    st.info(
                        f"Stored {result['chunks_created']} chunks."
                    )

                else:

                    st.error(
                        "Embedding failed."
                    )

    # -----------------------------------------------------
    # Generate Summary
    # -----------------------------------------------------

    with col2:

        if st.button(
            "Generate AI Summary"
        ):

            with st.spinner(
                "Generating summary..."
            ):

                response = requests.get(
                    f"{BACKEND}/summary",
                    params={
                        "title": paper["title"]
                    }
                )

                if response.status_code == 200:

                    summary = response.json()[
                        "summary"
                    ]

                    st.session_state[
                        "summary"
                    ] = summary

                else:

                    st.error(
                        "Summary generation failed."
                    )

    # -----------------------------------------------------
    # Compare Papers
    # -----------------------------------------------------

    with col3:

        if st.button(
            "Compare Papers"
        ):

            with st.spinner(
                "Comparing papers..."
            ):

                response = requests.get(
                    f"{BACKEND}/compare",
                    params={
                        "paper1": selected,
                        "paper2": selected2
                    }
                )

                if response.status_code == 200:

                    comparison = response.json()[
                        "comparison"
                    ]

                    st.session_state[
                        "comparison"
                    ] = comparison

                else:

                    st.error(
                        "Comparison failed."
                    )

    # =====================================================
    # SUMMARY
    # =====================================================

    if "summary" in st.session_state:

        st.divider()

        st.subheader(
            "AI Summary"
        )

        st.markdown(
            st.session_state[
                "summary"
            ]
        )

    # =====================================================
    # COMPARISON
    # =====================================================

    if "comparison" in st.session_state:

        st.divider()

        st.subheader(
            "Paper Comparison"
        )

        st.markdown(
            st.session_state[
                "comparison"
            ]
        )

st.divider()

# ==========================================================
# QUESTION ANSWERING
# ==========================================================

st.header("Ask Questions")

question = st.text_input(
    "Ask a question about all embedded papers"
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if st.button("Ask"):

    if question.strip() == "":

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner("Thinking..."):

            response = requests.get(
                f"{BACKEND}/ask",
                params={
                    "question": question
                }
            )

            if response.status_code == 200:

                result = response.json()

                answer = result["answer"]

                sources = result.get(
                    "sources",
                    []
                )

                chunks = result.get(
                    "chunks",
                    []
                )

                scores = result.get(
                    "scores",
                    []
                )

                distances = result.get(
                    "distances",
                    []
                )

                st.session_state["chat_history"].append(
                    {
                        "question": question,
                        "answer": answer,
                        "sources": sources,
                        "chunks": chunks,
                        "scores": scores,
                        "distances": distances
                    }
                )

            else:

                st.error(
                    "Backend error while generating answer."
                )

# ==========================================================
# CHAT HISTORY
# ==========================================================

if len(st.session_state["chat_history"]) > 0:

    st.divider()

    st.header("Conversation")

    for idx, chat in enumerate(
        reversed(st.session_state["chat_history"]),
        start=1
    ):

        st.markdown(
            f"## Question"
        )

        st.info(chat["question"])

        st.markdown(
            "## Answer"
        )

        st.success(chat["answer"])

        # =====================================================
        # RETRIEVED EVIDENCE
        # =====================================================

        chunks = chat.get(
            "chunks",
            []
        )

        scores = chat.get(
            "scores",
            []
        )

        distances = chat.get(
            "distances",
            []
        )

        if len(chunks) > 0:

            st.subheader(
                "Retrieved Evidence"
            )

            for i, chunk in enumerate(chunks):

                confidence = (
                    scores[i]
                    if i < len(scores)
                    else None
                )

                similarity = (
                    distances[i]
                    if i < len(distances)
                    else None
                )

                with st.expander(
                    f"Chunk {i+1}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        if confidence is not None:

                            st.metric(
                                "CrossEncoder Score",
                                f"{confidence:.3f}"
                            )

                    with col2:

                        if similarity is not None:

                            st.metric(
                                "Embedding Distance",
                                f"{similarity:.3f}"
                            )

                    st.write(chunk)

        # =====================================================
        # SOURCES
        # =====================================================

        sources = chat.get(
            "sources",
            []
        )

        if len(sources) > 0:

            st.subheader(
                "Sources Used"
            )

            shown = set()

            for source in sources:

                if not source:
                    continue

                title = source.get(
                    "title"
                )

                if not title:
                    continue

                if title in shown:
                    continue

                shown.add(title)

                with st.expander(
                    f"{title}"
                ):

                    authors = source.get(
                        "authors",
                        []
                    )

                    if isinstance(
                        authors,
                        list
                    ):
                        authors = ", ".join(authors)

                    st.write(
                        f"**Authors:** {authors}"
                    )

                    st.write(
                        f"**Published:** {source.get('published','Unknown')}"
                    )

                    pdf = source.get(
                        "pdf_url",
                        ""
                    )

                    if pdf:

                        st.markdown(
                            f"[Open PDF]({pdf})"
                        )

        st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        "Vector Database\n\nChromaDB"
    )

with col2:

    st.info(
        "LLM\n\nGemini 2.5 Flash"
    )

with col3:

    st.info(
        "Retrieval\n\nSentence Transformers + CrossEncoder"
    )

st.divider()

st.markdown(
    """
    <style>
    .footer {
        text-align: center;
        color: grey;
        padding-top: 20px;
        padding-bottom: 10px;
        font-size: 15px;
    }
    </style>

    <div class="footer">

    <h4>Multi-Agent Research Assistant</h4>

    Built with <b>FastAPI</b> • <b>Streamlit</b> •
    <b>Gemini</b> •
    <b>Sentence Transformers</b> •
    <b>CrossEncoder</b> •
    <b>ChromaDB</b>

    <br><br>

    Version 2.0

    </div>

    """,
    unsafe_allow_html=True
)