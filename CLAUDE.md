# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a documentation-only repository providing a literature-grounded survey of foundational concepts underlying Retrieval-Augmented Generation (RAG). It serves as a prerequisite reference for understanding how RAG systems are constructed.

**Key principle**: Content is grounded in peer-reviewed academic papers (NeurIPS, ICLR, ACL, EMNLP, NAACL). Informal sources like blog posts or framework documentation are not used as primary references.

## Repository Structure

- **concepts/**: Core reference material organized by topic (language-models, retrieval, inference, rag). Non-linear - concepts can be accessed in any order.
- **learning-paths/**: Sequential reading paths (numbered: 01-absolute-beginner.md, etc.)
- **code-examples/**: Runnable Python examples organized by topic
- **assets/images/**: Diagrams supporting conceptual explanations

## Code Examples

Examples demonstrate concepts through execution. Explanations belong in concept files, not in code.

```
code-examples/
├── embeddings/          # Vector similarity, word analogies
├── retrieval/           # BM25 vs dense, failures, hybrid
├── context/             # Truncation, lost-in-the-middle
└── vanilla_rag/         # Complete RAG pipeline
```

**Running examples:**
```bash
python code-examples/embeddings/cosine_similarity.py
python code-examples/vanilla_rag/retrieve_then_generate.py
```

**Dependencies:** Most examples need only `numpy`. Optional dependencies (gensim, sentence-transformers, openai) enable real embeddings/generation but aren't required—examples fall back to simulated data.

**Guidelines for new examples:**
- Keep under 100 lines when possible
- Use simulated data so examples run without API keys
- **Demonstrate, don't explain** — code shows the concept in action
- **Reference concept files** — end with pointer to relevant `.md` file for explanations
- Link to relevant concept file in docstring

## Content Guidelines

### Creating New Concept Files

All concept files must follow the structure in `concepts/TEMPLATE.md`:

1. **Definition** - Single, precise definition from academic literature
2. **Core idea** - Fundamental abstraction or mechanism
3. **Why this concept matters for RAG** - How it enables/constrains RAG systems
4. **Historical context** - Evolution in research literature
5. **Canonical papers** - Up to 3 papers with venue, year, and link to proceedings
6. **Common misconceptions** - Typical misunderstandings in practice
7. **Limitations** - What the concept doesn't solve

### Content Scope

This repository IS: prerequisite survey, literature-grounded, conceptually focused

This repository IS NOT: tutorial series, how-to guide, framework comparison, benchmark suite

### Learning Paths

- Number paths sequentially (01-, 02-, etc.)
- Design for first-time sequential reading
- Include prerequisites and learning objectives

## Development

No build system or test suite. To run code examples:
```bash
pip install numpy  # minimum requirement
python code-examples/<folder>/<example>.py
```
