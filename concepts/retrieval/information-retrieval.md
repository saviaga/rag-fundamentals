# Information Retrieval

## One-sentence definition

Information retrieval is the task of selecting relevant items from a large collection in response to an information need expressed by a user or a system.

## Core idea

At its core, information retrieval is about reducing scale. Given a very large collection of documents, the goal is to identify a much smaller subset that is likely to be relevant to a particular query. The key abstraction that makes this possible is relevance: a retrieval system estimates which items in the collection are worth examining further for a given information need.

Retrieval does not produce answers, explanations, or summaries. Instead, it selects candidates. Its value lies in narrowing an unmanageably large search space to a tractable set of documents that downstream components can inspect, rank more carefully, or use as evidence. In this sense, retrieval is a filtering step that precedes any deeper reasoning or generation.

This abstraction does not depend on how relevance is computed. Different retrieval approaches define and estimate relevance in different ways, but the underlying task remains the same. Given an information need and a collection, decide which items are likely to matter. The effectiveness of a retrieval system is judged by how well its selected candidates align with what a human would consider relevant, a judgment shaped by both representation choices and comparison mechanisms.

## Why this concept matters for RAG

Language models store knowledge in their parameters, but that knowledge is limited, static, and imperfect. No model can internalize all facts, keep pace with new information, or reliably recall precise details across all domains. These limitations become especially clear when systems are asked about recent events, specialized topics, or exact factual claims.

Retrieval provides a way to address these limits by supplying external information at inference time. Instead of relying only on what the model learned during training, a system that uses retrieval can draw on a large and up to date collection of documents. In this role, retrieval acts as a bridge between the fixed capacity of a language model and the open ended range of information needs it must support.

In modern systems built around large language models, retrieval is often embedded within broader inference pipelines rather than used as a standalone step. A language model may influence when retrieval is triggered, how queries are formulated, or how retrieved results are interpreted. However, these systems do not change the fundamental nature of retrieval itself. The relevance signals used to select documents remain lexical, semantic, or hybrid in nature. What changes is how retrieval is orchestrated within end-to-end systems, not how relevance is defined.

## Historical context

Information retrieval emerged as a formal field in the mid twentieth century, motivated by the rapid growth of scientific, technical, and governmental documents. Early efforts focused on organizing and searching structured records, and later expanded to full text search over unstructured documents. By the 1960s and 1970s, the field had developed shared evaluation methods and test collections, establishing a strong experimental tradition centered on measuring retrieval effectiveness.

The rise of web search in the 1990s transformed information retrieval into a central problem of computing. Search engines demonstrated that retrieval systems could operate over billions of documents while serving highly diverse and ambiguous information needs. Despite dramatic changes in scale and technology, the core problem remained unchanged. Given a need, identify what is relevant. What evolved over time were the methods used to estimate relevance, not the abstraction itself.

## Canonical papers

- **Introduction to Information Retrieval**
  Cambridge University Press, 2008
  [https://nlp.stanford.edu/IR-book/](https://nlp.stanford.edu/IR-book/)
  This textbook established the canonical reference for information retrieval as a discipline, covering the foundational abstractions, evaluation methods, and system design principles that define the field.

- **Large Language Models for Information Retrieval: A Survey**  
  ACM Transactions on Information Systems (TOIS), 2025  
  [https://dl.acm.org/doi/full/10.1145/3748304](https://dl.acm.org/doi/full/10.1145/3748304)  
  This survey reviews how large language models have shaped modern information retrieval, connecting classic retrieval concepts with neural and generative techniques in a unified framework. 

- **Relevance: A Review of the Literature and a Framework for Thinking on the Notion in Information Science**  
  Journal of the American Society for Information Science and Technology, 2003  
  [https://doi.org/10.1002/asi.10286](https://doi.org/10.1002/asi.10286)
  This paper analyzes how relevance has been defined and understood across disciplines, underscoring its central role in the conceptual foundations of retrieval systems.

## Common misconceptions

A common misconception is that retrieval is the same as answering questions. In reality, retrieval selects documents or passages that may contain relevant information, but it does not extract, verify, or synthesize answers. Understanding this distinction is essential for reasoning about how retrieval fits into larger systems.

Another misunderstanding is the belief that retrieval returns facts. Retrieval systems return items from a collection, and those items may be relevant, partially relevant, or misleading. Relevance estimates are approximations, not guarantees of accuracy or truth.

It is also sometimes assumed that retrieval is unnecessary in systems built around large neural models. This view confuses memorization with access. Even powerful models cannot store all possible information or remain current over time. Retrieval remains essential because it allows systems to access external knowledge beyond what is encoded in model parameters.

## Limitations

Information retrieval is inherently limited by how relevance is estimated. No system can perfectly separate relevant from irrelevant items, and every approach involves tradeoffs between precision, recall, and efficiency. Any representation of queries and documents emphasizes certain aspects of meaning while discarding others, which means that retrieval is always an approximation.

Retrieval also depends on the contents of the collection itself. If relevant information is missing, no retrieval method can recover it. In addition, retrieval systems are sensitive to how information needs are expressed. The same underlying need, phrased differently, can lead to different results depending on how relevance is modeled.

These constraints motivate the study of different ways to define and operationalize relevance, each offering distinct strengths and tradeoffs. The next concepts examine how relevance is instantiated in practice through different retrieval paradigms.
