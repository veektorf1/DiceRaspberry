**[EN English Version Below](#english-version)**

🇵🇱 PL
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
 
---

<a id="english-version"></a>
# 🎲 Embedded System for Dice Game Powered by Artificial Intelligence

## 1. Project Description  
This group project aimed to develop a device for the classic dice game using an embedded system to minimize user interaction during dice rolling while ensuring precise and fair result detection. Our device automatically performs the physical dice roll, reads the number of pips using the YOLO algorithm, and sends the results to a Flask-based web application, where players track the game.

The game rules are based on the classic [YAHTZEE](https://en.wikipedia.org/wiki/Yahtzee). In our implementation, the game lasts for 13 rounds, during which each player can roll the dice up to 3 times per round. Initially, five dice are rolled, and after each roll, the player can choose which dice to keep and which to re-roll. In each round, the player selects a category to assign their score (e.g., small straight, Yahtzee, etc.). If the dice match the category’s criteria, the player earns points; otherwise, they receive zero. The final score is the sum of all category scores, and the player with the highest score wins.

## 2. Hardware and Technologies Used  
### 🖥️ Hardware  
- Raspberry Pi  
- Pi Camera v1.3  
- Button  
- LED diodes  
- 9V DC motor  
- Mechanical and mounting components  

### 🛠️ Technologies  
- **Python**  
  - **Flask** – Web server management  
  - **Picam2** – Library for capturing images from the camera module  
  - **YOLO & Ultralytics** – Object detection model used to recognize dice values  
- **Roboflow** – Platform used for annotation and dataset preparation for training the YOLO model  
- **Google Colab** – Cloud service by Google that provided cloud computing resources, including a Tesla T4 GPU, which accelerated the YOLO model training process  
- **HTML, CSS, JavaScript**  

## 3. Authors  
* [Wiktor Makowski](https://github.com/veektorf1)
* [Filip Baranowski](https://github.com/Fizz874)
* [Artur Strzelecki](https://github.com/0Artur1)

