# Autoregressive Generation

## Definition

Autoregressive generation is a method of producing text in which each token is predicted based on all previously generated tokens. The output is built one token at a time, from left to right.

## Core idea

In autoregressive generation, the model does not produce an entire response in a single step. Instead, it generates one token, appends that token to the input, and then predicts the next token based on the extended sequence. This process repeats until the model reaches a stop condition or a maximum length.

Each token prediction depends on two things: the original input provided to the model and all tokens generated so far. As a result, early tokens shape everything that follows. Once a token is generated, it becomes part of the context and cannot be revised.

Although transformer models can process many tokens in parallel during training, generation at inference time is inherently sequential. Each new token depends on the previous output, so tokens must be produced one step at a time.

## Why this concept matters for RAG

Autoregressive generation directly affects how retrieved information is used in RAG systems.

First, input order matters. Because the model attends to all prior context when generating each token, where retrieved passages appear in the prompt influences which information the model relies on during generation.

Second, the model commits as it goes. There is no built-in ability to reconsider earlier tokens once they are generated. If the model starts down an incorrect or poorly grounded path, it will often continue unless the system intervenes externally.

Third, generation cost scales with output length. Each new token requires a forward pass that attends to the full context. Longer responses are more expensive to generate, creating tradeoffs between response detail, latency, and cost.

## Key constraints

Generation is one directional. The model cannot look ahead to future tokens when deciding what to generate next. Each prediction depends only on the past.

Early errors propagate. A poor choice early in generation can bias all subsequent tokens, leading to responses that drift from the intended meaning or evidence.

The model cannot pause to retrieve. Once generation begins, the model can only use the information already present in the context. It cannot issue new retrieval queries unless the system explicitly supports iterative retrieval or generation control.

## Canonical papers

- **Attention Is All You Need**
NeurIPS, 2017
https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html

This paper introduced the transformer architecture and the autoregressive decoding mechanism used by modern language models, establishing the foundation for token by token generation conditioned on prior context.

- **Language Models are Unsupervised Multitask Learners**
OpenAI, 2019
https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf

This work demonstrated that large autoregressive language models trained on next token prediction can perform a wide range of tasks at inference time without task specific training, popularizing autoregressive generation as the core inference paradigm.

- **On the Dangers of Stochastic Parrots**
FAccT, 2021
https://dl.acm.org/doi/10.1145/3442188.3445922

While not a technical architecture paper, this work discusses the implications of autoregressive text generation, including how models can produce fluent but ungrounded outputs, which is directly relevant to understanding hallucination and grounding issues in RAG systems.
