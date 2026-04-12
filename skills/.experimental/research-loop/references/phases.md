# Codex Research Loop Phases

All phases are small and inspectable. Python helper phases write deterministic artifacts; Codex-native phases perform judgment and code generation.

| Phase | Owner | Output |
| --- | --- | --- |
| `source_intake` | Python + Codex | source snapshot and inventory |
| `mempalace_context` | Python | current-head memory pack |
| `council_knowledge` | Python | expert council route |
| `expert_forum_coverage` | Python | coverage score and expansion queue |
| `literature_refresh` | OpenAlex + Codex WebSearch | papers and web evidence |
| `knowledge_publish` | Python | cycle knowledge base |
| `advisor_design` | Codex | advisor manifest and action backlog |
| `execution_packet` | Python | one selected micro-step |
| `executor_run` | Codex | runnable source changes and executor manifest |
| `advisor_reflection` | Python | post-execution constraints |
| `openspace_retrospective` | Python | loop improvement notes |
| `next_cycle_handoff` | Python | next-cycle handoff |
| `star_office_status` | Python | local dashboard status |
| `overwatcher_check` | Python | observe-only workflow health report |
| `github_publish` | Python | target repo delivery |

Do not rely on Ollama native web search. If fresh web evidence is needed inside a Codex-native phase, use Codex WebSearch and pass short, attributed snippets into the relevant helper stage.

