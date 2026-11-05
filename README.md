# Stardust NEXT – Manual

Dokumentacja techniczna platformy balonów stratosferycznych Stardust NEXT. Platformę opracowało Koło Naukowe SimLE (Politechnika Gdańska).

Manual daje niezbędne minimum, aby nowy zespół wyjął sprzęt z szafki i wykonał misję stratosferyczną.

## Spis treści

0. [Wprowadzenie](00_INTRO.md)
1. [Historia i wnioski](01_HISTORY.md)
2. [Wymagania prawne](02_LEGAL.md)
3. [Segment naziemny](03_GROUND.md) – stanowisko startowe, tankowanie, stacje odbiorcze
4. [Segment lotny](04_FLIGHT.md) – powłoka, spadochron, olinowanie, odcinacz, gondola
5. [Oprogramowanie](05_SOFTWARE.md) – planowanie, predykcja, śledzenie
6. [Elektronika](06_ELECTRONICS.md) – tracker, komputer pokładowy, lokalizator
7. [Wykaz materiałów i narzędzi](07_BOM.md)
8. [Instrukcje montażu](08_ASSEMBLY.md)
9. [Listy kontrolne](09_CHECKLISTS.md)
10. [Prowadzenie projektu i dokumentacja](10_PROJECT.md)

## PDF

Akcja GitHub `Build PDF` składa wszystkie rozdziały (`NN_*.md`) w jeden plik `Stardust-NEXT-Manual.pdf`.

- Każdy push i pull request: PDF jest artefaktem przebiegu akcji (zakładka *Actions*).
- Tag `v*` (np. `v1.0`): PDF jest dołączony do wydania (zakładka *Releases*).

Wydanie nowej wersji:

```sh
git tag v1.0
git push origin v1.0
```

Budowa lokalna (wymaga `pandoc`, XeLaTeX i ImageMagick; alternatywnie `nix-shell .scripts/shell.nix`):

```sh
.scripts/generate_pdf.sh
```

Wynik: `pdf/Stardust-NEXT-Manual.pdf`.

## Zasady edycji

- Jeden rozdział = jeden plik `NN_NAZWA.md`. Numer określa kolejność w PDF.
- Każdy plik zaczyna się nagłówkiem `#` (tytuł rozdziału).
- Obrazy umieszczaj w katalogu `assets/` i wstawiaj ścieżką względną: `![Opis](assets/plik.jpg)`.
- Pisz krótkie zdania i polecenia w trybie rozkazującym.
- Pisz ogólnie: dokumentacja ma działać dla każdej przyszłej misji. Dane konkretnych misji zapisuj tylko w rozdziale „Historia i wnioski”.
