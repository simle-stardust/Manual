# Stardust NEXT – Podręcznik misji stratosferycznych

Dokumentacja platformy balonów stratosferycznych Stardust NEXT ([Koło Naukowe SimLE](https://www.simle.pl), Politechnika Gdańska).

Podręcznik daje niezbędne minimum, aby nowy zespół wyjął sprzęt z szafki i wykonał misję stratosferyczną. Dokument jest przygotowany do druku dwustronnego i bindowania. Zawiera formularze do wypełnienia długopisem i strony na notatki terenowe.

Pierwsze wydanie: Marcin Jasiukowicz, 2026 – bardzo opóźnione, bo misje z 2023 roku czekały na swój podręcznik trzy lata. Ku chwale kolejnym pokoleniom baloniarzy!

Wydane w 10-lecie pierwszych misji Stardust (2016–2026) – na kolejne 10 lat misji stratosferycznych SimLE.

**Gotowy PDF:** zakładka *Releases* (wydania) albo artefakt ostatniego przebiegu akcji *Build PDF*.

## Spis treści

1. Wprowadzenie
2. Historia i wnioski
3. Planowanie misji
4. Wymagania prawne
5. Segment naziemny – stanowisko, tankowanie, stacje odbiorcze
6. Segment lotny – powłoka, spadochron, olinowanie, odcinacz, gondola
7. Elektronika i łączność
8. Oprogramowanie
9. Instrukcje montażu
10. Wykaz materiałów i narzędzi
11. Prowadzenie projektu i dokumentacja
- A. Formularze (F0–F14)
- B. Notatki terenowe
- Literatura

## Struktura repozytorium

| Ścieżka | Zawartość |
|---|---|
| `tex/main.tex` | Główny plik dokumentu |
| `tex/stardust.sty` | Styl: układ do druku, bloki niełamane, makra formularzy |
| `tex/rozdzialy/` | Rozdziały, formularze, notatki, literatura |
| `tex/figures/diagrams.tex` | Rysunki TikZ |
| `tex/figures/generated/` | Wykresy i tabele z danych (`.scripts/plots.py`) |
| `tex/figures/photos/` | Zmniejszone zdjęcia (`.scripts/photos.py`) |
| `assets/` | Oryginalne zdjęcia z misji; `assets/logo/` – logotypy SimLE (zasady użycia: księga znaku SimLE) |
| `data/` | Dane z lotów (KML, CSV: pozycje, wysokość, rejestratory pokładowe) |
| `papers/` | Artykuły konferencyjne, prace dyplomowe i archiwalna dokumentacja projektu (bez danych osobowych) |

## Budowanie PDF

Akcja GitHub `Build PDF` kompiluje dokument przy każdym pushu i pull requeście (PDF jako artefakt). Tag `v*` dołącza PDF do wydania:

```sh
git tag v1.0
git push origin v1.0
```

Lokalnie (TeX Live z `latexmk`; alternatywnie `nix-shell .scripts/shell.nix`):

```sh
.scripts/generate_pdf.sh        # wynik: pdf/Stardust-NEXT-Podrecznik.pdf
```

Formularze same wypełniają stronę: pola (`\etykieta`, `\krok`, `\linia`, wiersze z `\rosnie`) rosną o wartość zmierzoną w poprzednim przebiegu LaTeX-a i zapisaną w `main.aux`. Dlatego `latexmk` wykonuje kilka przebiegów (limit w `tex/latexmkrc`). Nowe puste wiersze tabel w formularzu kończ makrem `\rosnie`, np. `& & \rosnie\\\hline`.

Po zmianie danych lub zdjęć wygeneruj rysunki ponownie (Python: matplotlib, Pillow, opcjonalnie `geopandas<1.0` dla mapy):

```sh
python3 .scripts/plots.py
python3 .scripts/photos.py
```

## Jak edytować dokument

### Przebieg zmiany

1. Utwórz gałąź (albo fork) repozytorium.
2. Zmień pliki w katalogu `tex/` (opis niżej).
3. Zbuduj PDF lokalnie (`.scripts/generate_pdf.sh`) i sprawdź zmienione strony. Gdy nie masz LaTeX-a, wyślij zmianę i pobierz PDF z artefaktu akcji *Build PDF*.
4. Otwórz pull request. W opisie podaj, co się zmieniło i dlaczego (np. „wniosek z misji, formularz F10”).
5. Po przeglądzie scal zmianę. Gdy zmiana jest gotowa do druku, wydaj nową wersję (tag `v*`).

### Zasady pisania

- Pisz po polsku, krótkimi zdaniami. Procedury zapisuj jako polecenia w trybie rozkazującym: „Sprawdź…”, „Zapisz…”.
- Jedno polecenie = jeden krok. Nie łącz kilku czynności w jednym kroku.
- Pisz ogólnie: dokument ma działać dla każdej przyszłej misji. Dane konkretnych misji (daty, wyniki, nazwiska) zapisuj tylko w rozdziale „Historia i wnioski” i w wypełnionych formularzach.
- Podawaj jednostki przez `\SI{5}{m/s}`, `\SI{-60}{\degreeCelsius}`.
- Każde twierdzenie z zewnętrznego źródła opatrz cytowaniem `\cite{klucz}`.
- Adresy WWW w tekście i tabelach wstawiaj makrem `\www{domena/ścieżka}` (bez `https://`): adres jest klikalny i nie łamie się. W literaturze używaj `\url{…}` na osobnej linii (`\newline`).
- Dokument jest **publiczny**. Nie wpisuj danych osobowych (prywatnych telefonów, adresów) ani treści z wewnętrznej dokumentacji koła. Na zdjęciach zamazuj numery telefonów i dane osób postronnych. Wypełnionych formularzy nie dodawaj do repozytorium.
- Źródłami mogą być materiały publiczne (artykuły, wpisy na blogach, media, strony instytucji) oraz archiwalne dokumenty projektu opublikowane za zgodą autorów w katalogu `papers/`. Przed dodaniem dokumentu usuń z niego dane osobowe (np. strony z oświadczeniami, numery albumów, daty urodzenia, numery telefonów).

### Gdzie co zmienić

| Chcę… | Plik |
|---|---|
| zmienić treść rozdziału | `tex/rozdzialy/NN_nazwa.tex` |
| dodać rozdział | nowy plik w `tex/rozdzialy/` + `\input{rozdzialy/…}` w `tex/main.tex` |
| zmienić formularz | `tex/rozdzialy/A_formularze.tex` |
| dodać pozycję literatury | `tex/rozdzialy/literatura.tex` (`\bibitem{klucz}`) |
| dopisać misję lub wniosek | `tex/rozdzialy/02_historia.tex` (tabele misji i wniosków) |
| zmienić rysunek schematu | `tex/figures/diagrams.tex` (TikZ) |
| zmienić wykres z danych | `.scripts/plots.py` i pliki w `data/` |
| zmienić wygląd (marginesy, kolory, nagłówki) | `tex/stardust.sty` |

### Sekcje

Każdą sekcję umieszczaj w środowisku `sekcja`. Sekcja krótsza niż strona nie łamie się – w całości przechodzi na następną stronę:

```latex
\begin{sekcja}{Tytuł sekcji}\label{sec:klucz}
Treść sekcji.
\end{sekcja}
```

Sekcji dłuższych niż strona (np. z tabelą `longtable`) nie umieszczaj w środowisku – użyj zwykłego `\section{…}`.

Ramki:

```latex
\begin{uwaga}Zagrożenie dla ludzi, sprzętu albo misji.\end{uwaga}
\begin{wskazowka}Praktyczna rada z poprzednich misji.\end{wskazowka}
```

Odwołania: `rozdział~\ref{ch:planowanie}`, `\rozdz{ch:naziemny}` (numer i nazwa).

### Zdjęcia

1. Dodaj oryginał do `assets/RRRR/opisowa_nazwa.jpg` (rok misji). Zdjęcie bez osób postronnych; kadruj, gdy trzeba.
2. Uruchom `python3 .scripts/photos.py`. Skrypt zapisze zmniejszoną kopię jako `tex/figures/photos/RRRR_opisowa_nazwa.jpg`.
3. Wstaw zdjęcie (bez rozszerzenia):

```latex
\foto[0.8\linewidth]{RRRR_opisowa_nazwa}{Podpis: co widać i kiedy (data misji).}
\dwafoto{plik1}{Podpis 1.}{plik2}{Podpis 2.}
```

Nie używaj środowiska `figure` (obiekty pływające psują bloki niełamane).

### Tabele

Używaj `tabularx` o szerokości `\linewidth`. Tabela nie może przechodzić na kolejną stronę z nagłówkiem oddzielonym od treści: krótkie tabele umieszczaj w środowisku `sekcja`, a długie listy (np. wykaz materiałów) dziel tak, aby każda tabela z tytułem mieściła się na jednej stronie. Typy kolumn: `L` – tekst do lewej, rozciągany; `Y` – tekst wyśrodkowany, rozciągany; `P{30mm}` – stała szerokość; `C{8mm}` – stała szerokość, wyśrodkowany. Wiersze z pliku generowanego wstawiaj makrem `\wiersze{plik.tex}`. Szerokie tabele umieszczaj w środowisku `landscape`.

### Formularze

Każdy formularz zaczyna się na nowej stronie i **musi zmieścić się na jednej stronie**:

```latex
\formularz[kierownik startu]{F15}{Tytuł formularza}{kiedy, np. T$-$1 dzień}
\begin{procedura}
\etap{Nazwa etapu}
\krok{Wejdź na aprs.fi i sprawdź pozycję znaku.}{\pole[2cm]{godz.:}}
\krok{Polecenie bez pola na wartość.}{}
\end{procedura}
\komentarze[3]
\podpisy
```

Argument w nawiasie kwadratowym to rola, która prowadzi formularz. Pola tabel w formularzach twórz makrem `\etykieta{Opis pola}` (mała etykieta, pod nią miejsce na wpis); wysokość pola podaj opcjonalnie: `\etykieta[20mm]{…}`. Szerokie formularze (np. dzienniki) umieszczaj w środowisku `landscape`.

Po dodaniu formularza dopisz go do tabeli na początku dodatku A. Po kompilacji sprawdź w spisie treści, że kolejny formularz zaczyna się na następnej stronie.

### Po misji

1. Przenieś notatki terenowe i komentarze z formularzy do odpowiednich rozdziałów.
2. Dopisz misję i wnioski do rozdziału „Historia i wnioski”.
3. Dodaj zdjęcia i dane z lotu (`assets/`, `data/`).
4. Wydaj nową wersję dokumentu (tag `v*`) i dołącz ją do wydania kodu lotnego.
