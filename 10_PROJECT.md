# Prowadzenie projektu i dokumentacja

Ten rozdział opisuje, jak prowadzić projekt misji i dokumentację eksperymentu. Praktyki pochodzą z programu REXUS/BEXUS (ESA, DLR, SNSA), w którym zespół Stardust uczestniczył. Program prowadzi zespoły studenckie przez pełny cykl misji kosmicznej. Uproszczona wersja tych praktyk działa dobrze w misjach własnych.

## Cykl projektu

Podziel projekt na etapy. Na końcu każdego etapu zrób przegląd: zespół przedstawia stan projektu osobom spoza zespołu (np. absolwentom projektu, opiekunowi koła). Przegląd kończy się listą działań.

| Etap | Pytanie przeglądu | Wynik |
|-----------------------|-------------------------------------------------|------------------------------------------------|
| Koncepcja | Co chcemy zbadać i dlaczego? Czy to jest możliwe? | Cel misji, wymagania, wstępny budżet masy. |
| Projekt wstępny (PDR) | Czy koncepcja spełnia wymagania? | Schemat systemu, wybór komponentów, plan testów. |
| Projekt krytyczny (CDR) | Czy projekt jest gotowy do budowy? | Kompletny projekt, budżety, rejestr ryzyk. |
| Integracja i testy | Czy zbudowany sprzęt działa? | Wyniki testów, poprawki. |
| Gotowość do lotu (FRR) | Czy możemy bezpiecznie polecieć? | Decyzja „leci / nie leci”, listy kontrolne. |
| Po misji | Co działało? Co poprawić? | Raport z misji, wnioski. |

Dla prostej misji szkoleniowej wystarczą dwa przeglądy: przed budową (CDR) i przed lotem (FRR).

## Dokumentacja eksperymentu

Każdy ładunek i każda zmiana platformy ma dokument eksperymentu. Wzór: dokument SED (Student Experiment Documentation) z programu REXUS/BEXUS. Przykład dokumentu SED zespołu Stardust: <https://rexusbexus.net/wp-content/uploads/2023/01/BX30_STARDUST_SED_v5-0s_26Apr2022_highlighted.pdf>.

Minimalna struktura dokumentu eksperymentu:

1. **Wprowadzenie** – cel naukowy lub techniczny, zespół i role.
2. **Wymagania** – co eksperyment musi robić (funkcjonalne), jakie ma ograniczenia (masa, wymiary, zasilanie, temperatura).
3. **Projekt** – schemat mechaniczny, elektryczny i program (np. maszyna stanów).
4. **Budżety** – masa, energia, dane.
5. **Rejestr ryzyk** – co może się nie udać, prawdopodobieństwo, skutek, środek zaradczy.
6. **Plan testów i wyniki** – co, jak i kiedy testujemy, wynik każdego testu.
7. **Procedury** – montaż, przygotowanie na stanowisku, listy kontrolne.
8. **Wyniki i wnioski** – po misji.

Zasady:

- Pisz dokument od początku projektu, nie po misji.
- Każde wymaganie ma test, który je weryfikuje.
- Numeruj wersje dokumentu. Zapisz, co się zmieniło.
- Trzymaj dokumentację w repozytorium (Markdown), razem z kodem i projektami PCB.

## Budżety

**Budżet masy:** tabela wszystkich elementów z masą zmierzoną (nie oszacowaną). Zapas: co najmniej 10%.

**Budżet energii:** dla każdego urządzenia: napięcie, prąd w pracy, prąd szczytowy, czas pracy. Suma energii × zapas ≤ pojemność baterii w niskiej temperaturze.

**Budżet danych:** ilość danych na sekundę × czas lotu ≤ pojemność pamięci. Pojemność łącza radiowego ≥ dane telemetrii.

## Rejestr ryzyk

Przykładowe ryzyka dla platformy:

| Ryzyko | Skutek | Środek zaradczy |
|-------------------|-----------------------------|---------------------------------------------------------|
| Odcinacz nie działa | Długi lot, lądowanie daleko | Test w warunkach lotu, zapas linki, automatyczne odcięcie |
| Brak telemetrii | Utrata ładunku | Dwa systemy śledzenia, lokalizator SPOT |
| Za mało gazu | Opóźniony start | Zapas gazu, pomiar siły nośnej |
| Rozładowana bateria | Brak danych, brak lokalizacji | Budżet energii, test w zimnie, nowe baterie |
| Lądowanie w wodzie | Utrata ładunku | Predykcja, kryteria „brak startu” |
| Restart OBC w locie | Utrata stanu misji | Zapis stanu w pamięci nieulotnej |

## Testy

Minimalny zestaw testów przed lotem:

| Test | Cel |
|---------------------------------------------------|------------------------------------------------------------|
| Test funkcjonalny na stole | Wszystkie funkcje działają. |
| Test w zimnie (zamrażarka, około −20 °C, czas lotu) | Elektronika i baterie działają w niskiej temperaturze. |
| Test zasięgu radia | Telemetria odbierana z odległości kilku km. |
| Test odcinacza pod obciążeniem | Odcinacz zwalnia linkę z masą zestawu i ze skręconymi linkami. |
| Test czasu pracy | System działa na bateriach dłużej niż lot plus poszukiwania. |
| Test upadku | Mocowania przetrwają upadek z wysokości około 1 m. |
| Próba generalna | Zespół wykonuje cały montaż i listy kontrolne bez balonu. |

Zapisuj wynik każdego testu (data, osoba, wynik, uwagi).

## Raport z misji

Napisz raport w ciągu tygodnia po misji. Wzór: raport z misji testowej 2020 (<https://yasiu.pl/blog/stardust-stratospheric-balloon-mission/>).

Struktura raportu:

1. Zestaw lotny (elementy, masy, wersje programu).
2. Oś czasu (NOTAM, start, pęknięcie/odcięcie, lądowanie, odzyskanie).
3. Dane z lotu (trasa, profil wysokości, czujniki) – w załączniku pliki z danymi.
4. Problemy (co nie działało i dlaczego).
5. Wnioski (co zmienić w następnej misji).

Dopisz wnioski do rozdziału „Historia i wnioski” w tej dokumentacji.

## Przekazywanie wiedzy

Zespoły studenckie zmieniają się co kilka lat. Wiedza ginie, gdy jest tylko w głowach.

- Każda nowa grupa zaczyna od lotu szkoleniowego z prostym ładunkiem.
- Doświadczona osoba prowadzi pierwszą misję. Następną misję nowy zespół prowadzi samodzielnie.
- Każdy podzespół ma osobę odpowiedzialną i opisaną procedurę.
- Po każdej misji aktualizuj tę dokumentację.
- Publikuj wyniki (konferencje, artykuły, blog). Publikacje zostają po zespole.
