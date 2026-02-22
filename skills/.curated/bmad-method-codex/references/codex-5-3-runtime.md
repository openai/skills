# Codex 5.3 runtime profile for BMAD

## Zasada główna

Wydaj krótkie odpowiedzi i zawsze podawaj jasno:

1) co zostało już wykonane,
2) co robimy teraz,
3) co jest kolejnym krokiem.

## Szablon odpowiedzi

```text
FAZA:
- Nazwa fazy BMM

WYNIK:
- Potwierdzenie plików i wyników

NASTĘPNE DZIAŁANIE:
- Jeden precyzyjny krok
```

## Ustawienie kontekstu

- Nie opisuj wszystkich możliwości BMAD naraz.
- Nie zakładaj istnienia komend bez potwierdzenia.
- Jeżeli krok zależy od zainstalowanych modułów, zaznacz to jawnie.

## Zasady jakości odpowiedzi

- Używaj krótkich zdań i jednoznacznych poleceń.
- Weryfikuj artefakt: `_bmad/`, `_bmad-output/`, `.claude/commands/`.
- Gdy brak danych wejściowych, poproś o minimum informacji i nie zgaduj.

## Gdy robisz analizę lub review

- Oddziel decyzję od rekomendacji.
- Nie zastępuj komend BMAD własnym pseudo-flow.
- Gdy command matrix się zmieniła, podmień ją przed kolejnym krokiem.
