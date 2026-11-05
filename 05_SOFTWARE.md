# Oprogramowanie

Ten rozdział opisuje narzędzia do planowania lotu, predykcji trajektorii i śledzenia balonu.

## Narzędzia

| Narzędzie | Zastosowanie | Adres |
|-------------------------|------------------------------------------|-------------------------------|
| SondeHub Burst Calculator | Ilość gazu, siła nośna, wysokość pęknięcia | <https://sondehub.org/calc/> |
| SondeHub Predictor | Predykcja trajektorii i miejsca lądowania | <https://predict.sondehub.org/> |
| SondeHub Amateur | Mapa śledzenia (APRS, RTTY, LoRa, Horus) | <https://amateur.sondehub.org/> |
| aprs.fi | Mapa śledzenia APRS | <https://aprs.fi/> |
| PureTrack | Mapa śledzenia (bez źródła APRS) | <https://puretrack.io/> |
| SPOT | Lokalizator satelitarny po lądowaniu | <https://www.findmespot.com/> |

## Obliczenie ilości gazu

1. Zważ cały zestaw lotny bez powłoki (rozdział „Segment lotny”, budżet masy).
2. Otwórz kalkulator SondeHub.
3. Wpisz masę ładunku [g]. Wybierz model powłoki.
4. Wpisz docelową prędkość wznoszenia: 5 m/s.
5. Zapisz wyniki:
    - siła nośna szyjki (neck lift) [g] – potrzebna do tankowania,
    - objętość gazu [m³] – potrzebna do zamówienia gazu,
    - wysokość pęknięcia [m] i czas do pęknięcia [min] – potrzebne do predykcji i zgłoszenia.
6. Zamów gaz z zapasem (straty przy tankowaniu, butla z mniejszą ilością gazu).

## Predykcja trajektorii

1. Otwórz predyktor SondeHub.
2. Wpisz: miejsce startu, datę i godzinę, prędkość wznoszenia, wysokość pęknięcia, prędkość opadania.
3. Sprawdź miejsce lądowania.
4. Powtarzaj predykcję codziennie od około 7 dni przed lotem. Prognoza wiatru zmienia się.
5. Gdy miejsce lądowania jest złe, zmień godzinę startu, miejsce startu lub prędkość wznoszenia.

**Nie startuj, gdy predykcja pokazuje lądowanie:**

- w morzu, jeziorze lub na rozległym terenie podmokłym,
- w dużym lesie lub w mieście,
- w strefie kontrolowanej lotniska,
- za granicą państwa.

**Nie startuj, gdy:**

- wiatr przy ziemi jest silny,
- pada deszcz, jest burza lub niska podstawa chmur.

## Konfiguracja śledzenia

Przed misją:

1. Ustaw w trackerze znak wywoławczy (callsign) i SSID APRS (rozdział „Elektronika”). Dla balonów stosuje się zwyczajowo SSID -11.
2. Skonfiguruj ładunek (payload) w SondeHub Amateur, jeśli używasz RTTY/LoRa/Horus. Bez konfiguracji SondeHub nie zdekoduje telemetrii.
3. Aktywuj subskrypcję lokalizatora SPOT (plan Flex – na jeden miesiąc).
4. Sprawdź, czy tracker pojawia się w SondeHub i aprs.fi (test na ziemi).
5. Udostępnij link do śledzenia całemu zespołowi.

## Śledzenie w trakcie lotu

- Jedna osoba (operator śledzenia) obserwuje mapę i podaje pozycję kierowcy.
- Po starcie jedź w kierunku przewidywanego miejsca lądowania.
- Aktualizuj predykcję w trakcie lotu na podstawie aktualnej pozycji.
- Gdy balon pęknie, przyspiesz. Opadanie trwa krócej niż wznoszenie.
- Przy ziemi sygnał z trackera zanika (zasłaniają go drzewa i budynki). Zapisz ostatnią pozycję.
- Po lądowaniu użyj lokalizatora SPOT i odbiornika mobilnego blisko ostatniej pozycji.
