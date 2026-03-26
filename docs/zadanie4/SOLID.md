Zastsowanie zasady SOLID w naszym projekcie: 

S - Zasada pojedynczej odpowiedzialności (SRP) - zakłada, że każda klasa powinna mieć tylko jeden powód do zmiany, odpowiadając jednocześnie za konkretny aspekt funkcji systemu;
Postaralismy się aby klasy w diagramie klas, więc także przyszły kod były jak najbardziej atomowe, aby móc rozwijać tylko jedną klasę, w celu dodania nowej funkcji, a nie żeby była sytuacja że zmiana podstawowej jednostki wymaga interwencji w głównym segmencie gry. 
Oczywiście może wystąpić problem, kóry będzie wymagał interwencji w kilki miejscach jednocześnie ale postaramy sie aby taka sytuacja nie wystąpiła 

O - Zasada otwarte-zamknięte (OCP) - zaleca projektowanie modułów w sposób umożliwiający ich rozszerzanie bez konieczności modyfikacji;
Dodawanie nowych jednostek, typów terenu oraz budynków postaramy się aby było możliwe bez znacznego integrowania w kod.

L - Zasada podstawienia Liskov (LSP) - podkreśla znaczenie zastępowalności obiektów klasy bazowej przez obiekty klasy pochodnej bez wpływu na poprawne działanie programu;
Planujemy stworzyć klasy które są odzielone od siebie, jednocześnie sprawiając że kod będzie działał ogólnie dla klasy, i dodawanie nowych typów np. jednostek nie spowoduje problemów, gdyż program będzie przystosowany do akceptacji segmentów które są stworzone w ogólności 

I - Zasada segregacji interfejsów (ISP) - sugeruje tworzenie wyspecjalizowanych interfejsów zamiast jednego rozbudowanego i ogólnego;
Planujemy rozdzielić interface na kilka, odpowiedzialnych za główną grę, między innymi: 
interface od włączania gry
interface od scenariuszy 
interface od wczytywania i zapisywania gry

D - Zasada odwrócenia zależności (DIP) - promuje zależność od abstrakcji zamiast od szczegółowych implementacji. Oddziela tym samym wysokopoziomowe moduły od szczegółowych elementów niskiego poziomu.
Jak widać na (prawie) drzewku będącym diagramie klas, staralismy się rozbić moduły jak najbaardziej aby można bylo zajmować się kodem segmentami, i całość nie powinno ingerować na siebie w znaczącym stopniu, więc można w danym momencie zając się wybranym sektorem i to w znaczącym stopniu nie powinno wpłynąć na problemy w innej odzielonej od tego sekcji kodu.
