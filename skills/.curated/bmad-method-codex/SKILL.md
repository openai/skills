---
name: bmad-method-codex
description: Pomaga stosować BMAD-METHOD w Codex 5.3, utrzymując spójność workflowów i kontrolując zgodność wersji skilla oraz wydania BMAD-METHOD.
---

# BMAD-METHOD Skill for Codex 5.3

## Zakres zastosowania

Używaj tego skilla, gdy użytkownik:
- chce wdrożyć BMAD-METHOD w projekcie i uruchomić workflowy,
- pyta o komendy BMAD i artefakty procesu,
- wymaga aktualizacji implementacji po nowych wydaniach BMAD-METHOD lub zmianie środowiska Codex.

## Zasady działania

1. W odpowiedzi podawaj:
   - co zostało wykonane,
   - co jest bieżącym krokiem,
   - co jest kolejnym krokiem.
2. Nie zakładaj istnienia plików ani komend bez potwierdzenia w instalacji.
3. Najpierw odwołuj się do aktualnych źródeł lokalnych i snapshotów.
4. Utrzymuj komunikaty neutralne i praktyczne, bez sugestii specyficznych dla pojedynczej wersji modelu.

## Wejście do pracy

1. `python3 scripts/sync_bmad_method.py check`
2. Jeśli skrypt zwróci `SKILL_NOTICE`, poinformuj użytkownika, że ustawienie jest prawdopodobnie nieoptymalne i zasugeruj:
   - instalację/aktualizację najnowszej wersji skilla,
   - uruchomienie `python3 scripts/sync_bmad_method.py sync`,
   - powtórzenie `check`.
3. Zweryfikuj zasoby:
   - `references/command-matrix.md`
   - `references/upstream/latest-release-summary.md`
   - `references/upstream/CHANGELOG.md` (jeśli istnieje)

## Najczęstsze komendy BMAD

- Strategia produktu: `/bmad-bmm-create-prd`
- Szybki loop: `/bmad-bmm-quick-spec`, `/bmad-bmm-quick-dev`
- Architektura: `/bmad-bmm-create-architecture`
- Planowanie: `/bmad-bmm-sprint-planning`
- Backlog: `/bmad-bmm-create-epics-and-stories`
- Wdrożenie: `/bmad-bmm-dev-story`
- Przegląd: `/bmad-bmm-code-review`
- Testy: `/bmad-bmm-automate`

Pełna mapa znajduje się w `references/command-matrix.md`.

## Rekomendowany szkielet odpowiedzi

```text
FAZA:
- ...

WYKONANE:
- ...

KROK_NASTĘPNY:
- ...
```

Szczegóły stylu i jakości decyzji: `references/codex-5-3-runtime.md`.

## Procedura po zmianach BMAD lub Codex

1. Uruchom `python3 scripts/sync_bmad_method.py check --json`.
2. Jeśli `release_changed` jest `true`, uruchom `python3 scripts/sync_bmad_method.py sync`.
3. Zaktualizuj mapy komend/artefakty po zmianach w `references/upstream/*`.
4. Przejdź do `references/release-sync-protocol.md` przed publikacją i publikuj tylko wtedy, gdy mapy i snapshoty są spójne.

## Testy skryptu i smoke-check

- `python3 scripts/test_sync_bmad_method.py` — minimalny pakiet testów skryptu (`unit + smoke` z stubami endpointów).
- `python3 scripts/sync_bmad_method.py check --json --max-retries 3 --retry-delay 1.0` — smoke-check integracyjny łączący się z upstream.

## Przygotowanie do publikacji w openai/skills

1. Publikacja oficjalna trafia do `skills/.curated` repozytorium `openai/skills`.
2. Wersje eksperymentalne można testować przez `skills/.experimental`.
3. Przed PR weryfikuj:
   - `[ ]` `SKILL.md`
   - `[ ]` `agents/openai.yaml`
   - `[ ]` `scripts/sync_bmad_method.py`
   - `[ ]` `references/skill-manifest.json`
   - `[ ]` `python3 scripts/test_sync_bmad_method.py`
   - `[ ]` `python3 scripts/sync_bmad_method.py check --json`

## Reakcja na problemy

- Gdy polecenie/plik w planie nie istnieje:
  1. Wypisz konkretny brak,
  2. Zaproponuj bezpieczny następny krok (`check`/`sync`),
  3. Podaj krótki wariant alternatywny.
