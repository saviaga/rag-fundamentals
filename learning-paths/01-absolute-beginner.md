## Who this is for

This learning path is for readers who are familiar with language models at a high level but are new to Retrieval Augmented Generation. It assumes no prior experience building RAG systems and focuses on building correct mental models before implementation details.

If you are asking questions like
- "What problem does RAG actually solve?"
- "Why can’t a language model just know this?"
- "Where does retrieval fit in?"
- this is the right place to start.

## Prerequisites

- Basic familiarity with language models as a concept
- No prior experience with RAG required
- No deep machine learning background assumed

## How to use this path

Read the files in order. Each concept builds on the previous one.
Do not skip ahead. Many misunderstandings about RAG come from missing early constraints.

This path is conceptual. Code examples are optional and can be explored afterward.

### Step 1: What RAG is and why it exists

Read:
concepts/rag/what-is-rag.md

Start here to understand what Retrieval Augmented Generation is at a system level. This file explains the retrieve then generate pattern and why it exists as a response to the limitations of standalone language models.

Focus on understanding that RAG is not a model, but a way of structuring inference.

### Step 2: What a language model is

Read:
concepts/language-models/what-is-a-language-model.md

Before understanding retrieval, you need to understand the generation component. This file explains what language models do, what they learn during training, and what they cannot do.

Pay particular attention to what is meant by “knowledge encoded in parameters”.

### Step 3: Training versus inference

Read:
concepts/language-models/training-vs-inference.md

This is one of the most important concepts in the entire repository. It explains why language models cannot learn new facts at inference time and why retrieval must happen outside the model.

If this boundary is unclear, RAG will not make sense.

### Step 4: Embeddings and semantic similarity

Read:
concepts/language-models/embeddings.md

Retrieval in modern RAG systems depends on embeddings. This file explains how text is mapped into vectors and how similarity in that space enables semantic retrieval.

You do not need to understand the math. Focus on what embeddings capture and what they lose.

### Step 5: Information retrieval as a problem

Read:
concepts/retrieval/information-retrieval.md

This file zooms out and frames retrieval as a general problem that predates language models. It clarifies what retrieval systems are trying to optimize and why retrieval can fail.

Understanding this helps explain why RAG systems fail even when the language model is strong.

### Step 6: The simplest possible RAG system

Read:
concepts/rag/vanilla-rag.md

This file introduces vanilla RAG, the minimal retrieve then generate pipeline. It is the baseline against which all other RAG designs are compared.

Make sure you understand each step of the pipeline and what assumptions it makes.

### Step 7: Why vanilla RAG breaks down

Read:
concepts/rag/common-rag-failures.md

This file explains the structural failure modes of naive RAG systems. These are not edge cases. They are the default outcomes when retrieval, context construction, or grounding is weak.

This step is critical for understanding why more advanced RAG patterns exist.

### Optional next step: See it in code

Explore:
code-examples/first-rag/

Once the concepts are clear, you can look at a minimal code example to see how the pieces fit together. The goal is not to memorize code, but to connect the conceptual pipeline to an implementation.

## What you should understand by the end

After completing this learning path, you should be able to:

- Explain why RAG exists
- Describe the retrieve then generate pattern
- Explain why language models need retrieval
- Identify the limitations of vanilla RAG
- Reason about where RAG systems fail

At this point, you are ready to move on to more advanced learning paths that focus on retrieval strategies, inference pipelines, and system design tradeoffs.