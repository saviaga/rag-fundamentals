# Embeddings

## Definition

An embedding is a learned representation that maps a discrete unit of text, such as a word, token, or passage, to a point in a continuous vector space where geometric relationships encode semantic similarity.

## Core idea

Text is inherently discrete. Words are symbols, and sentences are sequences of symbols. Neural networks, however, operate on continuous numerical values. Embeddings provide the bridge between these two domains by assigning each discrete unit a vector of real numbers.

The key property of embeddings is that they are learned to capture meaning. Words or passages with similar meanings are mapped to nearby points in the vector space, while unrelated items are mapped to distant points. This allows mathematical operations, such as measuring distance or computing similarity, to serve as proxies for semantic relationships.

Embeddings are produced by encoding models that have been trained on large amounts of text. The training process adjusts the mapping so that the resulting vectors reflect patterns of usage and co-occurrence observed in the data. After training, the encoder can be used to embed new text that was not seen during training, as long as it resembles the training distribution.

## Why this concept matters for RAG

Embeddings are foundational to retrieval in RAG systems, particularly dense retrieval. When a query is issued, both the query and the documents in the collection are represented as embeddings. Retrieval then reduces to finding documents whose embeddings are close to the query embedding in the vector space.

This approach enables semantic matching. Unlike lexical retrieval, which depends on exact word overlap, embedding-based retrieval can identify relevant documents even when the query and document use different vocabulary to express the same idea.

Embeddings also determine what information can be retrieved. If the embedding model fails to capture a relevant semantic distinction, that distinction will not be reflected in the vector space, and retrieval will not be able to exploit it. The quality of retrieval is therefore bounded by the quality of the embeddings.

## Key constraints

Embeddings are fixed representations. Once a document is embedded, its vector does not change unless the document is re-encoded. If the embedding model is updated, the entire collection must be re-embedded to maintain consistency.

Embedding models have limited capacity. They compress the meaning of text into a fixed-size vector, which necessarily discards some information. Fine-grained distinctions, rare concepts, or domain-specific terminology may not be well represented.

Embeddings reflect training data biases. The relationships encoded in the vector space are derived from the training corpus. If that corpus contains biases or gaps, the embeddings will inherit them.

## Relationship to other concepts

Embeddings are distinct from generation. While language models use embeddings internally to represent tokens, the embeddings used for retrieval are typically produced by separate encoder models optimized for similarity rather than next-token prediction. In a RAG system, embeddings enable the retrieval component to select relevant documents, which are then passed to the language model for generation. Understanding this division clarifies why embedding quality directly affects retrieval quality, and why retrieval failures can occur even when the language model is highly capable.
