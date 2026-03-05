### Macierz ryzyka


 - P - prawdopodobieństwo wystąpienia, oceniane w skali 1 do 5 (1 - mało prawdopodobne, 5 - bardzo prawdopodobne)
 - W - wpływ na projekt, oceniany w skali 1 do 5 (1 - niewielki wpływ, 5 - bardzo poważny wpływ)


| P↓\W→     | **1** | **2** | **3** | **4** | **5** |
| ---       | ----- | ----- | ----- | ----- | ----- |
| **5**     |   .   |   .   |   .   |   .   |   R4  |
| **4**     |   .   |   R5  |   .   |   R2  |   .   |
| **3**     |   .   |   R1  |   R8  |   .   |   R3  |
| **2**     |   .   |   .   |   .   |   R7  |   .   |
| **1**     |   .   |   .   |   .   |   R6  |   .   |

Identyfikator danego ryzyka (umieszczony w macierzy) jest powiązany z jego nazwą zgodnie z listą w ListaRyzyk.md

---

Poziom ryzyka
(zdefiniowany jako ocena prawdopodobieństwa wystąpienia * ocena potencjalnego wpływu na projekt)

- niski (1 - 4): R6 
- średni (5 - 14): R8, R5, R7, R1
- wysoki (15 - 25): R4, R2, R3
