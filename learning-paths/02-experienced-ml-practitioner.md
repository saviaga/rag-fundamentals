## Who this is for

This learning path is for readers who already have experience with machine learning and language models but are new to RAG systems. It assumes familiarity with transformers, embeddings, and inference, and skips foundational LLM concepts to focus on retrieval and RAG-specific material.

If you are asking questions like
- "I understand LLMs well, but how does retrieval fit in?"
- "What makes RAG different from just prompting with context?"
- "Where do RAG systems typically fail?"
- this is the right place to start.

## Prerequisites

- Working knowledge of transformer architectures
- Understanding of embeddings and vector similarity
- Familiarity with the training versus inference distinction
- Experience using or building with language models

## How to use this path

Read the files in order. This path is shorter than the absolute beginner path but assumes you can fill in gaps from your existing knowledge.

If any concept feels unfamiliar, consult the corresponding file in `concepts/language-models/` before continuing.

### Step 1: Information retrieval as a problem

Read:
concepts/retrieval/information-retrieval.md

Start here to understand retrieval as a standalone problem that predates neural methods. This framing is essential because RAG failures are often retrieval failures, not generation failures.

Focus on what retrieval systems optimize for and the distinction between relevance and usefulness.

### Step 2: Dense retrieval

Read:
concepts/retrieval/dense-retrieval.md

This file explains how neural embeddings replaced lexical matching in modern retrieval. Since you already understand embeddings, focus on the retrieval-specific concerns: what dense retrieval captures that lexical methods miss, and where it still fails.

### Step 3: What RAG is

Read:
concepts/rag/what-is-rag.md

This file explains Retrieval Augmented Generation at a system level. Given your LLM background, pay attention to how RAG restructures inference rather than modifying the model itself.

The key insight is that RAG addresses the knowledge limitation without retraining.

### Step 4: The vanilla RAG pipeline

Read:
concepts/rag/vanilla-rag.md

This file details the minimal retrieve-then-generate pipeline. You should be able to map each component to systems you already know.

Focus on the assumptions vanilla RAG makes and where those assumptions create brittleness.

### Step 5: Common failure modes

Read:
concepts/rag/common-rag-failures.md

This is the most important file for practitioners. It explains the structural failure modes that appear in production RAG systems regardless of model quality.

Understanding these failures is prerequisite to understanding why advanced RAG variants exist.

## Optional deeper dives

If you want to explore specific areas further:

- **Retrieval strategies**: Read `concepts/retrieval/lexical-retrieval.md` and `concepts/retrieval/hybrid-retrieval.md` to understand the full retrieval landscape
- **System design**: Read `concepts/inference/inference-pipelines.md` and `concepts/rag/hosted-rag-vs-self-hosted.md` for deployment considerations
- **Alternatives**: Read `concepts/rag/fine-tuning-vs-rag.md` to understand when RAG is or is not the right choice

## What you should understand by the end

After completing this learning path, you should be able to:

- Explain how retrieval and generation interact in RAG
- Identify which failures are retrieval problems versus generation problems
- Describe the vanilla RAG pipeline and its assumptions
- Reason about where a RAG system will break before building it

At this point, you are ready to engage with advanced RAG research or the companion repository on RAG system design.
