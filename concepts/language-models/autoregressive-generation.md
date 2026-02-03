# Autoregressive Generation

## Definition

Autoregressive generation is a method of producing text in which each token is predicted based on all previously generated tokens, with the output sequence built one token at a time from left to right.

## Core idea

In autoregressive generation, the model does not produce an entire response at once. Instead, it generates one token, appends that token to the input, and then generates the next token based on the extended sequence. This process repeats until the model produces a stop signal or reaches a maximum length.

Each token prediction depends on two things: the original input provided to the model and all tokens generated so far. This means that early tokens influence later tokens. The model cannot revise earlier decisions; once a token is generated, it becomes part of the context for all subsequent predictions.

The generation process is inherently sequential. Even though the underlying transformer architecture can process many tokens in parallel during training, generation at inference time proceeds one step at a time because each new token depends on the previous output.

## Why this concept matters for RAG

Autoregressive generation has direct implications for how retrieved information is used in RAG systems.

First, the order of information in the input matters. Because the model generates sequentially and attends to all prior context, the placement of retrieved passages within the prompt can affect which information the model emphasizes when generating each token.

Second, the model commits to its outputs as it generates. There is no built-in mechanism for the model to reconsider earlier tokens based on later context. If the model begins generating an incorrect or poorly grounded response, it cannot self-correct mid-sequence unless the system intervenes externally.

Third, the total cost of generation scales with output length. Each token requires a forward pass that attends to the full context. Longer outputs are more expensive, which creates practical tradeoffs between response thoroughness and computational efficiency.

## Key constraints

Generation is one-directional. The model cannot look ahead to future tokens when deciding what to generate now. Each prediction is conditioned only on the past.

Early errors propagate. A poorly chosen token early in generation can bias all subsequent tokens, leading to outputs that drift from the intended meaning or factual grounding.

The model cannot pause to retrieve. Once generation begins, the model produces tokens based on the context it was given at the start. It cannot issue new retrieval queries mid-generation unless the system architecture explicitly supports iterative retrieval.

## Relationship to other concepts

Autoregressive generation is the standard inference procedure for transformer-based language models. It operates within the context window established by the transformer architecture. The sequential nature of generation interacts with prompting, since the structure and content of the prompt determine the starting point from which all tokens are generated. Understanding autoregressive generation clarifies why retrieved information must be present in the input before generation begins, and why vanilla RAG uses a retrieve-then-generate structure.
