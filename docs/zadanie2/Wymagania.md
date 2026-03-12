# Wymagania

## 1. Wymagania funkcjonalne (testowalne)

| Nr | Wymaganie | Priorytet | Testowalność |
|----|-----------|-----------|--------------|
| FR1 | Gracz może wybrać gotowy scenariusz i rozpocząć grę | Must | Po wybraniu scenariusza gra rozpoczyna się i wczytuje mapę |
| FR2 | Gracz może utworzyć nowy scenariusz z mapą, jednostkami | Must | Po zapisaniu scenariusz pojawia się w liście dostępnych scenariuszy i można w niego zagrać |
| FR3 | Gracz może edytować zapisany scenariusz | Should | Po zmianie parametrów i zapisaniu, zmodyfikowany scenariusz wczytuje się zgodnie z nowymi ustawieniami |
| FR4 | System generuje losowe wydarzenia w grze | Must | Uruchamiając kilka rozgrywek w tym samym scenariuszu, losowe wydarzenia różnią się między grami |
| FR5 | Gracz może zapisać i wczytać stan gry | Must | Zapisanie gry i późniejsze wczytanie odtwarza dokładnie ten sam stan rozgrywki |
| FR6 | Menu główne umożliwia wybór gry, edytora scenariuszy, ustawień i wyjścia | Must | Wszystkie przyciski w menu działają i przechodzą do odpowiednich funkcji |

---

## 2. Wymagania systemowe (testowalne)

| Nr | Wymaganie | Priorytet | Testowalność |
|----|-----------|-----------|--------------|
| SR1 | Gra działa na Windows, macOS i Linux | Should | Uruchomienie gry na każdej platformie bez błędów krytycznych |
| SR2 | Gra działa płynnie na komputerach średniej klasy | Must | Średnia liczba FPS ≥ 30 podczas rozgrywki |
| SR3 | Gra korzysta z określonego silnika lub bibliotek | Must | Projekt kompiluje się i uruchamia z użyciem deklarowanego silnika/biblioteki |
| SR4 | Zapis danych do pliku lokalnego | Must | Po zapisaniu scenariusza lub gry plik istnieje i można go wczytać |
| SR5 | Nowe scenariusze można dodawać bez modyfikacji kodu | Must | Dodanie pliku scenariusza powoduje jego pojawienie się w menu gry |

---

## 3. Wymagania niefunkcjonalne (testowalne)

| Nr | Wymaganie | Priorytet | Testowalność |
|----|-----------|-----------|--------------|
| NFR1 | Intuicyjny interfejs | Must | Nowy użytkownik wykonuje podstawowe akcje w <5 minut bez pomocy |
| NFR2 | Brak awarii podczas gry i edycji scenariuszy | Must | Gra działa ≥2 godziny bez krytycznych błędów |
| NFR3 | Czytelna grafika 2D | Should | Wszystkie elementy mapy i jednostki są rozróżnialne w rozdzielczości 1080p |
| NFR4 | Możliwość rozbudowy gry | Could | Dodanie nowej jednostki lub mapy działa bez zmiany kodu |
| NFR5 | Czas ładowania scenariusza <5 sekund | Must | Od wybrania scenariusza do rozpoczęcia gry ≤5 sekund |
| NFR6 | Pliki zapisów i scenariuszy odporne na uszkodzenia | Should | Próba odczytu pliku po zapisaniu nie generuje błędów i dane są kompletne |