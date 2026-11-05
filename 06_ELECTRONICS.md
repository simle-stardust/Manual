# Elektronika

Elektronika platformy jest w gondoli platformy. Zawiera:

- tracker (GPS + nadajnik telemetrii),
- komputer pokładowy (OBC) – steruje odcinaczem i zapisuje dane,
- lokalizator po lądowaniu,
- baterie.

## Tracker

Tracker podaje pozycję balonu przez radio. Bez trackera nie odzyskasz ładunku.

### HABduino

HABduino to nakładka na Arduino do trackerów balonowych. Nadaje telemetrię RTTY (moduł Radiometrix NTX2B, 434 MHz) i APRS.

- Sprzęt i dokumentacja: <https://github.com/HABduino/HABduino> (projekt nie jest już rozwijany).
- Zalecane oprogramowanie: FlexTrack <https://github.com/daveake/FlexTrack> (obsługuje HABduino v4, RTTY i APRS, zawiera obsługę odcinacza).
- Opis budowy trackera: <https://www.daveakerman.com/?p=1732>.

### Konfiguracja przed misją

1. Ustaw znak wywoławczy krótkofalowca (callsign).
2. Ustaw SSID APRS (zwyczajowo -11 dla balonów).
3. Ustaw identyfikator ładunku RTTY (payload ID), taki sam jak w SondeHub.
4. Wgraj program. Zapisz wersję programu w raporcie z misji.
5. Sprawdź na ziemi: pozycja GPS, odbiór APRS (aprs.fi), odbiór RTTY (SondeHub).

### Zasady

- Moduł GPS musi działać powyżej 18 km (tryb „airborne”). Typowe moduły u-blox działają do około 50 km w tym trybie.
- Nie startuj bez pozycji GPS (GPS lock) i bez odbioru telemetrii na ziemi.
- Włóż nowe baterie przed każdym lotem. Używaj baterii litowych (działają w niskiej temperaturze).
- Sprawdź czas pracy na bateriach. Zapas: co najmniej dwa razy dłuższy niż planowany lot plus czas poszukiwań.
- Sprawdź antenę po montażu (zła antena wyłączyła APRS w misji z 2020 roku).

## Komputer pokładowy (OBC)

Komputer pokładowy:

- steruje odcinaczem (komenda z ziemi albo warunek automatyczny),
- zapisuje dane z czujników na karcie SD z czasem,
- przekazuje stan systemu do telemetrii.

Wymagania:

- Wysokość bierz z GPS. Wzór na wysokość z ciśnienia jest niedokładny powyżej około 10 km.
- Zapisuj stan misji (np. „przed startem”, „wznoszenie”, „opadanie”) w pamięci nieulotnej. Restart w locie nie może zerować misji.
- Odrzucaj błędne odczyty czujników (kody błędów, wartości poza zakresem).
- Dodaj diody statusu: zasilanie, GPS, karta SD, stan odcinacza.
- Czujniki ciśnienia muszą mierzyć do około 5 hPa (BME280 mierzy tylko do 300 hPa).

Dokumentacja i kod komputera pokładowego są w repozytoriach organizacji <https://github.com/simle-stardust>.

## Lokalizator po lądowaniu

Lokalizator satelitarny SPOT Trace podaje pozycję przez satelity, także bez zasięgu GSM.

- Działa tylko do około 6500 m. Służy tylko do lokalizacji po lądowaniu.
- Wymaga aktywnej subskrypcji.
- Ustaw interwał raportów (np. 5 minut).
- Antena (górna strona urządzenia) musi być skierowana do nieba.

Zapasowo możesz użyć smartfona z funkcją „Znajdź moje urządzenie” (pomogła odnaleźć ładunek w 2020 roku).

## Zasilanie i temperatura

- Licz budżet energii: pobór każdego urządzenia × czas lotu × zapas.
- Uwzględnij prąd rozruchowy serw i silników.
- W stratosferze powietrze ma do −60 °C, ale gondola nagrzewa się od słońca i od elektroniki. W lecie elektronika w izolowanej gondoli może przekroczyć 50 °C.
- Testuj elektronikę w zamrażarce (około −20 °C) przez czas równy czasowi lotu.

## Licencja radiowa

APRS i RTTY na 434 MHz wymagają pozwolenia radiowego (rozdział „Wymagania prawne”). Operator z licencją krótkofalowca odpowiada za nadajnik.
