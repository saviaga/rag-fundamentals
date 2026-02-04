# Common RAG Failures

## Definition

Common RAG failures are structural failure modes that appear in naive or vanilla RAG systems when retrieval, context construction, or grounding is poorly designed. These failures are not historical or obsolete. They still occur in modern systems whenever the core constraints of retrieval augmented generation are not explicitly addressed.

## Why vanilla RAG fails

Vanilla RAG implements the simplest possible connection between retrieval and generation. Documents are retrieved, concatenated into a context, and passed to a language model to generate a response. This simplicity makes vanilla RAG easy to build, but it also creates fundamental weaknesses.

The retrieve then generate pattern assumes that retrieval works, that the constructed context is usable, and that the model will rely on the provided evidence. It includes no mechanism to verify retrieval quality, resolve ambiguity, detect missing information, or ensure that the model grounds its answer in the retrieved content.

When any part of the pipeline underperforms, the failure propagates forward. There is no feedback loop, no correction step, and no signal that something went wrong. The system still produces an answer, often fluent and confident, even when it is incorrect or unsupported.

Understanding these failure modes is essential for recognizing the limits of vanilla RAG and for understanding why more structured approaches exist.

## Retrieval failures

The most basic failure occurs when retrieval does not surface relevant documents. If the necessary information exists in the collection but is not retrieved, the generation stage has no access to it. The model must either guess, hallucinate, or answer based on incomplete evidence.

Retrieval can fail for many reasons. The query may be ambiguous or underspecified. The embedding model may not capture the relevant semantic relationships. Important documents may use different terminology than the query. Retrieval thresholds may filter out passages that are weakly matched but still critical.

In vanilla RAG, these failures are invisible. The model cannot tell whether the retrieved documents are the best available evidence or whether better information exists elsewhere in the collection.

## Context construction failures

Even when relevant documents are retrieved, they must be assembled into a context the model can use. This step introduces additional failure modes.

Truncation removes information. When retrieved content exceeds the context window, some passages must be dropped. If the most relevant information is truncated, the model cannot use it.

Ordering affects attention. Language models do not treat all positions equally. Information placed in low attention regions may be ignored even if it is relevant.

Redundancy wastes capacity. Including multiple passages that repeat the same information consumes context space without adding value, reducing room for diverse or complementary evidence.

Lack of structure obscures meaning. When passages are concatenated without clear boundaries or framing, the model may struggle to identify sources, assess importance, or understand how the information relates to the query.

## Grounding failures

Grounding failures occur when the model produces text that is not supported by the retrieved evidence. The documents may be present in the context, but the model ignores them, misinterprets them, or blends them with its internal knowledge in ways that introduce errors.

This can happen when the model’s training priors override the retrieved content, when the evidence is ambiguous or conflicting, or when the prompt does not clearly instruct the model to prioritize retrieved information.

Grounding failures are especially dangerous because the output often sounds confident and coherent. There is no visible signal that the answer is unsupported by the evidence.

## Compound failures

In real systems, failures often combine. A weak retrieval result may be truncated, poorly ordered, or ambiguously framed, and then ignored by a model that defaults to its internal assumptions. Each issue alone might be survivable, but together they produce answers that are confidently wrong.

Vanilla RAG offers no way to detect or recover from these compound failures. The pipeline runs once and produces an output regardless of whether the underlying process succeeded.

## Why these failures persist

These failures are not simple bugs. They follow directly from the structure of vanilla RAG.

Retrieval happens once, before generation, with no opportunity for refinement. Context is constructed statically, without feedback from the model. The model is not constrained to justify its output using retrieved evidence. There is no verification step and no self correction mechanism.

Any system that follows this pattern will exhibit the same weaknesses, regardless of implementation quality. Recognizing these limitations explains why more advanced RAG designs introduce iteration, feedback, verification, or adaptive retrieval.

## Mitigating retrieval failures

| Failure Mode | Description | Mitigation |
|--------------|-------------|------------|
| **Missing content** | Answer not in corpus | Ensure corpus coverage; detect unanswerable queries |
| **Vocabulary mismatch** | Query/document language differs | Query expansion; hybrid retrieval; better embeddings |
| **Ambiguous queries** | Multiple valid interpretations | Query clarification; user context; re-ranking |
| **Needle in haystack** | Relevant doc ranks too low | Increase k; use re-rankers; improve chunking |

A perfect LLM cannot compensate for bad retrieval. The retrieved context IS the model's knowledge for that query. See `code-examples/retrieval/retrieval_failure_example.py` for demonstrations of each failure mode.

## Relationship to other concepts

Common RAG failures arise directly from the structure of vanilla RAG. They show why retrieval quality, context window constraints, and prompting all matter, and why none of them can be treated as minor implementation details.

They also clarify the role of fine tuning. Fine tuning can shape model behavior, but it cannot compensate for missing evidence, poor retrieval, or ungrounded generation at inference time.

Understanding these failures motivates the study of more advanced RAG patterns that explicitly address the limitations of the vanilla approach.