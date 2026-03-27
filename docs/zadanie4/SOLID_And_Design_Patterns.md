<h1> Zastosowanie zasady SOLID w naszym projekcie: </h1>  

S - Zasada pojedynczej odpowiedzialności (SRP) - zakłada, że każda klasa powinna mieć tylko jeden powód do zmiany, odpowiadając jednocześnie za konkretny aspekt funkcji systemu; <p>
Postaraliśmy się aby klasy w diagramie klas, więc także przyszły kod były jak najbardziej atomowe, aby móc rozwijać tylko jedną klasę, w celu dodania nowej funkcji, a nie żeby była sytuacja że zmiana podstawowej jednostki wymaga interwencji w głównym segmencie gry. 
Oczywiście może wystąpić problem, który będzie wymagał interwencji w kilki miejscach jednocześnie ale postaramy sie aby taka sytuacja nie wystąpiła 

O - Zasada otwarte-zamknięte (OCP) - zaleca projektowanie modułów w sposób umożliwiający ich rozszerzanie bez konieczności modyfikacji;<p>
Dodawanie nowych jednostek, typów terenu oraz budynków postaramy się aby było możliwe bez znacznego integrowania w kod.

L - Zasada podstawienia Liskov (LSP) - podkreśla znaczenie zastępowalności obiektów klasy bazowej przez obiekty klasy pochodnej bez wpływu na poprawne działanie programu;<p>
Planujemy stworzyć klasy które są odzielone od siebie, jednocześnie sprawiając że kod będzie działał ogólnie dla klasy i dodawanie nowych typów np. jednostek nie spowoduje problemów, gdyż program będzie przystosowany do akceptacji segmentów które są stworzone w ogólności 

I - Zasada segregacji interfejsów (ISP) - sugeruje tworzenie wyspecjalizowanych interfejsów zamiast jednego rozbudowanego i ogólnego;<p>
Planujemy rozdzielić interface na kilka, odpowiedzialnych za główną grę, między innymi: 
interface od włączania gry
interface od scenariuszy 
interface od wczytywania i zapisywania gry

D - Zasada odwrócenia zależności (DIP) - promuje zależność od abstrakcji zamiast od szczegółowych implementacji. Oddziela tym samym wysokopoziomowe moduły od szczegółowych elementów niskiego poziomu.<p>
Jak widać na (prawie) drzewku będącym diagramie klas, staraliśmy się rozbić moduły jak najbardziej aby można bylo zajmować się kodem segmentami, i całość nie powinno ingerować na siebie w znaczącym stopniu, więc można w danym momencie zając się wybranym sektorem i to w znaczącym stopniu nie powinno wpłynąć na problemy w innej odzielnej od tego sekcji kodu.


<h1>Wzorce projektowe w naszym projekcie: </h1>

<h3>Kompozycja(Composite):</h3>

Wzorzec ten określa pattern który ma strukturę drzewa, a każdy obiekt jest dalej niezależnym obiektem nad który można pracować osobno, mimo że jest zależny i połaczony z innymi. 
U nas, np. Mapa składa się z Prowincji, Prowincje zwierają Armię, Armia składa się z 2 Odziałów, a Odział to grupa jednostek danego typu.
Pasuje więc idealnie to do naszej koncepcji, gdyż mamy strukturę drzewa podsegmentów gry zwłaszcza, że nawet w materiałach istnieje przykład związany z wojskowością. <p>
<img width="420" height="345" alt="image" src="https://github.com/user-attachments/assets/14c78734-9c4a-4288-a276-5e73e68a9ede"/>

<h3>Memento/Migawka(Memento/Snapshot)</h3>  

Memento to wzorzec który pokazuje nam jak zapisywać poprzednie stany aplikacji. Z uwagi na to, że chcemy zaimplementować system zapisywania gry, potrzebujemy jakiegoś sposobu na zapisywanie informacji o stanie gry w czasie zapisu. Dzięki niemu możemy stworzyć właśnie snapshota stanu gry w danym momencie, aby gracz mógł do niego wrócić w późniejszym czasie, bądź wykorzystamy ten system do tworzenia customowych scenariuszy. Jest on też polecany jak program potrzebuje sposobu na powrót do swojego wcześniejszego stanu więc wszystko się łaczy w całość, zwłaszcza że w gamedevie reusing zdawałoby się niepowiązanych schematów i rozwiązań jest często na porządku dziennym.

