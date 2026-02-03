# Training vs Inference

## Definition

Training is the process of adjusting a model's parameters based on data. Inference is the process of using a trained model to produce outputs without modifying its parameters. These two phases are fundamentally distinct and do not overlap.

## Core idea

During training, a model is exposed to large amounts of data and iteratively updates its internal parameters to minimize error on a learning objective. This is when the model acquires its capabilities: its knowledge of language, its ability to follow instructions, and its patterns of reasoning are all established during training.

During inference, the model's parameters are frozen. The model receives an input, processes it through its fixed computations, and produces an output. No learning occurs. The model cannot update its knowledge, correct its biases, or acquire new information based on the inputs it receives at inference time.

This distinction is not a design choice that can be easily changed. It reflects the fundamental structure of how neural networks operate. Training requires computing gradients and updating millions or billions of parameters, which is computationally expensive and requires access to the model's internals. Inference is a forward pass through a fixed function.

## Why this concept matters for RAG

The separation between training and inference is the core reason why RAG exists.

A language model's knowledge is fixed at training time. If the model was trained on data up to a certain date, it has no knowledge of events after that date. If the model was not exposed to a particular domain or fact during training, it cannot reliably produce accurate information about it.

At inference time, the model cannot learn new facts from the user's query or from retrieved documents. It can only use information that is present in its input to condition its output. This is why retrieval is necessary: it provides a mechanism to inject external, up-to-date, or domain-specific information into the model's input, compensating for the limitations of static parametric knowledge.

Understanding this boundary clarifies what retrieval can and cannot do. Retrieval can supply information that the model lacks. It cannot teach the model new skills, change its reasoning patterns, or permanently update its knowledge.

## Key constraints

Model knowledge is static after training. The facts, patterns, and capabilities encoded in the parameters do not change during inference. Any appearance of learning or adaptation is an artifact of how the model uses its input, not evidence of parameter updates.

Inference is stateless across requests. Each inference call is independent. The model does not remember previous queries or retrieved documents. If information must persist across interactions, it must be explicitly included in each new input.

Updating model knowledge requires retraining. To incorporate new information into the model's parameters, the model must be retrained or fine-tuned, which is a separate and expensive process. This cannot happen during normal inference.

## Relationship to other concepts

The training-inference boundary explains why language models need external support to handle knowledge-intensive tasks. It motivates the design of RAG systems, which use retrieval to provide information at inference time that the model could not have learned during training. It also explains why context windows and prompting are so important: since the model cannot update its knowledge, the only way to influence its behavior at inference time is through the input it receives. The constraints established during training, including what the model knows and how it reasons, are fixed. Retrieval, context construction, and prompting operate within these constraints rather than changing them.
