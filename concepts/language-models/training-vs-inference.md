# Training vs Inference

## Definition

Training is the process of adjusting a model’s parameters based on data. Inference is the process of using a trained model to produce outputs without modifying its parameters. These two phases are fundamentally distinct and do not overlap.

## Core idea

During training, a model is exposed to large amounts of data and repeatedly updates its internal parameters to reduce error on a learning objective. This is when the model acquires its capabilities. Its knowledge of language, its ability to follow instructions, and its patterns of reasoning are all established during training.

During inference, the model’s parameters are fixed. The model receives an input, applies a fixed computation, and produces an output. No learning occurs. The model cannot update its knowledge, correct its biases, or incorporate new information into its parameters based on what it sees at inference time.

This separation is not an arbitrary design choice. It follows from how neural networks operate in practice. Training requires computing gradients and updating millions or billions of parameters, which is computationally expensive and requires access to the model’s internals. Inference is a forward pass through a fixed function.

## Why this concept matters for RAG

The separation between training and inference is the core reason why Retrieval Augmented Generation exists.

A language model’s knowledge is fixed at training time. If the model was trained on data up to a certain point, it has no awareness of events after that point. If it was never exposed to a particular domain or fact during training, it cannot reliably produce accurate information about it.

At inference time, the model cannot learn new facts from a user query or from retrieved documents. It can only condition its output on information that appears in its input. Retrieval is therefore necessary. It provides a way to supply external, up to date, or domain specific information to the model at inference time, compensating for the limitations of static parametric knowledge.

Understanding this boundary clarifies what retrieval can and cannot do. Retrieval can supply information the model lacks. It cannot teach the model new skills, alter its reasoning patterns, or permanently update its knowledge.

## Key constraints

Model knowledge is static after training. The facts, patterns, and capabilities encoded in the parameters do not change during inference. Any apparent learning or adaptation reflects how the model uses its input, not changes to its parameters.

Inference is stateless across requests. Each inference call is independent. The model does not retain memory of previous queries or retrieved documents. If information must persist across interactions, it must be explicitly included in each new input.

Updating model knowledge requires retraining. Incorporating new information into the model’s parameters requires retraining or fine tuning, which is a separate and expensive process and cannot occur during normal inference.

## Relationship to other concepts

The training inference boundary explains why language models require external support for knowledge intensive tasks. It motivates the design of RAG systems, which use retrieval to supply information at inference time that the model could not have learned during training.

It also explains why context windows and prompting are so important. Since the model cannot update its knowledge, the only way to influence its behavior at inference time is through the input it receives. Retrieval, context construction, and prompting all operate within the constraints established during training rather than changing them.
