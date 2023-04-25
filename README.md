# Transformacje.py



Program Transformacje.py ma na celu transformacje pomiędzy układami współrzędnych takimi jak:
- XYZ -> BLH
- BLH -> XYZ
- XYZ -> NEU
- BL -> XY w układzie PL2000
- BL -> XY w układzie PL1992



Program został stworzony przy wykorzystaniu oprogramowania Spyder 5.4.3 w sposób umożliwiający zaimportowanie pliku w formacie .txt, owy plik pozwoli na transformację danych w ograniczonych wyłącznie ilością współrzędnych.



W celu implementacji transformacji zalecane jest wykorzystanie systemu operacyjnego Windows 11 oraz oprogramowania python v3.10 wraz z zainstalowanymi bibliotekami takimi jak:
- numpy - biblioteka posłużyła do opracowania danych w postaci macierzowej oraz do otrzymania wyników obliczeń z większą precyzją która jest kluczowa podczas operacji geodezyjnych.
- argparse - biblioteka służąca do przetwarzania argumentów wykorzystywanych podczas implementacji programu w wierszu poleceń, za jej pomocą jesteśmy w stanie przekazać do programu podstawowe informacje mające na celu wydawanie poleceń które zapoczątkują działanie programu.
- math - podstawowa biblioteka wykorzystywana w oprogramowaniu służącym do wykonywania operacji matematycznych na danych w języku python.



Program został napisany oraz sprawdzony na urządzeniu obsługującym system operacyjny Windows 11, za pomocą języka python w wersji 3.10
W związku z brakiem możliwości przeprowadzenia testów oprogramowania na urządzeniach posiadających starszą wersję systemu operacyjnego nie byliśmy w stanie stwierdzić zgodności ze starszymi urządzeniami.

Transformacje.py został zaprogramowany w sposób który powinien być przyjemny dla potencjalnego użytkownika, pozwala on na wykorzystanie pliku z danymi znajdującego się w dowolnym miejscu na dysku za pomocą wykorzystania ścieżki która pozwoli na odnalezienie pliku poprzez wpisanie jej w terminalu podczas aktywacji modułu.

Plik z danymi powinien zostać utworzony na podstawie pliku przykładowego example.txt, aspektami koniecznymi do wykonania operacji na pliku są:
- Pierwszy znak każdej linijki tekstu powinien zaczynać się od danej do transformacji, znak 'space' powoduje błędy w programie, w następstwie tego program nie pozwoli na wykonanie zamierzonych operacji.
- Dane wyjściowe powinny być oddzielone poprzez wykorzystanie wyłącznie jednego znaku 'space' bez wykorzystywania tabulatora.
- Dane przedstawione w postaci ułamka dziesiętnego powinny być zapisane za pomocą kropki, wykorzystanie przecinka spowoduje zatrzymanie działania programu w związku z błędem w kodzie.
- Puste wiersze w pliku tekstowym będą powodowały pojawienie się błędów uniemożliwiających dalsze działanie programu.
- Dane podawane w pliku .txt powinny być zapisane w postaci następujących jednostek:

- XYZ jako dane metryczne zapisane z dowolną dokładnością

- BLH:
	
	B oraz L jako kąty w mierze łukowej z dowolną dokładnością [rho]
	H jako dana w postaci metrycznej [m]	

Przykład utworzonego wiersza danych:
- BLH:

		5.12331 1.41213 24541.165
- BL:

		5.12331 1.41213
- XYZ:

		5416810.156 8184131.642 4616413.1648


Program pozwala na obliczenia z wykorzystaniem trzech różnych elipsoid odniesienia:
- GRS80
- WGS84
- Kraswoskiego

Tak owy zabieg umożliwia użytkownikowi implementacje transformacji na najczęściej wykorzystywanych elipsoidach, dzięki czemu stajemy się przygotowani na większość przypadków.

Aby zainicjować start oprogramowania należy wykorzystać cmd lub WindowsPowerShell w następujący sposób:
-Włączenie cmd
-Wczytanie katalogu w którym znajduje się plik Transformacje.py za pomocą komendy:

	cd filepath
gdzie:

- filepath - ścieżka do katalogu w postaci C:/Users/Dominik/Desktop/Informatyka/Projekt_1 

-Po przejściu do katalogu jesteśmy w stanie wywołać komendę służącą do pomocy w obsłudze oprogramowania:
	python Transformacje.py -h
Wpisanie owej komendy w Windows commands zwróci:

	usage: Transformacje.py [-h] [-filepath FILEPATH] [-m MODEL] [-method METHOD]

	Transformacja współrzędnych

	options:
  	-h, --help            show this help message and exit
  	-filepath FILEPATH, --filepath FILEPATH
                        	Ścieżka do pliku .txt
  	-m MODEL, --model MODEL
                        	Dostępne modele elipsoidy: -GRS80 -WGS84 -Krasowski
  	-method METHOD, --method METHOD
                        	Podaj co chcesz wyznaczyć: -BLH -XYZ -NEU -PL2000 -PL1992

Komenda odpowiadająca za pomoc wskazuje opcje możliwe do wykorzystania:
- -filepath jest zmienną wymaganą do zainicjowania startu pliku, wykorzystuje ona podaną ścieżkę na podstawie której program dokona transfomracji
- -m pozwala na wybór jednej spośród elipsoid odniesienia dostępnych do wykorzystania w programie gdzie GRS80 jest elipsoidą nominalnej (wartości nie trzeba wywoływać w celu obliczeń)
- -method pozwala na wybór transformacji jaką chcemy rozpocząć:
	- XYZ pozwala na wyznaczenie XYZ wykorzystując współrzędne geocentryczne BLH ( jest to wartość podstawowa, zostaje zaimplementowana w przypadku gdy nie uwzględnimy zmiennej -method)
	- BLH rozpoczyna transformację danych z XYZ do BLH
	- NEU przekształca XYZ w macierz obrotu NEU
	- PL2000 transformuje BL w współrzędne płaskie w układzie PL2000
	- PL1992 transformuje BL w współrzędne płaskie w układzie PL1992



Przykłady startu programu Transformacje.py:
 - python Transformacje.py -filepath C:/Users/Dominik/Desktop/Informatyka/Projekt_1 -m GRS80 -method XYZ     
 
 		Rozpoczyna działanie programu przy wyborze pliku C:/Users/Dominik/Desktop/Informatyka/Projekt_1 , elipsoidy GRS80 oraz transformuje współrzędne BLH na XYZ
		
 - python Transformacje.py -filepath C:/Users/Dominik/Desktop/Informatyka/Projekt_1      
 
 		Rozpoczyna działanie programu przy wyborze pliku C:/Users/Dominik/Desktop/Informatyka/Projekt_1 , elipsoidy GRS80{wartość nominalna} oraz transformuje współrzędne BLH na XYZ{wartość nominalna}
 
 - python Transformacje.py -filepath C:/Users/Dominik/Desktop/Informatyka -m Krasowski -method NEU
 
 		Rozpoczyna działanie programu przy wyborze pliku C:/Users/Dominik/Desktop/Informatyka, elipsoida Krasowskiego oraz transformuje współrzędne XYZ na NEU
		
 - python Transformacje.py -filepath C:/Users/Dominik/Desktop/Informatyka/Projekt_1 -WGS84      
 
 		Rozpoczyna działanie programu przy wyborze pliku C:/Users/Dominik/Desktop/Informatyka/Projekt_1 , elipsoidy WGS84 oraz transformuje współrzędne BLH na XYZ{wartość nominalna}

Program jest przygotowany na błędnie wprowadzone komendy podane poprzez użytkownika, wskazuje błąd oraz sposób rozwiązania.
Jednakże podczas próby uruchomienia skryptu po podaniu więcej niż jednej błędnej komendy program zwróci wyłącznie jeden błąd po rozwiązaniu którego program jako output zwróci kolejny.
Błędy jakie program rozwiązuje to następująco:
- Błędnie wprowadzona ścieżka do pliku:

		!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

		Plik C:\Users\Dominik\Desktop\cos\infa\example.tx nie został odnaleziony, sprawdź czy ścieżka została prawidłowo wpisana

		!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		
- Próba implementacji niedostępnej transformacji:

		!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

		x nie jest obsługiwane przez program, proszę o wybór z dostępnej listy atrybutów:
 		-BLH
 		-XYZ
 		-NEU
 		-PL2000
		-PL1992

		!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

- Wybór elipsoidy nie uwzględnionej w programie:

		!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

		Podana wartość nie jest obsługiwana poprzez program, wybierz z dostępnych uwzględniając wielkosć znaków:
		-GRS80
		-WGS84
		-Krasowski

		!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




Rozpoczęcie skryptu zainicjuje implementacje transformacje pliku z danymi oraz jako output utworzy plik tekstowy w katalogu w którym znajduje się plik Transformacje.py:

- dla metody BLH utworzy plik Dane_Z_Transformacji_BLH.txt:

		---------------------------------------------------------------------------------
		|                   Wykaz przetransformowanych współrzędnych                     |
		---------------------------------------------------------------------------------
		| NR PKT |          B[°]         |          L[°]         |          H[m]         |
		---------------------------------------------------------------------------------
		|       1|                 60.000|                 50.000|              10000.000|
		|       .|                 60.000|                 50.000|              10000.000|
		|       .|                 60.000|                 50.000|              10000.000|
		|       .|                 60.000|                 50.000|              10000.000|
		|       n|                 60.000|                 50.000|              10000.000|
		---------------------------------------------------------------------------------

- dla metody XYZ utworzy plik Dane_Z_Transformacji_XYZ.txt:

		---------------------------------------------------------------------------------
		|                   Wykaz przetransformowanych współrzędnych                     |
		---------------------------------------------------------------------------------
		| NR PKT |          X[m]         |          Y[m]         |          Z[m]         |
		---------------------------------------------------------------------------------
		|       1|               1000.000|               1000.000|               1000.000|
		|       .|               1000.000|               1000.000|               1000.000|
		|       .|               1000.000|               1000.000|               1000.000|
		|       .|               1000.000|               1000.000|               1000.000|
		|       n|               1000.000|               1000.000|               1000.000|
		---------------------------------------------------------------------------------

- dla metody NEU utworzy plik Dane_Z_Transformacji_NEU.txt:


					       Macierz obrotu dla pkt n
					 _                                 _
					|                                   |
					| 0.0016642  -0.7074597    0.7067517|
					| 0.0016659   0.7067537    0.7074578|
					| 0.9999972   0.0000000   -0.0023548|
					|_                                 _|



- dla metody PL2000 utworzy plik Dane_Z_Transformacji_PL2000.txt:

		---------------------------------------------------------------------------------
		|                   Wykaz przetransformowanych współrzędnych                     |
		---------------------------------------------------------------------------------
		| NR PKT |          X[m]         |          Y[m]         |          Z[m]         |
		---------------------------------------------------------------------------------
		|       1|               1000.000|               1000.000|               1000.000|
		|       .|               1000.000|               1000.000|               1000.000|
		|       .|               1000.000|               1000.000|               1000.000|
		|       .|               1000.000|               1000.000|               1000.000|
		|       n|               1000.000|               1000.000|               1000.000|
		---------------------------------------------------------------------------------

- dla metody PL1992 utworzy plik Dane_Z_Transformacji_PL1992.txt:

		---------------------------------------------------------------------------------
		|                   Wykaz przetransformowanych współrzędnych                     |
		---------------------------------------------------------------------------------
		| NR PKT |          X[m]         |          Y[m]         |          Z[m]         |
		---------------------------------------------------------------------------------
		|       1|               1000.000|               1000.000|               1000.000|
		|       .|               1000.000|               1000.000|               1000.000|
		|       .|               1000.000|               1000.000|               1000.000|
		|       .|               1000.000|               1000.000|               1000.000|
		|       n|               1000.000|               1000.000|               1000.000|
		---------------------------------------------------------------------------------






