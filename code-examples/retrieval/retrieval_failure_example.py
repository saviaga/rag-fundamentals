"""
Retrieval failure modes.

Demonstrates cases where retrieval fails to return relevant documents,
showing that RAG failures are often retrieval failures.
See: concepts/rag/common-rag-failures.md

Run: python retrieval_failure_example.py
Dependencies: numpy
"""

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_top_k(query_emb: np.ndarray, doc_embs: dict, k: int = 3) -> list:
    """Retrieve top-k documents by cosine similarity."""
    scores = [(doc, cosine_similarity(query_emb, emb)) for doc, emb in doc_embs.items()]
    return sorted(scores, key=lambda x: x[1], reverse=True)[:k]


def main():
    print("=" * 70)
    print("RETRIEVAL FAILURE MODES IN RAG")
    print("=" * 70)
    print("\nRAG systems can only generate good answers if retrieval finds")
    print("relevant documents. Here are common ways retrieval fails.\n")

    # ================================================================
    # Failure Mode 1: Relevant document not in corpus
    # ================================================================
    print("=" * 70)
    print("FAILURE 1: RELEVANT DOCUMENT NOT IN CORPUS")
    print("=" * 70)

    corpus_1 = {
        "Python was created by Guido van Rossum":           np.array([0.9, 0.1, 0.1]),
        "JavaScript runs in web browsers":                   np.array([0.1, 0.9, 0.1]),
        "SQL is used for database queries":                  np.array([0.1, 0.1, 0.9]),
    }

    query_1 = "What is the capital of France?"
    query_1_emb = np.array([0.2, 0.2, 0.2])  # Not similar to any document

    print(f"\nQuery: \"{query_1}\"")
    print("\nCorpus contains only programming-related documents:")
    for doc in corpus_1:
        print(f"  - {doc}")

    results = retrieve_top_k(query_1_emb, corpus_1, k=3)
    print(f"\nTop retrieved documents:")
    for doc, score in results:
        print(f"  [{score:.3f}] {doc}")

    print("\n→ PROBLEM: The answer (Paris) is not in the corpus at all.")
    print("  No matter how good the retrieval, it cannot find what doesn't exist.")
    print("  The LLM will either hallucinate or say it doesn't know.")

    # ================================================================
    # Failure Mode 2: Vocabulary mismatch
    # ================================================================
    print("\n" + "=" * 70)
    print("FAILURE 2: VOCABULARY MISMATCH")
    print("=" * 70)

    corpus_2 = {
        "The CEO announced quarterly earnings exceeded expectations":
            np.array([0.8, 0.7, 0.1, 0.1]),
        "Annual revenue grew by 15% year over year":
            np.array([0.75, 0.65, 0.15, 0.1]),
        "The company's profit margins improved significantly":
            np.array([0.7, 0.6, 0.2, 0.1]),
        "Stock prices rose following the financial report":
            np.array([0.6, 0.5, 0.3, 0.2]),
    }

    # User uses casual language, documents use formal business language
    query_2 = "how much money did they make"
    query_2_emb = np.array([0.3, 0.2, 0.8, 0.7])  # Different "space" than formal docs

    print(f"\nQuery: \"{query_2}\" (casual language)")
    print("\nCorpus uses formal business language:")
    for doc in corpus_2:
        print(f"  - {doc}")

    results = retrieve_top_k(query_2_emb, corpus_2, k=2)
    print(f"\nTop retrieved documents:")
    for doc, score in results:
        print(f"  [{score:.3f}] {doc}")

    print("\n→ PROBLEM: 'money they make' ≠ 'quarterly earnings' in embedding space")
    print("  The semantic gap between casual and formal language causes poor retrieval.")

    # ================================================================
    # Failure Mode 3: Ambiguous query
    # ================================================================
    print("\n" + "=" * 70)
    print("FAILURE 3: AMBIGUOUS QUERY")
    print("=" * 70)

    corpus_3 = {
        "Python snake habitat in tropical rainforests":
            np.array([0.9, 0.1, 0.1, 0.1]),
        "Python programming language tutorial for beginners":
            np.array([0.1, 0.9, 0.1, 0.1]),
        "Monty Python comedy sketches from the 1970s":
            np.array([0.1, 0.1, 0.9, 0.1]),
        "Ball python care guide for pet owners":
            np.array([0.85, 0.15, 0.1, 0.1]),
    }

    query_3 = "python"
    query_3_emb = np.array([0.4, 0.4, 0.3, 0.1])  # Ambiguous - all meanings mixed

    print(f"\nQuery: \"{query_3}\" (ambiguous)")
    print("\nCorpus contains documents about different meanings of 'python':")
    for doc in corpus_3:
        print(f"  - {doc}")

    results = retrieve_top_k(query_3_emb, corpus_3, k=3)
    print(f"\nTop retrieved documents:")
    for doc, score in results:
        print(f"  [{score:.3f}] {doc}")

    print("\n→ PROBLEM: Without context, retrieval returns a mix of meanings.")
    print("  User wanted programming help but got snake care guides.")

    # ================================================================
    # Failure Mode 4: Needle in haystack
    # ================================================================
    print("\n" + "=" * 70)
    print("FAILURE 4: NEEDLE IN HAYSTACK (relevant doc ranks low)")
    print("=" * 70)

    # Many similar documents, one has the specific answer
    corpus_4 = {
        "Company overview and mission statement":
            np.array([0.8, 0.7, 0.6, 0.1]),
        "Our team of experienced professionals":
            np.array([0.75, 0.72, 0.58, 0.12]),
        "Product catalog and pricing information":
            np.array([0.78, 0.68, 0.62, 0.15]),
        "Contact us for more information":
            np.array([0.72, 0.65, 0.55, 0.1]),
        "Refund policy: Full refunds within 30 days of purchase":  # THE ANSWER
            np.array([0.5, 0.4, 0.3, 0.9]),
        "Shipping and delivery options":
            np.array([0.7, 0.6, 0.5, 0.2]),
    }

    query_4 = "what is your return policy"
    query_4_emb = np.array([0.6, 0.5, 0.4, 0.7])

    print(f"\nQuery: \"{query_4}\"")
    print("\nCorpus (typical company FAQ):")
    for doc in corpus_4:
        print(f"  - {doc[:50]}...")

    results = retrieve_top_k(query_4_emb, corpus_4, k=3)
    print(f"\nTop 3 retrieved documents:")
    for doc, score in results:
        print(f"  [{score:.3f}] {doc[:50]}...")

    # Check if the refund policy is in top-3
    refund_in_top3 = any("Refund" in doc for doc, _ in results)
    if not refund_in_top3:
        print("\n→ PROBLEM: The refund policy document ranked #4 or lower!")
        print("  If we only retrieve top-3, the LLM never sees the answer.")

    # ================================================================
    # Reference
    # ================================================================
    print("\n" + "=" * 70)
    print("For failure modes and mitigations, see:")
    print("  concepts/rag/common-rag-failures.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
