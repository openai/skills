---
name: rag-vector-search
description: Build, debug, evaluate, or optimize retrieval-augmented generation and vector search systems. Use when working with embeddings, chunking, hybrid search, reranking, FAISS, Qdrant, Chroma, Pinecone, pgvector, sentence-transformers, retrieval evals, or production RAG pipelines.
---

# RAG and Vector Search

Use this skill for retrieval systems. Optimize retrieval before changing generation prompts; bad context cannot be fixed reliably by a stronger answer prompt.

## Validated Version Evidence

This guidance was checked against mined retrieval repositories including `llama-index` 0.14.22, downstream locks with `llama-index` 0.14.10, `sentence-transformers` 5.2.0.dev0 and 5.2.2, and Haystack requirements using `transformers[torch, sentencepiece]>=4.57` and `sentence-transformers>=5.0.0`. Vector-store APIs move quickly, so capture exact versions before changing ingestion or query code:

```bash
python - <<'PY'
from importlib.metadata import PackageNotFoundError, version
for package in ["llama-index", "haystack-ai", "sentence-transformers", "transformers", "qdrant-client", "chromadb", "pinecone", "faiss-cpu", "pgvector"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "not installed")
PY
```

## What This Skill Delivers

Use this skill to build or debug retrieval with measurable evidence. A complete run produces:

- A pipeline map: parser, chunker, embedding model, vector store, filters, retriever, reranker, and generator.
- A small gold set of queries with expected source IDs.
- Inspectable retrieved chunks with source metadata.
- Separate retrieval metrics before any answer-generation judgment.
- A recommendation that names the failing stage when quality is poor.

## Standalone Quick Start

If no framework is already present, prove the retrieval loop with a tiny corpus before adding infrastructure:

```python
import math
import re
from collections import Counter

def tokens(text):
    return re.findall(r"[a-z0-9_]+", text.lower())

def vector(text):
    return Counter(tokens(text))

def cosine(a, b):
    numerator = sum(a[k] * b.get(k, 0) for k in a)
    denom = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return numerator / denom if denom else 0.0

docs = [
    {"id": "install", "text": "Install with pip and configure environment variables."},
    {"id": "auth", "text": "Credentials and API keys belong in the secret store."},
]
queries = [{"query": "where do I put credentials?", "expected": "auth"}]
doc_vectors = [vector(d["text"]) for d in docs]
for item in queries:
    query_vector = vector(item["query"])
    scores = [cosine(query_vector, doc_vector) for doc_vector in doc_vectors]
    ranked = [docs[i]["id"] for i in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)]
    print(item["query"], ranked, "hit@1", ranked[0] == item["expected"])
```

Then replace the toy vectorizer with the repo's embedding/index stack while keeping the same gold-set output shape.

## Workflow

1. Identify the retrieval objective: semantic search, QA grounding, recommendations, deduplication, or memory lookup.
2. Map the pipeline: ingestion, parsing, chunking, embedding, indexing, filtering, retrieval, reranking, answer generation, and evaluation.
3. Create a tiny repeatable test corpus with known relevant answers before tuning.
4. Inspect retrieved chunks directly before judging generated answers.
5. Add evaluation that measures retrieval quality separately from answer quality.

## Ingestion and Chunking

- Preserve source IDs, document titles, section paths, timestamps, and permissions as metadata.
- Chunk by semantic boundaries when possible: headings, paragraphs, functions, classes, or pages.
- Keep chunks small enough for precise retrieval but large enough to preserve local context.
- Store stable checksums to avoid duplicate re-ingestion.
- Respect access control at query time, not only during ingestion.

## Embeddings and Indexes

- Use the same embedding model and preprocessing at ingestion and query time.
- Record embedding model name, dimension, normalization, distance metric, and index type.
- For FAISS, verify index metric and vector normalization.
- For Qdrant, Chroma, Pinecone, or pgvector, verify collection schema, metadata filters, and payload persistence.
- Rebuild the index when embedding dimensions, model, or normalization change.

## References

Open `references/workflows.md` for detailed ingestion design, chunking strategies, vector-store checks, hybrid search, reranking, evaluation metrics, and production review artifacts.

Open `references/mastery.md` for retrieval mental models, failure diagnosis, evaluation philosophy, access-control risks, and review standards.

Open `references/source-evidence.md` when checking whether this skill covers workflows observed in mined/source repository evidence.

## Retrieval Quality

- Evaluate recall with known query-document pairs before adding complex reranking.
- Keep a small gold set table with `query`, `expected_source_id`, `retrieved_source_ids`, `hit@k`, and `rank` so regressions are visible in code review.
- Inspect false positives and false negatives; adjust chunking and metadata filters first.
- Use hybrid lexical + vector search when exact names, IDs, errors, or code symbols matter.
- Add reranking when top-k recall is good but ordering is weak.
- Avoid stuffing too many retrieved chunks into the answer context.

For a first useful eval, five to twenty representative queries are enough if they cover exact identifiers, paraphrased concepts, negative/permission-filtered cases, and recently changed documents.

Recommended debug order:

1. Print retrieved chunks before reading generated answers.
2. Check metadata filters and permissions.
3. Check chunk boundaries and source IDs.
4. Check embedding model/dimension/normalization/index metric.
5. Add hybrid search or reranking only after top-k recall is acceptable.

## Debugging

- Empty results: check filters, collection name, embedding dimension, and ingestion success.
- Irrelevant results: check chunk boundaries, query rewriting, metric choice, and normalization.
- Duplicate results: check document IDs and chunk checksums.
- Slow queries: inspect index type, payload filters, top-k, network latency, and reranker cost.
- Hallucinated answers: verify retrieved context contains the answer before changing the generation model.

## Done Criteria

- A small gold set or smoke queries exercise retrieval.
- Retrieved chunks are inspectable with source metadata.
- Retrieval metrics are reported separately from answer-generation quality.
- Index configuration and embedding model assumptions are documented.
- The final notes include the top retrieved source IDs for at least one representative query.
