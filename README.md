# memorsy

Głowne założenia komunkacji:
Wszystkie komunikaty są kończone znakiem końca linii – '\r\n'.
Tablice są formatowane za pomocą biblioteki pickle.
Obie strony komunikują sie za pomocą kodów : mapowane z pliku 'codes.py', 
# poza wyjątkiem gdy klient chce opuścić rozgrywkę, nie wysyła kodu dla "OuitGame" tylko komunikat tekstowy
# 'QuitGame'. spowodoawne jest to tym,że zapytanie o kartę jest 


1.	Sposób obsługi klientów przez serwer:
a.	Każdy klient jest obsługiwany w niezależnym wątku.
b.	Dla każdego klienta generowana jest mapa zależna od poziomu, klient generuje pustą mapę.
c.	Mapa przechowywana jest tylko po stronie serwera, klient wysyła zapytania o zawartość kart.
d.	Klient wysyła tablice z pozycjami kart, z zapytaniem czy do siebie pasują.
e.	Gdy skończą się karty tj. klient odgadnie wszystkie możliwe pary, serwer wysyła komunikat informujący o wygranej.
f.	Po skończeniu gry, klient ma możliwość zaczęcia kolejnej rozgrywki.


Przepływ danych w aplikacji, (po połączeniu się z serwerem)
1.	Klient wysyła zapytanie o level
2.	Server odpowiada czy przygotował grę
3.	Klient wysyła zapytanie o kartę
4.	Server odpowiada tekstem.
5.	Klient wysyła parę kart [id, id]
6.	Server odpowiada czy karty do siebie pasują.
7.	Gdy wszystkie karty zostały odkryte – server wysyła komunikat „GameOver”
8.	Klient kończy rozgrywkę, lub rozpoczyna nową ( wysyła- „QuitGame” /„NewGame”).
9.	NewGame -> pkt 2 / QuitGame -> zamknięcie połączenia z klientem


1.1	Rozłączanie klienta
 Użytkownik w każdym momencie może zakończyć sesje, wysyła wtedy:
„QuitGame”
Server nie ospowiada żadnym potwierdzeniem, kończy sesje klienta.

2. Formaty pakietów
•	Wybrany level jest przesyłany bitowo
•	Wybrane karty wysyłane są jako tablica – np.  [1, 2]. Sformatowana na strumień bitowy za pomocą biblioteki pickle.
•	Server po otrzymaniu 
