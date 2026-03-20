```mermaid
graph LR;
    subgraph Gra;
      U01([ Otworzenie scenariusza]);
      U02([ Tworzenie nowego scenariusza]);
      U03([ Edytowanie scenariusza]);
      U04([ Zapisanie gry]);
      U05([ Wczytanie gry]);
      U06([ Pomyślny atak]);
      U07([ Nieudany atak]);
      U08([ Ruch]);
    end;

Gracz[ Gracz];

Gracz --- U01;
Gracz --- U02;
Gracz --- U03;
Gracz --- U04;
Gracz --- U05;
Gracz --- U06;
Gracz --- U07;
Gracz --- U08;
```
