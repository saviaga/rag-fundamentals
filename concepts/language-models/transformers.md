# Transformers

## Definition

A transformer is a neural network architecture that processes sequences by allowing every element in the sequence to attend to every other element, enabling the model to capture dependencies regardless of their distance in the input.

## Core idea

Before transformers, sequence models processed input in order, one element at a time. This made it difficult to capture relationships between elements that were far apart in the sequence, because information had to be passed through many intermediate steps.

Transformers introduced a different approach. Instead of processing sequentially, a transformer computes attention scores between all pairs of elements in the input. This allows the model to directly relate any two positions in the sequence, regardless of how far apart they are. The result is a more flexible and parallelizable architecture that can capture long-range dependencies more effectively.

The attention mechanism is the core innovation. It computes a weighted combination of all input elements for each output position, where the weights are learned based on the content of the elements themselves. This allows the model to dynamically focus on different parts of the input depending on what is being generated.

## Why this concept matters for RAG

Transformers are the dominant architecture underlying modern language models. Understanding transformers is necessary for understanding two constraints that directly affect RAG system design.

First, transformers operate over a fixed-size input called the context window. The model can only attend to elements within this window. Any information outside the window is invisible to the model during generation. This constraint is why retrieval must be selective: retrieved content must fit within the context window to be useful.

Second, transformers process their entire input in parallel during the forward pass. This enables efficient computation but also means that the model cannot iteratively refine its understanding of the input during a single inference step. The model sees the full context at once and generates based on that snapshot.

## Key constraints

The context window is finite. Transformers have a maximum sequence length determined by their architecture and computational resources. Information beyond this limit cannot be processed.

Attention scales quadratically with sequence length. Longer contexts require more computation, which imposes practical limits on how much information can be included in the input.

Transformers do not have persistent memory across inference calls. Each inference is independent. The model does not remember previous queries or retrieved documents unless they are explicitly included in the current input.

## Relationship to other concepts

Transformers provide the architectural foundation for autoregressive generation, where the model predicts tokens one at a time while attending to all previous tokens. They also rely on embeddings to represent input tokens in a continuous space before attention is applied. The fixed context window of transformers motivates the need for selective retrieval and careful context construction in RAG systems.
