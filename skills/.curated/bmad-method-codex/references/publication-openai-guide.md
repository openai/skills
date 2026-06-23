# Publish guide for openai/skills

## Miejsce docelowe

- Oficjalna publikacja: `https://github.com/openai/skills`, katalog `skills/.curated`.
- Wersje eksperymentalne: `skills/.experimental`.

## Pakiet minimalny

Skopiuj katalog skilla do:
- `skills/.curated/bmad-method-codex`

Zawartość katalogu do zachowania:
- `SKILL.md`
- `agents/openai.yaml`
- `scripts/sync_bmad_method.py`
- `scripts/test_sync_bmad_method.py` (opcjonalnie, zależy od standardu repo)
- `scripts/ci_smoke_sync_bmad_method.sh` (opcjonalnie)
- `references/` (w tym `skill-manifest.json`, protokoły i mapy)
- `state/` (opcjonalnie; zwykle pusty stan generowany lokalnie)

## Checklist przed PR

- [ ] Uruchom `python3 scripts/test_sync_bmad_method.py`.
- [ ] Uruchom `python3 scripts/sync_bmad_method.py check --json`.
- [ ] Zweryfikuj, że `references/skill-manifest.json` zawiera właściwą `skill_version`.
- [ ] Zweryfikuj, że `SKILL.md` i `agents/openai.yaml` odpowiadają sobie.
- [ ] Sprawdź, że `check` wypisuje `SKILL_NOTICE` tylko w scenariuszach realnego driftu.

## Dla GitHub PR

- Opisz w PR, które pliki zostały dodane/zmienione.
- Dodaj krótką notkę: „zabezpieczenia sieciowe (retry/backoff), test skryptu, smoke-check dla `check --json`”.
