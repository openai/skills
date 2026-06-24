# Source Evidence

Use this file as the evidence anchor for the workflow coverage in this skill. The skill should train an agent to build and debug an inspectable retrieval system with measured retrieval behavior.

## Retrieved Sources

- `run-llama/llama_index`: mined node parsing, metadata-aware splitting, node construction, and parser loading evidence.
- `deepset-ai/haystack`: pipeline docs and components for converters, preprocessors, retrievers, joiners, and RAG pipeline visualization.
- `UKPLab/sentence-transformers`: dense embedding, CrossEncoder reranking, SparseEncoder, semantic search, hybrid retrieval, and FAISS quantization evidence.
- Mined package evidence: `llama-index` 0.14.x, `sentence-transformers` 5.2.x, and Haystack stacks with `transformers` / `sentence-transformers` version constraints.

## Workflows Reflected In The Skill

### Ingestion And Chunking

LlamaIndex evidence emphasizes node construction, source relationships, metadata strings, and metadata-aware text splitting. The skill therefore requires:

- source IDs and section metadata;
- chunk boundaries that preserve document structure;
- stable checksums or IDs for re-ingestion;
- explicit parser and chunker mapping before index changes.

### Retrieval Before Generation

Haystack and LlamaIndex pipelines separate conversion, preprocessing, retrieval, prompt construction, and answer generation. The skill requires agents to inspect retrieved chunks before reading generated answers and to report retrieval metrics separately from answer quality.

### Embeddings, Sparse Retrieval, And Reranking

Sentence Transformers evidence includes dense embeddings, sparse encoders, CrossEncoder reranking, semantic search, and FAISS-backed search. The skill covers:

- embedding model and dimension capture;
- distance metric and vector normalization;
- hybrid lexical/vector search for exact IDs and code symbols;
- reranking only after top-k recall is good enough.

### Production RAG Boundaries

The mined workflows show retrieval pipelines as multi-stage systems, so this skill requires a pipeline map and a small gold set. Agents must identify which stage failed: parsing, chunking, embedding, filtering, vector-store schema, retriever, reranker, or generation.

## Review Standard

Reject RAG changes that only tune prompts or swap models. A useful workflow must include inspectable source metadata, test queries with expected source IDs, retrieval metrics, and a diagnosis that names the failing retrieval stage before changing generation.
