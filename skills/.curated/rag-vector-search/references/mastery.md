# RAG and Vector Search Mastery Notes

## Mental Model

RAG quality is bounded by retrieval quality. Generation can only answer from context that was retrieved, ranked, and passed through correctly.

## Core Contracts

- ingestion preserves source identity
- chunks preserve meaning
- embeddings match query preprocessing
- index metric matches vector normalization
- filters enforce permissions
- reranking improves ordering, not missing recall
- generated answers cite retrieved sources

## Evaluation Philosophy

Separate:

- retrieval recall
- ranking quality
- context packing
- answer faithfulness
- answer usefulness

Do not tune prompts before proving the answer exists in retrieved context.

## Failure Diagnosis

- Empty results: filters, collection name, ingestion.
- Wrong results: chunking, embeddings, metric.
- Good docs but bad order: reranking.
- Good context but bad answer: prompt/generator.
- Unauthorized docs: query-time permission bug.

## Review Standard

A complete RAG change proves:

- pipeline map exists
- gold set exists
- source metadata is inspectable
- retrieval metrics are reported
- at least one false positive/negative is analyzed
- access control is considered
