
# Scenariusza przypadków użycia:

Wszystkie poniższe przypadki użycia wykorzystują "Gracza" jako aktora.

## Otworzenie istniejącego scenariusza 

- **Warunki wstępne:** Gra w stanie początkowym (menu główne) 
- **Scenariusz (główny przepływ):**
    1. Gracz wybiera opcję "Gotowe scenariusze"
    2. System wyświetla listę istniejących scenariuszy
    3. Gracz wybiera pożądany scenariusz z listy. Wybiera opcję "Załaduj scenariusz"
    4. System weryfikuje poprawność pliku zawierającego wybrany scenariusz. 
    5. System ładuje wybrany scenariusz. 
- **Wyjątki/ alternatywne scenariusze:**
    4B. Walidacja scenariusza zawiodła, system informuje gracza. Kończy przypadek użycia.
- **Warunki końcowe:** Gracz może rozpocząć rozgrywkę

## Stworzenie nowego scenariusza 

- **Warunki wstępne:** Gra w stanie początkowym (menu główne) 
- **Scenariusz (główny przepływ):**
    1. Gracz wybiera opcję "Nowy scenariusz"
    2. System ładuje edytor (z pustym scenariuszem). Wyświetla stan mapy (heksagony bez podziału na prowincje) 
    3. Gracz wyznacza prowincje, poprzez zaznaczanie spójnych fragmentów jako poszczególne prowincje.
    4. System uaktualnia widok mapy.
    Kroki 3-4 wykonują się w pętli do momentu gdy użytkownik wyznaczy wszystkie pożądane prowincje.
    5. Gracz sygnalizuje zakończenie tworzenia mapy
    6. System weryfikuje poprawność utworzonej mapy
    7. Gracz wybiera liczbę przeciwników w scenariuszu 
    8. Gracz przyporządkowuje prowincje do stron (przyporządkowanie opisujące stan na początku gry)
    9. Gracz wybiera liczbę i rodzaj jednostek istniejących w poszczególnych prowincjach na początku gry
    10. Gracz sygnalizuje, że scenariusz jest gotowy.
    11. System weryfikuje poprawność (tj. czy każda strona konfliktu ma co najmniej jedną przyporządkowaną prowincję). System zapisuje nowo utworzony scenariusz do pliku. Powrót do menu głównego.
- **Wyjątki/ alternatywne scenariusze:**
    6B. Walidacja mapy zawiodła z powodu braku możliwych ścieżek pomiędzy wszystkimi prowincjami. System wyświetla informację o powodzie, powrót do etapu 3 (z zachowaniem dotychczas wybranych prowincji).
    11B. Zapis scenariusza nie powiódł się. System wyświetla informację o powodzie. Gracz potwierdza zapoznanie się z powodem. Przypadek kończy się (Powrót do menu głównego).
- **Warunki końcowe:** Nowy scenariusz został utworzony.


## Edycja istniejącego scenariusza 

- **Warunki wstępne:** Gra w stanie początkowym (menu główne) 
- **Scenariusz (główny przepływ):**
    1. Gracz wybiera opcję "Gotowe scenariusze"
    2. System wyświetla listę istniejących scenariuszy
    3. Gracz wybiera pożądany scenariusz z listy. Wybiera opcję "Edycja scenariusza"
    4. System ładuje edytor scenariusza (z wybranym scenariuszem).
    5. Gracz modyfikuję liczbę graczy, początkowe przyporządkowanie prowincji do graczy lub początkowe przyporządkowanie jednostek do prowincji.
    6. System weryfikuje poprawność scenariusza. 
    7. System zapisuje zmodyfikowany scenariusz.
    8. System wraca do menu głównego.     
- **Wyjątki/ alternatywne scenariusze:**
    6B. Walidacja scenariusza zawiodła, system przekazuje informacja o powodzie. Powrót do kroku 5.
    7B. Zapis scenariusza nie powiódł się. System wyświetla informację o powodzie. Gracz potwierdza zapoznanie się z powodem. Przypadek kończy się (Powrót do menu głównego).
- **Warunki końcowe:** dany scenariusz został zmodyfikowany. 

## Zapisanie gry 

- **Warunki wstępne:** Gra w trakcie rozgrywki. Aktualna tura należy do gracza.
- **Scenariusz (główny przepływ):**
    1. Gracz wybiera opcję "Zapisz grę"
    2. System prosi o podanie nazwy pliku docelowo zawierającego zapisany stan rozgrywki.
    3. Gracz podaje nazwę żądaną nazwę.
    4. System dokonuje zapisu aktualnego stanu gry do wskazanego pliku.
- **Wyjątki/ alternatywne scenariusze:**
- **Warunki końcowe:** Plik z stanem rozgrywki został utworzony/nadpisany.

## Wczytanie gry 

- **Warunki wstępne:** Gra w stanie początkowym (menu główne) 
- **Scenariusz (główny przepływ):**
    1. Gracz wybiera opcję "Wczytaj grę"
    2. System wyświetla listę dostępnych zapisanych rozgrywek. Oprócz nazwy wyświetlana jest ilość stron (tj. graczy), obecna tura, data zapisania gry.
    3. Gracz wybiera pozycję z listy z żądaną grą. 
    4. System ładuje wybraną pozycję. Wyświetla stan aktualny stan rozgrywki. 
- **Wyjątki/ alternatywne scenariusze:**
- **Warunki końcowe:** Gra została wczytana. Gracz może kontynuować rozgrywkę.


## Atak 

- **Warunki wstępne:** Rozgrywka w trakcie. Aktualna tura należy do gracza A, w fazie ataku. 
Istnieją dwie, połączone prowincje należące do różnych właścicieli. 
- **Scenariusz (główny przepływ):**
    1 . Gracz wybiera własną prowincję zawierającą jednostki.
    2. System zaznacza wybraną prowincję.
    3. Gracz wybiera osiągalną prowincję należące do innego gracza.
    4. System oblicza i wyświetla rezultat bitwy. W przypadku sukcesu atakowana prowincja zmienia właściciela. Jednostki poprzednio istniejące w prowincji zostają usunięte (zabite). Atakująca armia zostaje przesunięta do nowej prowincji. Wyświetlana mapa zostaje zaktualizowana.
- **Wyjątki/ alternatywne scenariusze:**
    4B. W przypadku porażki atakującej armii zostaje ona zredukowana. Prowincje nie zmieniają właścicieli. Przypadek kończy się.
- **Warunki końcowe:** Gracz przeprowadził atak.

## Ruch 

- **Warunki wstępne:** Rozgrywka w trakcie. Aktualna tura należy do gracza A, w fazie ruchu. 
Istnieją dwie prowincje należące do gracza A, gdzie co najmniej jedna z nich zawiera jednostki.
- **Scenariusz (główny przepływ):**
    1. Gracz wybiera własną prowincję zawierającą jednostki.
    2. System zaznacza wybraną prowincję źródłową.
    3. Gracz wybiera osiągalną prowincję należącą do niego.
    4. System zaznacza wybraną prowincję docelową.
    5. Gracz wybiera armię do przeniesienia. 
    6. Gracz wybiera lokację docelową spośród lokacji należących do prowincji docelowej. 
    7. System:
        Jeżeli lokacja docelowa jest zajęta przez jednostki, które nie wykonały ruchu w obecnej turze, wybrane odziały z prowincji docelowej/początkowej zamieniają się miejscami.
    8. System uaktualnia widok mapy. 
- **Wyjątki/ alternatywne scenariusze:**    
    7B. System: Jeżeli lokacja docelowa jest pusta, wybrana armia zostaje przeniesiona. Przejście do kroku 8.
- **Warunki końcowe:** Jednostki zamieniły się miejscami/zostały przeniesione.

## Tura gracza 

- **Warunki wstępne:** Rozgrywka w trakcie. Początek nowej tury dla danego gracza.
- **Scenariusz (główny przepływ):**
    1. System: Przejście do fazy ataku.
    2. Gracz może wykonać wielokrotnie wykonać akcję "Atak" (o ile możliwa) lub zapisać grę (scenariusz zapisanie gry). 
    3. System przechodzi do fazy ruchu.
    4. Gracz może wykonać wielokrotnie wykonać akcję "Ruch" (o ile możliwa) lub zapisać grę (scenariusz zapisanie gry). 
    5. System przechodzi do kolejnej tury (dla innego gracza).
 **Wyjątki/ alternatywne scenariusze:**    
    2B, 4B - Gracz wybiera opcję "Zakończ grę". System kończy obecną rozgrywkę i przechodzi do menu głównego. Koniec przypadku.
- **Warunki końcowe:** Koniec tury obecnego gracza
