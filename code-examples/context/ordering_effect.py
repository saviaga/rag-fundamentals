"""
Document ordering effect in context.

Demonstrates the lost-in-the-middle phenomenon where information
placement in context affects model attention and answer quality.
See: concepts/inference/context-windows.md

Run: python ordering_effect.py
Dependencies: none (pure Python, simulates the effect)

Note: This demonstrates the concept. To see real effects, you would
need to run actual LLM inference with different orderings.
"""

import random


def simulate_attention_weight(position: int, total_positions: int) -> float:
    """
    Simulate the U-shaped attention pattern observed in LLMs.

    Research (Liu et al., 2023 "Lost in the Middle") shows that LLMs
    pay more attention to information at the beginning and end of
    the context, with reduced attention in the middle.

    This is a simplified simulation of that effect.
    """
    # Normalize position to [0, 1]
    normalized_pos = position / (total_positions - 1) if total_positions > 1 else 0.5

    # U-shaped curve: high at edges (0 and 1), low in middle (0.5)
    # Using a simple quadratic: attention = 4*(x - 0.5)^2 + base
    distance_from_middle = abs(normalized_pos - 0.5)
    attention = 0.4 + 0.6 * (2 * distance_from_middle) ** 1.5

    return attention


def visualize_attention(num_docs: int):
    """Visualize the attention distribution across positions."""
    print("\nSimulated attention by position (U-shaped curve):")
    print("-" * 60)

    for i in range(num_docs):
        weight = simulate_attention_weight(i, num_docs)
        bar_length = int(weight * 40)
        position_label = ""
        if i == 0:
            position_label = " ← START (high attention)"
        elif i == num_docs - 1:
            position_label = " ← END (high attention)"
        elif i == num_docs // 2:
            position_label = " ← MIDDLE (low attention)"

        print(f"  Doc {i+1:2d}: {'█' * bar_length}{'░' * (40-bar_length)} {weight:.2f}{position_label}")


def main():
    print("=" * 70)
    print("LOST IN THE MIDDLE: DOCUMENT ORDERING EFFECTS")
    print("=" * 70)
    print("""
Research shows that LLMs don't attend equally to all parts of their
context. Information in the MIDDLE of long contexts receives less
attention than information at the BEGINNING or END.

This is the "Lost in the Middle" phenomenon (Liu et al., 2023).
""")

    # ================================================================
    # Setup: Documents with one containing the answer
    # ================================================================

    documents = [
        "The company was founded in 2010 by three college friends.",
        "Our headquarters is located in San Francisco, California.",
        "We have over 500 employees across 12 global offices.",
        "THE ANSWER: The CEO's name is Sarah Chen.",  # <-- The answer!
        "The company went public in 2018 on the NASDAQ.",
        "Annual revenue exceeded $100 million in 2023.",
        "We partner with over 200 enterprise clients worldwide.",
    ]

    answer_doc_index = 3  # 0-indexed, this is position 4 (middle)
    query = "What is the CEO's name?"

    # ================================================================
    # Visualize attention distribution
    # ================================================================
    print("=" * 70)
    print("ATTENTION DISTRIBUTION VISUALIZATION")
    print("=" * 70)

    visualize_attention(len(documents))

    # ================================================================
    # Scenario 1: Answer in the middle
    # ================================================================
    print("\n" + "=" * 70)
    print("SCENARIO 1: Answer document in the MIDDLE")
    print("=" * 70)

    print(f"\nQuery: \"{query}\"")
    print("\nDocument ordering:")

    for i, doc in enumerate(documents):
        attention = simulate_attention_weight(i, len(documents))
        is_answer = "★ ANSWER" if i == answer_doc_index else ""
        attention_level = "HIGH" if attention > 0.7 else "LOW" if attention < 0.5 else "MED"
        print(f"  {i+1}. [{attention_level}] {doc[:50]}... {is_answer}")

    middle_attention = simulate_attention_weight(answer_doc_index, len(documents))
    print(f"\n⚠ Problem: The answer is at position {answer_doc_index + 1} (middle)")
    print(f"  Simulated attention weight: {middle_attention:.2f} (relatively low)")
    print("  The model may miss or underweight this information!")

    # ================================================================
    # Scenario 2: Answer at the beginning
    # ================================================================
    print("\n" + "=" * 70)
    print("SCENARIO 2: Answer document at the BEGINNING")
    print("=" * 70)

    # Reorder: put answer first
    reordered_begin = [documents[answer_doc_index]] + \
                      [d for i, d in enumerate(documents) if i != answer_doc_index]

    print(f"\nQuery: \"{query}\"")
    print("\nDocument ordering (answer moved to position 1):")

    for i, doc in enumerate(reordered_begin):
        attention = simulate_attention_weight(i, len(reordered_begin))
        is_answer = "★ ANSWER" if "CEO's name" in doc else ""
        attention_level = "HIGH" if attention > 0.7 else "LOW" if attention < 0.5 else "MED"
        print(f"  {i+1}. [{attention_level}] {doc[:50]}... {is_answer}")

    print(f"\n✓ Better: The answer is now at position 1")
    print(f"  Simulated attention weight: {simulate_attention_weight(0, len(documents)):.2f} (high)")

    # ================================================================
    # Scenario 3: Answer at the end
    # ================================================================
    print("\n" + "=" * 70)
    print("SCENARIO 3: Answer document at the END")
    print("=" * 70)

    # Reorder: put answer last
    reordered_end = [d for i, d in enumerate(documents) if i != answer_doc_index] + \
                    [documents[answer_doc_index]]

    print(f"\nQuery: \"{query}\"")
    print("\nDocument ordering (answer moved to last position):")

    for i, doc in enumerate(reordered_end):
        attention = simulate_attention_weight(i, len(reordered_end))
        is_answer = "★ ANSWER" if "CEO's name" in doc else ""
        attention_level = "HIGH" if attention > 0.7 else "LOW" if attention < 0.5 else "MED"
        print(f"  {i+1}. [{attention_level}] {doc[:50]}... {is_answer}")

    print(f"\n✓ Also good: The answer is now at position {len(reordered_end)}")
    print(f"  Simulated attention weight: {simulate_attention_weight(len(documents)-1, len(documents)):.2f} (high)")

    # ================================================================
    # Implications for RAG
    # ================================================================
    print("\n" + "=" * 70)
    print("IMPLICATIONS FOR RAG SYSTEMS")
    print("=" * 70)
    print("""
The lost-in-the-middle effect has practical implications:

1. DOCUMENT ORDERING MATTERS
   - Don't just concatenate retrieved docs in retrieval-score order
   - Consider placing most relevant docs at START or END

2. ORDERING STRATEGIES
   - "Relevance-first": Most relevant at the beginning
   - "Relevance-last": Most relevant at the end (recency bias)
   - "Edges-priority": Alternate placing relevant docs at start/end

3. CHUNKING IMPLICATIONS
   - Shorter contexts reduce the middle problem
   - With 3-4 chunks, the "middle" barely exists

4. CONTEXT LENGTH TRADE-OFF
   - Longer contexts = more information but worse middle attention
   - Sometimes less is more (fewer, better-placed docs)

5. PROMPT ENGINEERING
   - Explicit instructions can help: "Pay attention to all documents"
   - But this only partially mitigates the effect

Reference: Liu et al. (2023) "Lost in the Middle: How Language Models
Use Long Contexts" - https://arxiv.org/abs/2307.03172
""")

    # ================================================================
    # Best practice demonstration
    # ================================================================
    print("=" * 70)
    print("RECOMMENDED: INTERLEAVED ORDERING")
    print("=" * 70)

    print("""
One strategy: interleave by relevance, placing top docs at edges.

If docs are ranked [1, 2, 3, 4, 5] by relevance:
  → Reorder to [1, 3, 5, 4, 2] or [1, 5, 3, 4, 2]
  → Puts #1 at start, #2 at end, less important in middle
""")

    # Simulate interleaved ordering
    ranked_docs = list(enumerate(documents, 1))  # (rank, doc) pairs
    # Simplified interleave: odds at start, evens at end (reversed)
    interleaved = []
    for i in range(0, len(ranked_docs), 2):
        interleaved.append(ranked_docs[i])
    for i in range(len(ranked_docs) - 1 if len(ranked_docs) % 2 == 0 else len(ranked_docs) - 2, 0, -2):
        interleaved.append(ranked_docs[i])

    print("Example interleaved ordering:")
    for i, (orig_rank, doc) in enumerate(interleaved):
        attention = simulate_attention_weight(i, len(interleaved))
        print(f"  Position {i+1} [attn:{attention:.2f}]: Doc originally ranked #{orig_rank}")


if __name__ == "__main__":
    main()
