# Transformers

## Definition

A transformer is a neural network architecture for processing sequences that allows every element in the input to directly attend to every other element. This design enables the model to capture relationships between tokens regardless of their distance in the sequence.

## Core idea

Earlier sequence models processed text step by step, passing information forward through the sequence. This made it difficult to model long range relationships, because information had to flow through many intermediate steps and could degrade along the way.

Transformers introduced a different approach. Instead of processing tokens sequentially, a transformer processes the entire sequence at once. It computes attention scores between all pairs of tokens, allowing the model to directly relate any position in the input to any other position. This makes it easier to capture long range dependencies and allows computation to be parallelized efficiently.

The central mechanism is self attention. For each token, the model computes a weighted combination of all other tokens in the sequence. The weights are learned based on the content of the tokens themselves, allowing the model to dynamically focus on different parts of the input depending on context. This flexibility is what enables transformers to model complex linguistic structure and meaning.

## Why this concept matters for RAG

Transformers are the architectural foundation of modern language models, and their properties directly shape how RAG systems must be designed.

First, transformers operate over a fixed size input called the context window. The model can only attend to tokens that fit within this window during inference. Any information outside the window is completely invisible to the model. This makes selective retrieval and careful context construction essential. Retrieved documents must be chosen and truncated so that the most useful information fits within the available space.

Second, transformers process the full input context in a single forward pass. The model does not revise its understanding of the input during generation. It generates tokens based on a static snapshot of the context it was given. This means that if important information is missing, poorly ordered, or unclear in the context, the model cannot compensate for it during inference.

These properties explain why retrieval, context windows, and inference pipelines are tightly coupled in RAG systems.

## Key constraints

The context window is finite. Each transformer model has a maximum sequence length determined by its architecture and practical compute limits. Information beyond this limit cannot be processed.

Attention is computationally expensive. The cost of attention grows rapidly as the context length increases, which places practical limits on how much retrieved content can be included even when larger context windows are available.

Transformers have no persistent memory across inference calls. Each request is processed independently. The model does not remember previous interactions unless they are explicitly included in the current input.

## Canonical papers

- **Attention Is All You Need**
NeurIPS, 2017
https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html

This paper introduced the transformer architecture and the self attention mechanism, establishing the foundation for modern large language models and their fixed context window constraints.

- **BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**
NAACL, 2019
https://aclanthology.org/N19-1423/

This work demonstrated how transformer encoders can learn powerful contextual representations, influencing both retrieval embeddings and downstream language understanding tasks.

- **Language Models are Few-Shot Learners**
NeurIPS, 2020
https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html

This paper showed that large transformer based language models can perform tasks through prompting alone, highlighting the importance of context windows and input construction at inference time.