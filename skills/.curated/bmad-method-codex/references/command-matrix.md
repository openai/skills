# BMAD Command Matrix (Codex 5.3)

## Discovery and alignment

- `/bmad-help` - szybkie rozpoznanie następnego kroku.
- `/bmad-agent-bmm-*` - uruchamia agenta (np. `dev`, `pm`, `architect`, `sm`).

## Faza 1: Analiza (opcjonalna)

- `bmad-bmm-bias` (gdy repo zawiera moduł bias),
- `bmad-bmm-research`,
- `bmad-bmm-create-product-brief`.

## Faza 2: Planowanie

- `bmad-bmm-create-prd`
- `bmad-bmm-create-ux-design`

## Faza 3: Projektowanie

- `bmad-bmm-create-architecture`
- `bmad-bmm-create-epics-and-stories`
- `bmad-bmm-check-implementation-readiness`

## Faza 4: Implementacja

- `bmad-bmm-sprint-planning`
- `bmad-bmm-create-story`
- `bmad-bmm-dev-story`
- `bmad-bmm-code-review`
- `bmad-bmm-correct-course`
- `bmad-bmm-automate`
- `bmad-bmm-retrospective`

## Quick flow

- `bmad-bmm-quick-spec`
- `bmad-bmm-quick-dev`

## Tasky i narzędzia

Wygodne, pojedyncze komendy wspierające proces:

- `bmad-shard-doc`
- `bmad-index-docs`
- `bmad-editorial-review-prose`

## Konwencja nazw

- `bmad-agent-<module>-<agent>`
- `bmad-<module>-<workflow>`
- `bmad-<task>`

Moduły domyślne:

- `bmm` - BMad Method
- `bmb` - BMad Builder
- `tea` - Test Architect (oddzielny pakiet)
- `cis` - Creative Intelligence
- `gds` - Game Dev Studio

Po każdym odświeżeniu skryptu `sync_bmad_method.py` sprawdź:
- `references/upstream/docs_reference_commands.md`,
- i spójność mapy komend z lokalnym opisem.
