"""
Semantic relationships in embedding space.

Demonstrates word analogies (king - man + woman ≈ queen) to show
how embeddings capture semantic meaning beyond lexical overlap.
See: concepts/language-models/embeddings.md

Run: python semantic_vs_lexical.py
Dependencies: numpy, gensim (for pre-trained word vectors)

If gensim is not installed, the script will use simulated embeddings.
"""

import numpy as np

try:
    import gensim.downloader as api
    GENSIM_AVAILABLE = True
except ImportError:
    GENSIM_AVAILABLE = False


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_nearest(target: np.ndarray, embeddings: dict, exclude: list) -> list:
    """Find words nearest to target vector."""
    similarities = []
    for word, vec in embeddings.items():
        if word not in exclude:
            sim = cosine_similarity(target, vec)
            similarities.append((word, sim))
    return sorted(similarities, key=lambda x: x[1], reverse=True)[:5]


def demo_with_real_embeddings():
    """Use GloVe word vectors for real analogy demonstration."""
    print("Loading GloVe word vectors (this may take a moment)...")
    model = api.load("glove-wiki-gigaword-50")

    print("\n[1] WORD ANALOGIES: king - man + woman = ?")
    print("-" * 50)
    print("The famous analogy test: if we take the vector for 'king',")
    print("subtract 'man', and add 'woman', we should get close to 'queen'.")

    king = model["king"]
    man = model["man"]
    woman = model["woman"]

    # king - man + woman should ≈ queen
    result_vector = king - man + woman

    print(f"\nOperation: king - man + woman")
    print(f"Expected result: queen")

    # Find nearest words to the result vector
    print(f"\nNearest words to the result vector:")
    similar = model.most_similar(positive=["king", "woman"], negative=["man"], topn=5)
    for word, sim in similar:
        marker = " <-- ✓" if word == "queen" else ""
        print(f"  {word}: {sim:.4f}{marker}")

    print("\n[2] MORE ANALOGIES")
    print("-" * 50)

    analogies = [
        (["paris", "germany"], ["france"], "berlin"),
        (["slow", "fastest"], ["fast"], "slowest"),
        (["man", "queen"], ["woman"], "king"),
    ]

    for positive, negative, expected in analogies:
        result = model.most_similar(positive=positive, negative=negative, topn=3)
        pos_str = " + ".join(positive)
        neg_str = " - ".join(negative)
        print(f"\n{pos_str} - {neg_str} = ?  (expected: {expected})")
        for word, sim in result:
            marker = " <--" if word == expected else ""
            print(f"  {word}: {sim:.4f}{marker}")

    print("\n[3] LEXICAL VS SEMANTIC SIMILARITY")
    print("-" * 50)
    print("Lexical similarity = shared characters/words")
    print("Semantic similarity = shared meaning")

    pairs = [
        ("car", "automobile"),  # Same meaning, different words
        ("car", "cars"),        # Same root, lexically similar
        ("bank", "river"),      # Can be related (river bank)
        ("happy", "joyful"),    # Synonyms
        ("happy", "hippy"),     # Lexically similar, semantically different
    ]

    print("\nWord pairs and their semantic similarity:")
    for w1, w2 in pairs:
        sim = model.similarity(w1, w2)
        print(f"  {w1:12} <-> {w2:12}: {sim:.4f}")

    print("\nNote: 'car' and 'automobile' are semantically similar (0.7+)")
    print("despite having zero lexical overlap!")
    print("Meanwhile 'happy' and 'hippy' share letters but have low similarity.")


def demo_with_simulated_embeddings():
    """Demonstrate concepts with pre-computed simulated embeddings."""
    print("(gensim not installed - using simulated embeddings)")
    print("Install gensim for real word vectors: pip install gensim")

    # Simulated embeddings designed to show the concept
    # In reality, these would be learned from large text corpora
    embeddings = {
        # Royalty cluster (dimension 0-1 high)
        "king":     np.array([0.9, 0.9, 0.1, 0.2, 0.8, 0.1]),
        "queen":    np.array([0.9, 0.9, 0.1, 0.2, 0.2, 0.8]),
        "prince":   np.array([0.85, 0.85, 0.15, 0.25, 0.75, 0.15]),
        "princess": np.array([0.85, 0.85, 0.15, 0.25, 0.25, 0.75]),
        # Gender encoded in dimensions 4-5
        "man":      np.array([0.1, 0.1, 0.5, 0.5, 0.9, 0.1]),
        "woman":    np.array([0.1, 0.1, 0.5, 0.5, 0.1, 0.9]),
        "boy":      np.array([0.1, 0.1, 0.6, 0.4, 0.85, 0.15]),
        "girl":     np.array([0.1, 0.1, 0.6, 0.4, 0.15, 0.85]),
        # Vehicle cluster (dimension 2-3 high)
        "car":       np.array([0.1, 0.2, 0.9, 0.8, 0.5, 0.5]),
        "automobile": np.array([0.1, 0.2, 0.88, 0.82, 0.5, 0.5]),
        "truck":     np.array([0.15, 0.25, 0.85, 0.75, 0.5, 0.5]),
    }

    print("\n[1] WORD ANALOGIES: king - man + woman = ?")
    print("-" * 50)
    print("The famous analogy test: if we take the vector for 'king',")
    print("subtract 'man', and add 'woman', we should get close to 'queen'.")

    king = embeddings["king"]
    man = embeddings["man"]
    woman = embeddings["woman"]
    queen = embeddings["queen"]

    result = king - man + woman

    print(f"\nking vector:   {king}")
    print(f"man vector:    {man}")
    print(f"woman vector:  {woman}")
    print(f"\nking - man + woman = {result}")
    print(f"queen vector:        {queen}")
    print(f"\nSimilarity to 'queen': {cosine_similarity(result, queen):.4f}")

    print("\nFinding nearest word to result vector:")
    nearest = find_nearest(result, embeddings, exclude=["king", "man", "woman"])
    for word, sim in nearest:
        marker = " <-- closest!" if word == nearest[0][0] else ""
        print(f"  {word}: {sim:.4f}{marker}")

    print("\n[2] WHY THIS WORKS")
    print("-" * 50)
    print("Embeddings encode semantic relationships as directions in space.")
    print("The 'gender direction' (woman - man) can be added to other concepts:")

    gender_direction = woman - man
    print(f"\nGender direction (woman - man): {gender_direction}")
    print("Notice: dimensions 4-5 encode gender (-0.8, +0.8)")

    print("\n[3] LEXICAL VS SEMANTIC SIMILARITY")
    print("-" * 50)
    print("Lexical: based on shared characters ('car' vs 'cars')")
    print("Semantic: based on meaning ('car' vs 'automobile')")

    car = embeddings["car"]
    automobile = embeddings["automobile"]

    sim = cosine_similarity(car, automobile)
    print(f"\n'car' and 'automobile' share NO letters")
    print(f"But semantic similarity: {sim:.4f}")
    print("\nThis is why dense retrieval finds documents that lexical search misses!")


def main():
    print("=" * 60)
    print("SEMANTIC VS LEXICAL: WHAT EMBEDDINGS CAPTURE")
    print("=" * 60)

    print("\nKey insight: Embeddings capture MEANING, not spelling.")
    print("This enables finding semantically related content even when")
    print("the exact words don't match.\n")

    if GENSIM_AVAILABLE:
        demo_with_real_embeddings()
    else:
        demo_with_simulated_embeddings()

    print("\n" + "=" * 60)
    print("TAKEAWAY FOR RAG")
    print("=" * 60)
    print("""
Dense retrieval using embeddings can find relevant documents even
when the query and document use completely different words.

Example: Query "automobile maintenance" can match a document about
"car repair" because embeddings place these concepts nearby in
vector space, despite zero lexical overlap.

This is the key advantage of dense retrieval over lexical methods
like BM25, which require exact word matches.
""")


if __name__ == "__main__":
    main()
