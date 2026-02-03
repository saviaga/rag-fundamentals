# What Is a Language Model

## Definition

A language model is a system that assigns probabilities to sequences of text. Given a sequence of words, a language model estimates how likely that sequence is, or how likely a particular word is to come next.

## Core idea

Language models learn statistical patterns from large amounts of text. During training, they are exposed to vast corpora and adjust their internal parameters to capture regularities in how words and sentences are structured. After training, these parameters are fixed, and the model can be used to evaluate or generate text based on the patterns it has learned.

The key abstraction is that a language model encodes a compressed representation of language as observed in its training data. This representation allows the model to make predictions about text it has never seen before, as long as that text resembles the patterns encountered during training.

## Why this concept matters for RAG

Language models form the generation component in Retrieval-Augmented Generation systems. Understanding what a language model is, and what it is not, is essential for understanding why retrieval is necessary.

A language model can generate fluent, coherent text. However, its knowledge is limited to what was encoded during training. It cannot access information that was not in the training data, and it cannot update its knowledge after training is complete. These limitations are fundamental, not incidental. They are intrinsic to how language models work.

RAG exists because language models, despite their capabilities, cannot know everything and cannot learn new facts at inference time. Retrieval provides a mechanism to supply external information that the model can condition on when generating a response.

## Key constraints

A language model is not a database. It does not store facts in a retrievable format. Instead, it stores patterns that allow it to produce text that is statistically consistent with its training data.

A language model is not an oracle. It can generate text that sounds authoritative but is factually incorrect, because its outputs are based on learned patterns rather than verified knowledge.

A language model is fixed after training. The parameters that define its behavior do not change during inference. This means that any new information must be provided externally, through the input, rather than learned on the fly.

## Relationship to other concepts

Language models rely on architectures such as transformers to process sequences of text. They produce outputs through autoregressive generation, predicting one token at a time. They use embeddings to represent words and phrases internally. The distinction between training and inference determines when and how their knowledge is established. Together, these concepts explain both the capabilities and the limitations that make retrieval necessary.
