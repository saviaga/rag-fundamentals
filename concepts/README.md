# Concepts

This directory contains foundational concepts underlying Retrieval-Augmented Generation, organized by topic area.

## How this directory is organized

Concepts are grouped into subdirectories by abstraction level:

- **language-models/** — What language models are, how they generate text, and why their knowledge is static
- **retrieval/** — Information retrieval paradigms including lexical, dense, and hybrid approaches
- **inference/** — Inference-time concerns including pipelines, context windows, and prompting
- **rag/** — Retrieval-Augmented Generation as a system pattern, including vanilla RAG and common failures

## How to use this directory

This is a reference, not a tutorial. Concepts are not numbered because they are not meant to be read in a single fixed order. Readers with different backgrounds may enter at different points.

However, if you are new to RAG, the following sequence provides a reasonable starting point:

1. [What is a language model](language-models/what-is-a-language-model.md)
2. [Training vs inference](language-models/training-vs-inference.md)
3. [Information retrieval](retrieval/information-retrieval.md)
4. [Dense retrieval](retrieval/dense-retrieval.md)
5. [Context windows](inference/context-windows.md)
6. [What is RAG](rag/what-is-rag.md)
7. [Vanilla RAG](rag/vanilla-rag.md)
8. [Common RAG failures](rag/common-rag-failures.md)

For a fully guided experience, see the [learning paths](../learning-paths/).

## File structure

Each concept file follows a consistent structure defined in [TEMPLATE.md](TEMPLATE.md). This ensures that every concept covers:

- Definition
- Core idea
- Why the concept matters for RAG
- Historical context (where relevant)
- Common misconceptions
- Limitations
- Relationship to other concepts
