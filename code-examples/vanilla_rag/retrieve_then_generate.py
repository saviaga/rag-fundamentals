"""
Minimal vanilla RAG pipeline.

Demonstrates the basic retrieve-then-generate pattern:
query -> retrieve documents -> construct prompt -> generate answer.
See: concepts/rag/vanilla-rag.md

Run: python retrieve_then_generate.py
Dependencies: numpy, openai (optional, for real generation)

Without OpenAI API key, the script demonstrates the pipeline
structure with simulated generation.
"""

import numpy as np
import os

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


# ============================================================
# Step 1: Document Store (simulated vector database)
# ============================================================

class SimpleVectorStore:
    """
    A minimal in-memory vector store.
    In production, you'd use Pinecone, Weaviate, Chroma, etc.
    """

    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add(self, text: str, embedding: np.ndarray):
        """Add a document with its embedding."""
        self.documents.append(text)
        self.embeddings.append(embedding)

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> list:
        """Find top-k most similar documents."""
        similarities = []
        for i, doc_emb in enumerate(self.embeddings):
            sim = np.dot(query_embedding, doc_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb)
            )
            similarities.append((self.documents[i], sim))

        # Sort by similarity (descending) and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]


# ============================================================
# Step 2: Embedding Function (simulated)
# ============================================================

def get_embedding(text: str) -> np.ndarray:
    """
    Get embedding for text.

    In production, you'd call an embedding API:
    - OpenAI: text-embedding-ada-002
    - Cohere: embed-english-v3.0
    - Local: sentence-transformers

    This simulation uses predefined embeddings for demonstration.
    """
    # Simulated embeddings for our knowledge base
    embedding_map = {
        # Company info documents
        "TechCorp was founded in 2015 by Alice Johnson and Bob Smith.":
            np.array([0.9, 0.8, 0.1, 0.1, 0.2]),
        "The company headquarters is located in Austin, Texas.":
            np.array([0.7, 0.6, 0.3, 0.2, 0.1]),
        "TechCorp specializes in cloud computing and AI solutions.":
            np.array([0.8, 0.7, 0.5, 0.6, 0.3]),
        "The current CEO is Alice Johnson, one of the original founders.":
            np.array([0.85, 0.75, 0.15, 0.1, 0.25]),
        "TechCorp has over 1,000 employees worldwide.":
            np.array([0.6, 0.5, 0.2, 0.15, 0.1]),
        "Annual revenue reached $500 million in 2023.":
            np.array([0.5, 0.4, 0.3, 0.2, 0.8]),
        "The company offers three main products: CloudBase, AIHub, and DataFlow.":
            np.array([0.7, 0.6, 0.7, 0.8, 0.4]),
    }

    # For queries, create embeddings based on content
    if text in embedding_map:
        return embedding_map[text]

    # Simple keyword-based embedding for queries (simulation only)
    emb = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
    text_lower = text.lower()

    if "founder" in text_lower or "founded" in text_lower or "started" in text_lower:
        emb = np.array([0.88, 0.78, 0.12, 0.1, 0.22])
    elif "ceo" in text_lower or "leader" in text_lower:
        emb = np.array([0.83, 0.73, 0.13, 0.1, 0.23])
    elif "location" in text_lower or "where" in text_lower or "headquarters" in text_lower:
        emb = np.array([0.68, 0.58, 0.32, 0.22, 0.12])
    elif "product" in text_lower or "offer" in text_lower or "sell" in text_lower:
        emb = np.array([0.68, 0.58, 0.68, 0.78, 0.38])
    elif "revenue" in text_lower or "money" in text_lower or "earn" in text_lower:
        emb = np.array([0.48, 0.38, 0.28, 0.18, 0.78])

    return emb


# ============================================================
# Step 3: Prompt Construction
# ============================================================

def build_prompt(query: str, retrieved_docs: list) -> str:
    """
    Construct the prompt for the LLM.

    This is where retrieval meets generation.
    The prompt template significantly affects output quality.
    """
    context = "\n\n".join([f"Document {i+1}: {doc}" for i, (doc, _) in enumerate(retrieved_docs)])

    prompt = f"""Answer the question based ONLY on the following context. If the answer is not in the context, say "I don't have enough information to answer this question."

Context:
{context}

Question: {query}

Answer:"""

    return prompt


# ============================================================
# Step 4: Generation
# ============================================================

def generate_answer(prompt: str, use_api: bool = False) -> str:
    """
    Generate an answer using an LLM.

    Set use_api=True and provide OPENAI_API_KEY to use real generation.
    """
    if use_api and OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=200,
        )
        return response.choices[0].message.content

    # Simulated generation for demonstration
    # In reality, this would be an LLM call
    return "[Simulated LLM response based on retrieved context]"


# ============================================================
# Main RAG Pipeline
# ============================================================

def rag_pipeline(query: str, vector_store: SimpleVectorStore, top_k: int = 3, verbose: bool = True) -> str:
    """
    The complete RAG pipeline:
    1. Embed the query
    2. Retrieve relevant documents
    3. Build prompt with context
    4. Generate answer
    """
    if verbose:
        print("\n" + "=" * 60)
        print("RAG PIPELINE EXECUTION")
        print("=" * 60)

    # Step 1: Embed query
    if verbose:
        print(f"\n[Step 1] EMBED QUERY")
        print(f"  Query: \"{query}\"")

    query_embedding = get_embedding(query)

    if verbose:
        print(f"  Embedding: {query_embedding[:3]}... (truncated)")

    # Step 2: Retrieve
    if verbose:
        print(f"\n[Step 2] RETRIEVE (top-{top_k})")

    retrieved = vector_store.search(query_embedding, top_k=top_k)

    if verbose:
        for i, (doc, score) in enumerate(retrieved, 1):
            print(f"  {i}. [{score:.3f}] {doc[:50]}...")

    # Step 3: Build prompt
    if verbose:
        print(f"\n[Step 3] BUILD PROMPT")

    prompt = build_prompt(query, retrieved)

    if verbose:
        print("  Prompt constructed with retrieved context")
        print("-" * 40)
        print(prompt[:300] + "..." if len(prompt) > 300 else prompt)
        print("-" * 40)

    # Step 4: Generate
    if verbose:
        print(f"\n[Step 4] GENERATE ANSWER")

    answer = generate_answer(prompt, use_api=False)

    if verbose:
        print(f"  Generated: {answer}")

    return answer


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 70)
    print("VANILLA RAG: RETRIEVE-THEN-GENERATE PIPELINE")
    print("=" * 70)
    print("""
This example demonstrates the core RAG pattern:

  Query → Embed → Retrieve → Build Prompt → Generate

Each step is shown explicitly so you can understand the flow.
""")

    # ================================================================
    # Initialize: Create and populate vector store
    # ================================================================
    print("=" * 70)
    print("INITIALIZATION: Populating Vector Store")
    print("=" * 70)

    store = SimpleVectorStore()

    documents = [
        "TechCorp was founded in 2015 by Alice Johnson and Bob Smith.",
        "The company headquarters is located in Austin, Texas.",
        "TechCorp specializes in cloud computing and AI solutions.",
        "The current CEO is Alice Johnson, one of the original founders.",
        "TechCorp has over 1,000 employees worldwide.",
        "Annual revenue reached $500 million in 2023.",
        "The company offers three main products: CloudBase, AIHub, and DataFlow.",
    ]

    print("\nIndexing documents:")
    for doc in documents:
        embedding = get_embedding(doc)
        store.add(doc, embedding)
        print(f"  ✓ {doc[:50]}...")

    print(f"\nVector store ready with {len(documents)} documents.")

    # ================================================================
    # Run RAG queries
    # ================================================================
    queries = [
        "Who founded TechCorp?",
        "Where is TechCorp located?",
        "What products does TechCorp offer?",
        "What is TechCorp's annual revenue?",
    ]

    for query in queries:
        rag_pipeline(query, store, top_k=3, verbose=True)

    # ================================================================
    # Key concepts summary
    # ================================================================
    print("\n" + "=" * 70)
    print("KEY CONCEPTS IN VANILLA RAG")
    print("=" * 70)
    print("""
1. INDEXING (offline)
   - Documents are chunked and embedded
   - Embeddings stored in vector database
   - Done once, before any queries

2. QUERY EMBEDDING (runtime)
   - User query converted to same embedding space
   - Must use same embedding model as indexing

3. RETRIEVAL (runtime)
   - Find k most similar documents via vector search
   - Similarity typically measured by cosine distance

4. PROMPT CONSTRUCTION (runtime)
   - Combine retrieved docs with query into prompt
   - Template design affects answer quality

5. GENERATION (runtime)
   - LLM generates answer based on prompt
   - Model only knows what's in the prompt!

CRITICAL INSIGHT:
The LLM's "knowledge" for this query IS the retrieved context.
If retrieval fails, the LLM either hallucinates or says "I don't know."
This is why retrieval quality is paramount in RAG systems.
""")

    # ================================================================
    # Try with real API (optional)
    # ================================================================
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        print("=" * 70)
        print("BONUS: Real LLM Generation")
        print("=" * 70)
        print("\nOpenAI API key detected. Running with real generation...")

        query = "Who is the CEO of TechCorp and when was the company founded?"
        query_embedding = get_embedding(query)
        retrieved = store.search(query_embedding, top_k=3)
        prompt = build_prompt(query, retrieved)
        answer = generate_answer(prompt, use_api=True)

        print(f"\nQuery: {query}")
        print(f"Answer: {answer}")
    else:
        print("\n" + "-" * 70)
        print("To see real LLM generation:")
        print("  1. pip install openai")
        print("  2. export OPENAI_API_KEY='your-key'")
        print("  3. Run this script again")
        print("-" * 70)


if __name__ == "__main__":
    main()
