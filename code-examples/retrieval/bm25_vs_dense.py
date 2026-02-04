"""
BM25 vs dense retrieval comparison.

Shows how the same query returns different documents depending on
retrieval method. Illustrates when lexical vs semantic retrieval succeeds.
See: concepts/retrieval/lexical-retrieval.md, concepts/retrieval/dense-retrieval.md

Run: python bm25_vs_dense.py
Dependencies: numpy, rank_bm25, sentence-transformers (optional)

Falls back to simulated embeddings if sentence-transformers is not installed.
"""

import numpy as np
from collections import Counter
import math

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


# ============================================================
# BM25 Implementation (simplified)
# ============================================================

def tokenize(text: str) -> list:
    """Simple whitespace tokenization with lowercasing."""
    return text.lower().split()


def compute_bm25_scores(query: str, documents: list, k1: float = 1.5, b: float = 0.75) -> list:
    """
    Compute BM25 scores for a query against documents.
    BM25 is a lexical ranking function based on term frequency.
    """
    query_terms = tokenize(query)
    doc_tokens = [tokenize(doc) for doc in documents]

    # Document frequencies
    doc_count = len(documents)
    avgdl = sum(len(d) for d in doc_tokens) / doc_count

    # IDF scores
    df = Counter()
    for tokens in doc_tokens:
        for term in set(tokens):
            df[term] += 1

    scores = []
    for tokens in doc_tokens:
        score = 0.0
        doc_len = len(tokens)
        term_freqs = Counter(tokens)

        for term in query_terms:
            if term in term_freqs:
                tf = term_freqs[term]
                idf = math.log((doc_count - df[term] + 0.5) / (df[term] + 0.5) + 1)
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * (doc_len / avgdl))
                score += idf * (numerator / denominator)

        scores.append(score)

    return scores


# ============================================================
# Dense Retrieval
# ============================================================

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def compute_dense_scores_real(query: str, documents: list) -> list:
    """Use sentence-transformers for real embeddings."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_emb = model.encode(query)
    doc_embs = model.encode(documents)
    return [cosine_similarity(query_emb, doc_emb) for doc_emb in doc_embs]


def compute_dense_scores_simulated(query: str, documents: list) -> list:
    """Use pre-computed embeddings for demonstration."""
    # Simulated embeddings that capture semantic similarity
    # In reality, these would come from a trained model
    embeddings = {
        # Query about car problems
        "my automobile is making strange noises": np.array([0.9, 0.8, 0.7, 0.1]),
        # Documents
        "the car engine produces unusual sounds when starting": np.array([0.85, 0.82, 0.75, 0.12]),
        "vehicle maintenance tips for beginners": np.array([0.7, 0.6, 0.5, 0.2]),
        "how to fix car noises and rattles": np.array([0.88, 0.79, 0.72, 0.15]),
        "automobile is derived from greek and latin": np.array([0.3, 0.2, 0.1, 0.9]),
        "the history of the word car in english": np.array([0.25, 0.15, 0.1, 0.85]),
    }

    query_emb = embeddings.get(query, np.array([0.9, 0.8, 0.7, 0.1]))
    scores = []
    for doc in documents:
        doc_emb = embeddings.get(doc, np.random.rand(4))
        scores.append(cosine_similarity(query_emb, doc_emb))
    return scores


# ============================================================
# Main demonstration
# ============================================================

def print_rankings(title: str, query: str, documents: list, scores: list):
    """Print ranked results."""
    print(f"\n{title}")
    print("-" * 50)
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    for rank, (doc, score) in enumerate(ranked, 1):
        print(f"  {rank}. [{score:.4f}] {doc[:60]}...")


def main():
    print("=" * 70)
    print("BM25 (LEXICAL) VS DENSE (SEMANTIC) RETRIEVAL")
    print("=" * 70)

    # --- Scenario 1: Dense retrieval wins ---
    print("\n" + "=" * 70)
    print("SCENARIO 1: Synonym usage (dense retrieval wins)")
    print("=" * 70)

    query1 = "my automobile is making strange noises"

    docs1 = [
        "the car engine produces unusual sounds when starting",
        "vehicle maintenance tips for beginners",
        "how to fix car noises and rattles",
        "automobile is derived from greek and latin",
        "the history of the word car in english",
    ]

    print(f"\nQuery: \"{query1}\"")
    print("\nDocuments:")
    for i, doc in enumerate(docs1, 1):
        print(f"  {i}. {doc}")

    bm25_scores = compute_bm25_scores(query1, docs1)
    print_rankings("BM25 Rankings (lexical match):", query1, docs1, bm25_scores)

    print("\n  → BM25 ranks 'automobile is derived from greek' high because")
    print("    it contains the exact word 'automobile' from the query.")
    print("    But this document is NOT relevant to car problems!")

    if TRANSFORMERS_AVAILABLE:
        dense_scores = compute_dense_scores_real(query1, docs1)
    else:
        dense_scores = compute_dense_scores_simulated(query1, docs1)
        print("\n  (Using simulated embeddings - install sentence-transformers for real ones)")

    print_rankings("Dense Rankings (semantic match):", query1, docs1, dense_scores)

    print("\n  → Dense retrieval ranks 'car engine produces unusual sounds' higher")
    print("    because it understands automobile≈car and noises≈sounds semantically.")

    # --- Scenario 2: BM25 wins ---
    print("\n" + "=" * 70)
    print("SCENARIO 2: Specific technical terms (BM25 often wins)")
    print("=" * 70)

    query2 = "python asyncio event loop"

    docs2 = [
        "the asyncio event loop runs coroutines in python",
        "python async programming with concurrent futures",
        "javascript promises and event-driven programming",
        "how to handle asynchronous operations efficiently",
        "event loop implementation details in asyncio module",
    ]

    print(f"\nQuery: \"{query2}\"")
    print("\nDocuments:")
    for i, doc in enumerate(docs2, 1):
        print(f"  {i}. {doc}")

    bm25_scores2 = compute_bm25_scores(query2, docs2)
    print_rankings("BM25 Rankings:", query2, docs2, bm25_scores2)

    print("\n  → BM25 correctly prioritizes documents with exact terms")
    print("    'python', 'asyncio', 'event loop' - important for technical queries.")

    # --- Reference ---
    print("\n" + "=" * 70)
    print("For guidance on when to use each method, see:")
    print("  concepts/retrieval/dense-retrieval.md")
    print("  concepts/retrieval/lexical-retrieval.md")
    print("  concepts/retrieval/hybrid-retrieval.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
