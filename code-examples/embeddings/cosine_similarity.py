"""
Cosine similarity between embedding vectors.

Demonstrates how similarity is computed in embedding space.
See: concepts/language-models/embeddings.md

Run: python cosine_similarity.py
Dependencies: numpy
"""

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def main():
    print("=" * 60)
    print("COSINE SIMILARITY IN EMBEDDING SPACE")
    print("=" * 60)

    # --- Part 1: Understanding cosine similarity geometrically ---
    print("\n[1] GEOMETRIC INTUITION")
    print("-" * 40)
    print("Cosine similarity measures the angle between vectors,")
    print("ignoring their magnitude. Range: -1 to 1")
    print("  1.0 = identical direction (parallel)")
    print("  0.0 = perpendicular (orthogonal)")
    print(" -1.0 = opposite direction")

    # Identical vectors
    v1 = np.array([1.0, 0.0])
    v2 = np.array([1.0, 0.0])
    print(f"\nIdentical vectors: {v1} and {v2}")
    print(f"Cosine similarity: {cosine_similarity(v1, v2):.4f}")
    print("""
          y
          │
          │
          │
     ─────┼────→→ x   Both vectors point right (→→)
          │           Angle = 0°, cos(0°) = 1.0
          │

    What does 1.0 mean semantically?
    ---------------------------------
    Geometrically: vectors point in exactly the same direction.

    For embeddings: The texts have identical or near-identical meaning.
    Examples:
    - "car" and "car" (same word)
    - "automobile" and "car" (synonyms, typically 0.7-0.9)
    - A document and itself (exactly 1.0)

    In RAG: A score of 1.0 means perfect match. Scores above 0.8
    typically indicate highly relevant documents.
    """)

    # Perpendicular vectors
    v3 = np.array([1.0, 0.0])
    v4 = np.array([0.0, 1.0])
    print(f"Perpendicular vectors: {v3} and {v4}")
    print(f"Cosine similarity: {cosine_similarity(v3, v4):.4f}")
    print("""
          y
          │
          ↑  v2 points up
          │
     ─────┼────→ x    v1 points right
          │           Angle = 90°, cos(90°) = 0.0
          │

    What does 0.0 mean semantically?
    ---------------------------------
    Geometrically: vectors are perpendicular (orthogonal), no overlap.

    For embeddings: The texts are completely unrelated.
    Examples:
    - "pizza" and "quantum physics"
    - "bicycle" and "democracy"
    - Any two words from entirely different domains

    In RAG: Scores near 0 mean the document is irrelevant to the query.
    However, exact 0.0 is rare—most unrelated pairs score 0.1-0.3
    due to common words and statistical noise in embeddings.
    """)

    # Opposite vectors
    v5 = np.array([1.0, 0.0])
    v6 = np.array([-1.0, 0.0])
    print(f"Opposite vectors: {v5} and {v6}")
    print(f"Cosine similarity: {cosine_similarity(v5, v6):.4f}")
    print("""
          y
          │
          │
          │
     ←────┼────→ x    v1 right (→), v2 left (←)
          │           Angle = 180°, cos(180°) = -1.0
          │

    What does -1.0 mean semantically?
    ---------------------------------
    Geometrically: vectors point in exactly opposite directions.

    In theory, this would mean "maximally different" or "opposite meaning"
    (e.g., "hot" vs "cold", "good" vs "bad").

    In practice: Real embedding models rarely produce -1.0 because:
    1. Most embeddings have positive components (no true opposites)
    2. Unrelated words are usually ~0.0 (orthogonal), not -1.0
    3. Even antonyms like "hot"/"cold" are often SIMILAR (~0.5+)
       because they share context (both describe temperature)

    For RAG retrieval, you typically see scores from 0.3 to 1.0.
    Scores near 0 mean "unrelated", not "opposite".
    """)

    # --- Part 2: Magnitude invariance ---
    print("\n[2] MAGNITUDE INVARIANCE")
    print("-" * 40)
    print("Cosine similarity only cares about direction, not length.")

    v7 = np.array([1.0, 1.0])
    v8 = np.array([100.0, 100.0])  # Same direction, 100x longer
    print(f"\nShort vector: {v7}")
    print(f"Long vector:  {v8}")
    print(f"Cosine similarity: {cosine_similarity(v7, v8):.4f}")
    print("(Still 1.0 because they point in the same direction)")

    # --- Part 3: Simulated word embeddings ---
    print("\n[3] WORD EMBEDDING EXAMPLE")
    print("-" * 40)
    print("In real embeddings, semantically similar words have similar vectors.")
    print("Here we simulate 4-dimensional embeddings for illustration.")

    # Simulated embeddings (in reality these come from trained models)
    embeddings = {
        "cat":      np.array([0.9, 0.8, 0.1, 0.2]),
        "kitten":   np.array([0.85, 0.75, 0.15, 0.25]),
        "dog":      np.array([0.8, 0.7, 0.2, 0.3]),
        "car":      np.array([0.1, 0.2, 0.9, 0.8]),
        "truck":    np.array([0.15, 0.25, 0.85, 0.75]),
    }

    print("\nComparing 'cat' to other words:")
    cat_embedding = embeddings["cat"]
    for word, embedding in embeddings.items():
        if word != "cat":
            sim = cosine_similarity(cat_embedding, embedding)
            print(f"  cat <-> {word:8s}: {sim:.4f}")

    print("\nObservation: 'cat' is most similar to 'kitten', then 'dog',")
    print("and least similar to 'car' and 'truck' (different category).")

    # --- Part 4: Why this matters for retrieval ---
    print("\n[4] WHY THIS MATTERS FOR RAG")
    print("-" * 40)
    print("In RAG systems, we embed both the query and documents.")
    print("Documents with highest cosine similarity to the query are retrieved.")

    query = np.array([0.88, 0.78, 0.12, 0.22])  # Similar to "cat"
    documents = {
        "Doc A: Cats are popular pets":     np.array([0.9, 0.8, 0.1, 0.2]),
        "Doc B: Dogs need daily walks":     np.array([0.8, 0.7, 0.2, 0.3]),
        "Doc C: Cars require maintenance":  np.array([0.1, 0.2, 0.9, 0.8]),
    }

    print("\nQuery embedding (similar to 'cat'):", query)
    print("\nDocument similarities:")

    ranked = sorted(
        [(doc, cosine_similarity(query, emb)) for doc, emb in documents.items()],
        key=lambda x: x[1],
        reverse=True
    )

    for rank, (doc, sim) in enumerate(ranked, 1):
        print(f"  {rank}. {sim:.4f} - {doc}")

    print("\nThe cat-related document ranks highest, as expected.")
    print("=" * 60)


if __name__ == "__main__":
    main()
