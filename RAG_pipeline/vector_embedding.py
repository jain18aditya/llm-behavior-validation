"""
Week 4 – Production RAG Knowledge Agent

Features:
- Embeddings + Persistent Vector DB
- Sliding window chunking
- Hybrid retrieval (vector + keyword)
- Distance threshold filtering
- LLM reranking
- Grounded answering with source citation
- Precision@K evaluation
- Faithfulness check
- Latency + token tracking
- Structured logging
- Basic prompt injection defense

Architecture:
Query → Sanitize → Embed → Vector Search → Threshold Filter →
Hybrid Rank → Rerank → Context Injection → LLM →
Evaluation → Logging
"""

import time
import json
import chromadb
from chromadb.config import Settings
from utils.llm_client import get_client

# ------------------ CONFIG ------------------

EMBED_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
TOP_K_RETRIEVAL = 10
TOP_K_RERANK = 3
DISTANCE_THRESHOLD = 0.8
HYBRID_ALPHA = 0.7

# ------------------ INIT ------------------

client = get_client()

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("sample_rag")

# ------------------ SAMPLE DOCS ------------------

documents = [
    {"text": "Python is a programming language.", "source": "tech"},
    {"text": "Paris is the capital of France.", "source": "geography"},
    {"text": "Dogs are loyal animals.", "source": "animals"}
]

# ------------------ UTILITIES ------------------

def log_event(event_type, data):
    log_entry = {
        "event": event_type,
        "timestamp": time.time(),
        "data": data
    }
    print(json.dumps(log_entry, indent=2))


# ------------------ PROMPT INJECTION DEFENSE ------------------

def sanitize_query(query):
    blocked_phrases = [
        "ignore previous instructions",
        "disregard context",
        "override system"
    ]
    for phrase in blocked_phrases:
        if phrase in query.lower():
            raise ValueError("Potential prompt injection detected.")
    return query


# ------------------ EMBEDDING ------------------

def embed(text):
    response = client.embeddings.create(
        input=text,
        model=EMBED_MODEL
    )
    return response.data[0].embedding


# ------------------ CHUNKING ------------------

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+chunk_size]))
        i += chunk_size - overlap
    return chunks


# ------------------ STORE DOCUMENTS ------------------

def embed_documents(docs):
    if collection.count() > 0:
        return

    for i, doc in enumerate(docs):
        chunks = chunk_text(doc["text"])
        for j, chunk in enumerate(chunks):
            collection.add(
                ids=[f"{i}_{j}"],
                embeddings=[embed(chunk)],
                documents=[chunk],
                metadatas=[{"source": doc["source"]}]
            )


# ------------------ HYBRID SEARCH ------------------

def keyword_score(query, doc):
    q_words = set(query.lower().split())
    d_words = set(doc.lower().split())
    return len(q_words & d_words) / max(len(q_words), 1)


def hybrid_rank(query, docs, distances, metadatas):
    scored = []

    for doc, dist, meta in zip(docs, distances, metadatas):
        if dist > DISTANCE_THRESHOLD:
            continue

        vector_sim = 1 - dist
        kw_sim = keyword_score(query, doc)
        score = HYBRID_ALPHA * vector_sim + (1 - HYBRID_ALPHA) * kw_sim
        scored.append((score, doc, meta))

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored


# ------------------ RETRIEVAL ------------------

def retrieve(query):
    q_vec = embed(query)

    result = collection.query(
        query_embeddings=[q_vec],
        n_results=TOP_K_RETRIEVAL,
        include=["documents", "distances", "metadatas"]
    )

    docs = result["documents"][0]
    distances = result["distances"][0]
    metadatas = result["metadatas"][0]

    log_event("vector_retrieval", {
        "docs": docs,
        "distances": distances
    })

    ranked = hybrid_rank(query, docs, distances, metadatas)

    return ranked


# ------------------ RERANK ------------------

def rerank(query, ranked_docs):
    docs = [doc for _, doc, _ in ranked_docs]

    joined_docs = "\n\n".join(
        [f"Doc {i}: {doc}" for i, doc in enumerate(docs)]
    )

    prompt = f"""
Rank documents by relevance.

Query: {query}
Documents:
{joined_docs}

Return top {TOP_K_RERANK} document numbers separated by commas.
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    indices = [
        int(i.strip())
        for i in response.choices[0].message.content.split(",")
    ]

    return [ranked_docs[i] for i in indices[:TOP_K_RERANK]]


# ------------------ BUILD PROMPT ------------------

def build_prompt(query, docs_with_meta):
    context = "\n\n".join([doc for _, doc, _ in docs_with_meta])
    sources = list(set(meta["source"] for _, _, meta in docs_with_meta))

    messages = [
        {
            "role": "system",
            "content": "Answer strictly using provided context. Cite sources."
        },
        {
            "role": "user",
            "content": f"""
Context:
{context}

Question:
{query}

Provide answer and list sources used.
"""
        }
    ]

    return messages, sources


# ------------------ EVALUATION ------------------

def precision_at_k(retrieved_docs, expected_text):
    hits = sum(1 for doc in retrieved_docs if expected_text in doc)
    return hits / len(retrieved_docs)


def faithfulness_check(query, answer, context):
    prompt = f"""
Is the answer fully supported by the context?

Query: {query}
Context: {context}
Answer: {answer}

Return only: Faithful or Not Faithful.
"""
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content


# ------------------ MAIN PIPELINE ------------------

def answer_question(query):
    start_time = time.time()

    query = sanitize_query(query)

    ranked_docs = retrieve(query)
    top_docs = rerank(query, ranked_docs)

    messages, sources = build_prompt(query, top_docs)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages
    )

    answer = response.choices[0].message.content
    latency = time.time() - start_time
    token_usage = response.usage.total_tokens

    # Evaluation
    retrieved_texts = [doc for _, doc, _ in top_docs]
    precision = precision_at_k(retrieved_texts, "Python is a programming language.")
    faithfulness = faithfulness_check(query, answer, "\n".join(retrieved_texts))

    log_event("evaluation", {
        "precision_at_k": precision,
        "faithfulness": faithfulness,
        "latency_sec": latency,
        "tokens_used": token_usage,
        "sources": sources
    })

    print("\nAnswer:\n", answer)
    print("\nSources:", sources)

    return answer


# ------------------ RUN ------------------

if __name__ == "__main__":
    embed_documents(documents)
    answer_question("What is Python?")