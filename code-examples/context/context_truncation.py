"""
Context window truncation.

Demonstrates what happens when retrieved content exceeds the
context window and must be truncated.
See: concepts/inference/context-windows.md

Run: python context_truncation.py
Dependencies: none (pure Python)
"""


def count_tokens_approx(text: str) -> int:
    """
    Approximate token count (rough: ~4 chars per token for English).
    Real tokenizers (tiktoken, sentencepiece) are more accurate.
    """
    return len(text) // 4


def truncate_to_fit(documents: list, max_tokens: int, query: str, prompt_template: str) -> tuple:
    """
    Truncate documents to fit within context window.
    Returns (truncated_docs, included_count, excluded_count).
    """
    # Reserve tokens for query and prompt structure
    prompt_overhead = count_tokens_approx(prompt_template) + count_tokens_approx(query)
    available_tokens = max_tokens - prompt_overhead

    included = []
    total_tokens = 0

    for doc in documents:
        doc_tokens = count_tokens_approx(doc)
        if total_tokens + doc_tokens <= available_tokens:
            included.append(doc)
            total_tokens += doc_tokens
        else:
            break  # No more room

    excluded_count = len(documents) - len(included)
    return included, len(included), excluded_count


def main():
    print("=" * 70)
    print("CONTEXT WINDOW TRUNCATION")
    print("=" * 70)
    print("""
Context windows have a fixed size (e.g., 4K, 8K, 128K tokens).
When retrieved documents exceed this limit, something must be cut.
This example shows how truncation affects what the model can see.
""")

    # ================================================================
    # Setup: Retrieved documents (ordered by relevance)
    # ================================================================

    # Simulate retrieved documents about "company refund policy"
    retrieved_docs = [
        # Doc 1: Highly relevant but verbose (rank 1)
        """REFUND POLICY OVERVIEW: Our company offers a comprehensive refund
        program designed to ensure customer satisfaction. We understand that
        sometimes purchases don't work out, and we want to make the return
        process as smooth as possible for all our valued customers.""",

        # Doc 2: Contains the actual answer (rank 2)
        """REFUND TIMEFRAME: Customers may request a full refund within 30 days
        of purchase. After 30 days, partial refunds may be available at our
        discretion. Digital products have a 7-day refund window.""",

        # Doc 3: Related but less relevant (rank 3)
        """REFUND PROCESS: To initiate a refund, contact our support team via
        email at support@company.com or call 1-800-REFUNDS. Please have your
        order number ready. Processing typically takes 5-7 business days.""",

        # Doc 4: Contains important exception (rank 4)
        """REFUND EXCEPTIONS: The following items are non-refundable: clearance
        items, personalized products, opened software, and items marked as
        final sale. Gift cards can only be refunded to the original purchaser.""",

        # Doc 5: Additional context (rank 5)
        """REFUND METHODS: Refunds are issued to the original payment method.
        Credit card refunds appear within 5-10 business days. PayPal refunds
        are typically instant. Store credit is available as an alternative.""",
    ]

    query = "What is the refund policy timeframe?"

    prompt_template = """Answer the question based on the context below.

Context:
{context}

Question: {question}

Answer:"""

    # ================================================================
    # Scenario 1: Large context window (all docs fit)
    # ================================================================
    print("=" * 70)
    print("SCENARIO 1: Large context window (8K tokens)")
    print("=" * 70)

    max_tokens_large = 8000
    included, inc_count, exc_count = truncate_to_fit(
        retrieved_docs, max_tokens_large, query, prompt_template
    )

    print(f"\nContext window: {max_tokens_large} tokens")
    print(f"Documents retrieved: {len(retrieved_docs)}")
    print(f"Documents included: {inc_count}")
    print(f"Documents excluded: {exc_count}")

    print("\n✓ All documents fit! The model sees everything:")
    for i, doc in enumerate(included, 1):
        print(f"  {i}. {doc[:60]}...")

    # ================================================================
    # Scenario 2: Small context window (truncation required)
    # ================================================================
    print("\n" + "=" * 70)
    print("SCENARIO 2: Small context window (500 tokens)")
    print("=" * 70)

    max_tokens_small = 500
    included, inc_count, exc_count = truncate_to_fit(
        retrieved_docs, max_tokens_small, query, prompt_template
    )

    print(f"\nContext window: {max_tokens_small} tokens")
    print(f"Documents retrieved: {len(retrieved_docs)}")
    print(f"Documents included: {inc_count}")
    print(f"Documents excluded: {exc_count}")

    print("\n⚠ TRUNCATION OCCURRED!")
    print("\nDocuments the model CAN see:")
    for i, doc in enumerate(included, 1):
        print(f"  {i}. {doc[:60]}...")

    print("\nDocuments the model CANNOT see (truncated):")
    for i, doc in enumerate(retrieved_docs[inc_count:], inc_count + 1):
        print(f"  {i}. {doc[:60]}... [EXCLUDED]")

    # ================================================================
    # The problem
    # ================================================================
    print("\n" + "=" * 70)
    print("THE PROBLEM")
    print("=" * 70)
    print("""
In Scenario 2, the model only sees the first 1-2 documents.
The answer "30 days" is in Doc 2, which was EXCLUDED.
The model will hallucinate, say "I don't know", or give a vague answer.
""")

    # ================================================================
    # Interactive demonstration
    # ================================================================
    print("=" * 70)
    print("TOKEN BUDGET BREAKDOWN")
    print("=" * 70)

    total_doc_tokens = sum(count_tokens_approx(d) for d in retrieved_docs)
    overhead = count_tokens_approx(prompt_template) + count_tokens_approx(query)

    print(f"\nPrompt template + query: ~{overhead} tokens")
    print(f"All retrieved documents: ~{total_doc_tokens} tokens")
    print(f"Total needed: ~{overhead + total_doc_tokens} tokens")
    print(f"\nWith 500-token limit: {500 - overhead} tokens available for docs")
    print(f"With 8K-token limit:  {8000 - overhead} tokens available for docs")

    print("\n" + "=" * 70)
    print("For mitigation strategies, see:")
    print("  concepts/inference/context-windows.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
