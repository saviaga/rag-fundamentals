# Embeddings

## Definition

An embedding is a learned numerical representation that maps a discrete unit of text, such as a word, token, sentence, or passage, to a point in a continuous vector space. In this space, geometric relationships, such as distance or similarity, reflect relationships in meaning.

## Core idea

Text is discrete. Words are symbols, and sentences are sequences of symbols. Neural networks, however, operate on continuous numerical values. Embeddings provide the bridge between these two domains by converting text into vectors of real numbers that models can process.

The key property of embeddings is that they encode semantic similarity. Text units that are similar in meaning tend to be mapped to nearby points in the vector space, while unrelated text is mapped farther apart. This allows mathematical operations, such as computing distances or similarity scores, to act as proxies for semantic relationships.

Embeddings are learned by encoder models trained on large text corpora. During training, the model adjusts the vector representations so that texts that appear in similar contexts end up with similar embeddings. After training, the encoder can embed new text that was not seen during training, as long as it follows similar linguistic patterns.

## Why this concept matters for RAG

Embeddings are foundational to retrieval in RAG systems, especially dense retrieval.

When a query is issued, both the query and the documents in the collection are converted into embeddings. Retrieval then becomes a geometric problem: finding the document embeddings that are closest to the query embedding in the vector space.

This enables semantic retrieval. Unlike lexical methods, which rely on exact word overlap, embedding-based retrieval can surface relevant documents even when the query and the document use different words to express the same idea.

At the same time, embeddings limit what can be retrieved. If the embedding model fails to capture a particular distinction, such as a subtle domain-specific concept or a rare term, retrieval cannot recover it. Retrieval quality is therefore bounded by the quality and suitability of the embedding model.

## Interpreting cosine similarity scores

Cosine similarity measures the angle between two embedding vectors, producing a score from -1 to 1.

| Score | Geometric meaning | Semantic interpretation |
|-------|-------------------|------------------------|
| **1.0** | Identical direction | Identical or synonymous meaning. A document compared to itself scores 1.0. Synonyms like "car" and "automobile" typically score 0.7–0.9. |
| **0.0** | Perpendicular (orthogonal) | Completely unrelated texts. However, exact 0.0 is rare in practice—most unrelated pairs score 0.1–0.3 due to shared common words and statistical noise. |
| **-1.0** | Opposite direction | Theoretically "opposite meaning." In practice, real embedding models rarely produce negative scores because most embeddings have positive components. Even antonyms like "hot" and "cold" often score positively (~0.5+) because they share context (both describe temperature). |

**Practical guidance for RAG:**
- Scores above 0.8 typically indicate highly relevant documents
- Scores between 0.5–0.8 suggest moderate relevance
- Scores below 0.3 usually mean the document is not relevant
- Scores near 0 mean "unrelated," not "opposite"

These thresholds vary by embedding model and domain. Calibration against labeled data is recommended for production systems.

## Why dense retrieval finds what lexical search misses

Dense retrieval using embeddings can find relevant documents even when the query and document use completely different words. For example, a query for "automobile maintenance" can match a document about "car repair" because embeddings place these concepts nearby in vector space, despite zero lexical overlap.

This is the key advantage of dense retrieval over lexical methods like BM25, which require exact word matches. See `code-examples/embeddings/semantic_vs_lexical.py` for a demonstration.

## Key constraints

Embeddings are static representations. Once a document is embedded, its vector does not change unless the document is re-encoded. If the embedding model is updated, the entire collection must typically be re-embedded to remain consistent.

Embedding models compress meaning into a fixed-size vector. This compression necessarily discards information. Fine-grained details, rare concepts, or highly specialized terminology may be poorly represented.

Embeddings reflect their training data. The structure of the vector space is shaped by the corpus used during training. If certain concepts are underrepresented or biased in the data, those gaps and biases will appear in the embeddings.

## Canonical Papers

- **A Survey of Text Embeddings**
  ACM Computing Surveys, 2020
  https://dl.acm.org/doi/10.1145/3400029
  This survey provides a systematic overview of text embedding methods, clarifying how different training objectives and architectures affect what information embeddings capture and what they discard.
