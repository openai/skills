# RAG and Vector Search Workflows

Use this reference to make retrieval systems measurable and repeatable.

## Contents

- [Pipeline Map](#pipeline-map)
- [Ingestion](#ingestion)
- [Index Validation](#index-validation)
- [Gold Set](#gold-set)
- [Debugging Order](#debugging-order)
- [Production Review](#production-review)
- [Final Artifact](#final-artifact)

## Pipeline Map

Document each stage:

```text
sources:
parser:
chunker:
metadata:
embedding model:
vector dimension:
normalization:
index/store:
filters:
retriever:
reranker:
generator:
eval set:
```

## Ingestion

Required metadata:

- stable source ID
- title/path/section
- timestamp or revision
- permissions/access group
- checksum

Chunking strategy:

- Docs: headings and paragraphs.
- Code: functions/classes/files.
- PDFs/slides: page plus heading when available.
- Tables: preserve row/column labels.

## Index Validation

After ingestion, check:

- document count
- chunk count
- embedding dimension
- distance metric
- sample payload metadata
- duplicate checksum count

Never mix embeddings from different models or dimensions in one collection unless the store explicitly supports it.

## Gold Set

Create 5-20 queries covering:

- exact names/IDs/errors
- paraphrased concepts
- negative cases
- permission-filtered cases
- recently changed documents

Evaluate:

```text
hit@1
hit@3
hit@5
MRR
false positives
false negatives
```

## Debugging Order

1. Print raw retrieved chunks.
2. Remove generator from the loop.
3. Disable filters temporarily to identify filter bugs.
4. Compare lexical vs vector retrieval for exact terms.
5. Inspect chunk boundaries.
6. Check metric/normalization.
7. Add reranking only when top-k recall is acceptable.

## Production Review

Check:

- access control at query time
- deletion/reindex behavior
- source refresh schedule
- observability for empty/low-confidence results
- citation/source display
- cost and latency of embeddings and reranker

## Final Artifact

Final notes should include:

```text
pipeline map:
index config:
gold queries:
retrieval metrics:
sample retrieved chunks:
answer quality result, if generation was tested:
remaining retrieval risks:
```
