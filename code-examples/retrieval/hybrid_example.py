"""
Hybrid retrieval combining lexical and dense methods.

Demonstrates how combining BM25 and dense retrieval can improve
recall over either method alone.
See: concepts/retrieval/hybrid-retrieval.md

Run: python hybrid_example.py
Dependencies: numpy
"""

import numpy as np
from collections import Counter
import math


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def tokenize(text: str) -> list:
    return text.lower().split()


def bm25_scores(query: str, documents: list, k1: float = 1.5, b: float = 0.75) -> dict:
    """Compute BM25 scores."""
    query_terms = tokenize(query)
    doc_tokens = [tokenize(doc) for doc in documents]
    doc_count = len(documents)
    avgdl = sum(len(d) for d in doc_tokens) / doc_count

    df = Counter()
    for tokens in doc_tokens:
        for term in set(tokens):
            df[term] += 1

    scores = {}
    for doc, tokens in zip(documents, doc_tokens):
        score = 0.0
        term_freqs = Counter(tokens)
        doc_len = len(tokens)
        for term in query_terms:
            if term in term_freqs:
                tf = term_freqs[term]
                idf = math.log((doc_count - df[term] + 0.5) / (df[term] + 0.5) + 1)
                score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avgdl))
        scores[doc] = score
    return scores


def dense_scores(query_emb: np.ndarray, doc_embeddings: dict) -> dict:
    """Compute dense retrieval scores."""
    return {doc: cosine_similarity(query_emb, emb) for doc, emb in doc_embeddings.items()}


def normalize_scores(scores: dict) -> dict:
    """Min-max normalize scores to [0, 1]."""
    values = list(scores.values())
    min_v, max_v = min(values), max(values)
    if max_v == min_v:
        return {k: 0.5 for k in scores}
    return {k: (v - min_v) / (max_v - min_v) for k, v in scores.items()}


def hybrid_scores(bm25: dict, dense: dict, alpha: float = 0.5) -> dict:
    """
    Combine BM25 and dense scores.
    alpha: weight for dense scores (1-alpha for BM25)
    """
    bm25_norm = normalize_scores(bm25)
    dense_norm = normalize_scores(dense)

    combined = {}
    for doc in bm25:
        combined[doc] = (1 - alpha) * bm25_norm[doc] + alpha * dense_norm[doc]
    return combined


def print_rankings(title: str, scores: dict, top_k: int = 5):
    print(f"\n{title}")
    print("-" * 60)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    for rank, (doc, score) in enumerate(ranked, 1):
        print(f"  {rank}. [{score:.4f}] {doc[:55]}...")


def main():
    print("=" * 70)
    print("HYBRID RETRIEVAL: COMBINING BM25 + DENSE")
    print("=" * 70)

    # ================================================================
    # Setup: Documents and embeddings
    # ================================================================

    documents = [
        "The Python programming language was created by Guido van Rossum",
        "Machine learning models require large datasets for training",
        "Guido designed Python to be readable and simple",
        "Deep learning is a subset of machine learning using neural networks",
        "Van Rossum worked at Google and later Dropbox",
        "Python syntax emphasizes code readability",
        "Neural networks are inspired by biological neurons",
        "The creator of Python prioritized developer experience",
    ]

    # Simulated embeddings (in practice, from a model like sentence-transformers)
    # These are designed to show semantic clustering
    doc_embeddings = {
        documents[0]: np.array([0.9, 0.8, 0.2, 0.1]),   # Python + Guido
        documents[1]: np.array([0.2, 0.1, 0.9, 0.8]),   # ML
        documents[2]: np.array([0.85, 0.9, 0.15, 0.1]), # Python + Guido
        documents[3]: np.array([0.25, 0.15, 0.85, 0.9]),# ML/DL
        documents[4]: np.array([0.7, 0.85, 0.1, 0.1]),  # Guido career
        documents[5]: np.array([0.8, 0.7, 0.2, 0.15]),  # Python
        documents[6]: np.array([0.2, 0.1, 0.8, 0.85]),  # Neural nets
        documents[7]: np.array([0.75, 0.8, 0.2, 0.1]),  # Python creator
    }

    # ================================================================
    # Scenario 1: Query benefits from hybrid
    # ================================================================
    print("\n" + "=" * 70)
    print("SCENARIO: Query about Python's creator")
    print("=" * 70)

    query = "Who invented Python programming language"
    query_emb = np.array([0.8, 0.85, 0.15, 0.1])  # Semantic: Python + person

    print(f"\nQuery: \"{query}\"")
    print("\nDocuments in corpus:")
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. {doc}")

    # Compute individual scores
    bm25 = bm25_scores(query, documents)
    dense = dense_scores(query_emb, doc_embeddings)

    print_rankings("BM25 Only (lexical):", bm25, top_k=4)
    print("\n  → BM25 finds docs with 'Python' and 'programming'")
    print("    but misses semantically related docs about 'creator' or 'Guido'")

    print_rankings("Dense Only (semantic):", dense, top_k=4)
    print("\n  → Dense finds docs about Python's creator (semantic match)")
    print("    but might rank docs without key terms too high")

    # Hybrid with different alpha values
    print("\n" + "-" * 70)
    print("HYBRID RETRIEVAL (combining both)")
    print("-" * 70)

    for alpha in [0.3, 0.5, 0.7]:
        hybrid = hybrid_scores(bm25, dense, alpha=alpha)
        print(f"\nAlpha = {alpha} (BM25 weight: {1-alpha:.1f}, Dense weight: {alpha:.1f})")
        ranked = sorted(hybrid.items(), key=lambda x: x[1], reverse=True)[:3]
        for rank, (doc, score) in enumerate(ranked, 1):
            print(f"  {rank}. [{score:.4f}] {doc[:50]}...")

    # ================================================================
    # Reference
    # ================================================================
    print("\n" + "=" * 70)
    print("For why hybrid works and combination methods, see:")
    print("  concepts/retrieval/hybrid-retrieval.md")
    print("=" * 70)

    # ================================================================
    # Reciprocal Rank Fusion demo
    # ================================================================
    print("=" * 70)
    print("BONUS: RECIPROCAL RANK FUSION (RRF)")
    print("=" * 70)
    print("\nRRF combines rankings instead of scores, avoiding normalization issues.")
    print("Formula: RRF(d) = Σ 1/(k + rank(d)) for each retrieval method")

    k = 60  # Standard RRF constant

    # Get rankings from each method
    bm25_ranked = sorted(bm25.items(), key=lambda x: x[1], reverse=True)
    dense_ranked = sorted(dense.items(), key=lambda x: x[1], reverse=True)

    bm25_ranks = {doc: rank for rank, (doc, _) in enumerate(bm25_ranked, 1)}
    dense_ranks = {doc: rank for rank, (doc, _) in enumerate(dense_ranked, 1)}

    rrf_scores = {}
    for doc in documents:
        rrf_scores[doc] = 1/(k + bm25_ranks[doc]) + 1/(k + dense_ranks[doc])

    print_rankings("RRF Combined Rankings:", rrf_scores, top_k=4)

    print("\n  → RRF is often more stable than score interpolation")
    print("    because it only uses rank positions, not raw scores.")


if __name__ == "__main__":
    main()
