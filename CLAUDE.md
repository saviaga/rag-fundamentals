# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a documentation-only repository providing a literature-grounded survey of foundational concepts underlying Retrieval-Augmented Generation (RAG). It serves as a prerequisite reference for understanding how RAG systems are constructed.

**Key principle**: Content is grounded in peer-reviewed academic papers (NeurIPS, ICLR, ACL, EMNLP, NAACL). Informal sources like blog posts or framework documentation are not used as primary references.

## Repository Structure

- **concepts/**: Core reference material organized by topic (language-models, retrieval, inference, rag). Non-linear - concepts can be accessed in any order.
- **learning-paths/**: Sequential reading paths (numbered: 01-absolute-beginner.md, etc.)
- **code-examples/**: Minimal illustrative code only
- **assets/images/**: Diagrams supporting conceptual explanations

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

## No Build System

This is a documentation repository with no build, test, or lint commands. The only tooling is standard git operations.
