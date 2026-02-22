# Protokół synchronizacji po wydaniach

## Cel
Utrzymać skill i mapy komend zgodne z bieżącą wersją BMAD-METHOD.

## Co uruchomić

1. `python3 scripts/sync_bmad_method.py check`

- `status: up_to_date`
  - normalny stan, gdy nie ma zmian release ani snapshotów.
- `status: update_available`
  - uruchom `python3 scripts/sync_bmad_method.py sync`.

2. `python3 scripts/sync_bmad_method.py sync`

- zapisze snapshoty plików do `references/upstream/`
- zapisze stan w `state/bmad-release-state.json`
- utworzy `references/upstream/latest-release-summary.md`

## Pierwsze uruchomienie

Podczas pierwszego uruchomienia skrypt wykonuje zestaw kontroli:

- porównanie wersji local skilla z wersją `references/skill-manifest.json` w aktywnej instalacji (`versions_match`),
- sprawdzenie najnowszego releasu z endpointu release,
- sprawdzenie wersji środowiska Codex i porównanie jej z ostatnim zapisanym stanem.

Jeśli którykolwiek warunek jest niespójny:
- `is_optimal` = `false`,
- skrypt wypisuje `SKILL_NOTICE` z zaleceniem: `sync` lub `check --json` i ponowne uruchomienie.

## Interpretacja zmian

- Patch/minor: odśwież snapshot, potem sprawdź komendy/artefakty.
- Major: ręczny przegląd `SKILL.md` i `references/command-matrix.md`, potwierdź, które komendy zniknęły lub zostały dodane.

## Checklist po synchronizacji

- [ ] Czy `references/command-matrix.md` odpowiada nowym komendom?
- [ ] Czy snapshot dokumentacji jest świeży (`references/upstream/`)?
- [ ] Czy wymagane komendy instalacyjne (`install`, `non-interactive`) pozostają aktualne?
- [ ] Czy `SKILL.md` wymaga doprecyzowania nowych workflowów?
- [ ] Czy `references/skill-manifest.json` opisuje spójną wersję skilla?
- [ ] Czy zmiany są gotowe do publikacji (`status: ready`)?

## Kontrola jakości skilla

- Security:
  - brak wykonywania komend powłoki w skrypcie,
  - ograniczony ruch sieciowy do wyznaczonych endpointów,
  - retry z exponential backoff dla błędów tymczasowych i limitu API,
  - walidacja JSON przy każdym wczytywaniu.
- Senior dev:
  - tryb `check` nie blokuje pracy przy ostrzeżeniach (działa informacyjnie),
  - stan jest odtwarzalny i jawny (`state/bmad-release-state.json`),
  - obsługa parametrów sieciowych (`--max-retries`, `--retry-delay`, `--request-timeout`, `--release-url`, `--raw-base`).
- Vibe:
  - komunikaty są fazowe i neutralne;
  - logika jest czytelna i rozwijalna.

## Po wydaniu nowego Codex

1. Zapisz nową wersję modelu.
2. Uruchom `check`.
3. Jeśli runtime zmienił się od ostatniego stanu, uruchom `sync`.
4. Zweryfikuj `/bmad-help` i podstawowe komendy BMAD.
5. W razie dryfu promptu dopracuj `references/codex-5-3-runtime.md`.

## Testy i CI smoke-check

- `python3 scripts/test_sync_bmad_method.py`
- `python3 scripts/sync_bmad_method.py check --json`
- CI powinno uruchamiać powyższe jako check bezpieczeństwa i kompatybilności skilla.
