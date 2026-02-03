# What Is a Language Model

## Definition

A language model is a system that assigns probabilities to sequences of text. Given a sequence of words, it estimates how likely that sequence is, or how likely a particular word is to come next.

## Core idea

Language models learn statistical patterns from large collections of text. During training, they are exposed to text from many sources and adjust internal parameters to capture regularities in how language is structured. After training, these parameters are fixed, and the model can be used to evaluate or generate text based on the patterns it has learned.

The key abstraction is that a language model encodes a compressed representation of language as observed in its training data. Rather than storing explicit facts, the model captures patterns of usage, association, and structure. This allows it to make predictions about text it has never seen before, as long as that text resembles patterns encountered during training.

## Why this concept matters for RAG

Language models are the generation component in Retrieval Augmented Generation (RAG) systems. Understanding what a language model is, and what it is not, is essential for understanding why retrieval is necessary.

A language model can generate fluent and coherent text, but its knowledge is limited to what was encoded during training. It cannot access information that was not present in its training data, and it cannot update its knowledge after training is complete. These limitations are fundamental and follow directly from how language models are built and used.

RAG exists because language models, despite their capabilities, cannot know everything and cannot learn new facts at inference time. Retrieval provides a way to supply external information that the model can condition on when generating a response.

## Key constraints

A language model is not a database. It does not store facts in a structured or directly retrievable form. Instead, it stores statistical patterns that allow it to produce text consistent with its training data.

A language model is not an oracle. It can generate text that sounds confident and authoritative while still being factually incorrect, because its outputs are based on learned correlations rather than verified knowledge.

A language model is fixed after training. The parameters that define its behavior do not change during inference. Any new information must be provided through the input rather than learned during use.

