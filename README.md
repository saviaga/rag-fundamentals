# RAG Fundamentals

This repository provides a foundational, literature-grounded survey of the core concepts underlying Retrieval-Augmented Generation (RAG).
It is intended to serve as a prerequisite reference for readers who want to understand how RAG systems are constructed, before engaging with research on advanced RAG variants and design choices.

The focus of this repository is on conceptual foundations and historical context, rather than implementation tutorials or system optimization.

## Scope and motivation

Modern RAG systems are composed of several well-established components, including information retrieval methods, neural language models, and inference pipelines.
While research on RAG variants often assumes familiarity with these components, they are rarely presented together in a unified and accessible form.

This repository surveys these foundational concepts as they appear in the academic literature, with the goal of clarifying:

- Why these components exist
- What problems they were designed to solve
- How they enable and constrain RAG systems

## What this repository covers

This repository surveys foundational concepts in four areas.

### Retrieval

Concepts related to information retrieval, including lexical and dense retrieval paradigms, and the indexing abstractions that support scalable search.

### Language models

Concepts related to neural language models, with emphasis on transformer-based architectures, embeddings, and autoregressive generation.

### Inference

Concepts related to inference-time system design, including prompting, context windows, and the separation of retrieval and generation.

### RAG basics

An introduction to Retrieval-Augmented Generation itself, including vanilla RAG formulations and early failure modes that motivated subsequent research.

Each concept is treated as a surveyed idea, grounded in canonical papers rather than step-by-step explanations.

## What this repository is and is not

This repository **is**:

- A prerequisite survey for understanding RAG systems
- Grounded in peer-reviewed academic literature
- Focused on conceptual clarity and historical context
- Suitable for students, researchers, and engineers

This repository **is not**:

- A tutorial series
- A how-to guide for implementation
- A framework or library comparison
- A benchmark or evaluation suite

Minimal code examples are included only for conceptual illustration.

## Organization

The repository is organized into the following sections.

### `concepts/`

Foundational concepts grouped by abstraction level.
Each concept file explains the idea, its motivation, and its role in enabling RAG systems, with references to canonical papers.

### `learning-paths/`

Curated reading paths designed to guide readers through the foundational material in a coherent order.

### `code-examples/`

Minimal examples intended to illustrate the interaction between retrieval and generation at a high level.

## Relationship to other repositories

This repository is intended to be read before engaging with research-oriented surveys of RAG system design.

Readers interested in modern RAG variants, design tradeoffs, and research-level comparisons should consult the companion repository:

- [rag-from-zero-to-hero](https://github.com/saviaga/rag-from-zero-to-hero)

## Inclusion criteria

Concepts included in this repository are supported by influential and widely cited academic papers, including work from venues such as:

- NeurIPS
- ICLR
- ACL
- EMNLP
- NAACL

Informal sources such as blog posts or framework documentation are not used as primary references.

## How to use this repository

Readers new to RAG are encouraged to follow the [absolute beginner learning path](learning-paths/01-absolute-beginner.md).
Readers with ML/LLM experience who want a shorter path focused on retrieval and RAG-specific concepts should follow the [experienced ML practitioner path](learning-paths/02-experienced-ml-practitioner.md).
Readers with existing RAG background may browse the [`concepts/`](concepts/) directory directly as a reference.

This repository is designed to establish shared vocabulary and intuition before engaging with advanced RAG research.

## Philosophy

Understanding RAG systems requires understanding the components they are built from.

This repository treats fundamentals not as lessons, but as surveyed concepts whose motivations and limitations shape the design of modern RAG systems.
