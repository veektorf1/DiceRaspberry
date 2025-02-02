POL
# 🎲 System wbudowany do gry w kości wspomagany sztuczną inteligencją
## 1. Opis projektu
Projekt grupowy, którego celem było stworzenie urządzenia do klasycznej wersji gry w kości z wykorzystaniem systemu wbudowanego, tak aby zminimalizować interakcję użytkownika podczas losowania kości oraz zapewnienie precyzyjnego i sprawiedliwego wykrywania wyników, dlatego nasze urządzenie samo wykonuje faktyczną czynność rzutu kośćmi, sczytanie liczby oczek przy pomocy algorytmu YOLO i ich przesłanie do aplikacji webowej opartej na Flasku, w której gracze prowadzą rozgrywkę. 

Zasady gry są oparte na klascznej [GRZE W KOŚCI](https://en.wikipedia.org/wiki/Yahtzee). W zaimplementowanej wersji gra trwa przez 13 kolejek, w których każdy z graczy może wykonać do 3 rzutów kośćmi. Na początku rzuca się pięcioma kośćmi i po każdym rzucie gracz ma prawo wybrać jakie kości z wyrzuconymi wartościami chce zostawić, a którymi zamierza dalej rzucać. Użytkownik w każdej kolejce wybiera do jakiej kategorii chce wpisać swój wynik (np. mały strit, generał, itd…). Jeśli jego kości układają się w kombinację premiowaną przez wybraną kategorię to dostaje odpowiednią liczbę punktów, w przeciwnym razie dostaje zero. Wynik końcowy to suma punktów ze wszystkich kategorii. Wygrywa gracz, którego wynik końcowy jest najwyższy.


## 2. Wykorzystany sprzęt i technologie:
🖥️ **Sprzęt** 
* Raspberry Pi,
* Pi camera v1.3,
* Przycisk,
* Diody LED,
* Silnik 9V DC,
* elementy mechaniczne i montażowe

🛠️ **Technologie**
* Python
  * Flask - obsługa serwera webowego
  * Picam2 - biblioteka umożliwiająca szczytanie obrazu z modułu kamery 
  * YOLO & Ultralytics - model detekcji obiektów użyty do rozpoznawania wartości na kostkach do gry
* Roboflow - platforma wykorzystana do anotacji i przygotowania zbioru danych do trenowania modelu YOLO
* Google Colab - Usługa chmurowa od Google, dostarczyła zasaoby sprzętowe w chmurze, m.in. karta graficzna Tesla T4, która przyspieszyła proces uczenia się modelu YOLO
* HTML, CSS, JavaScirpt

3. Autorzy
* [Wiktor Makowski](https://github.com/veektorf1)
* [Filip Baranowski](https://github.com/Fizz874)
* [Artur Strzelecki](https://github.com/0Artur1)
 



