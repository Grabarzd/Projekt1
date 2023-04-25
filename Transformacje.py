from math import pi,radians,tan,cos,sin
import numpy as np
import argparse
try:
    try:
        class Transformacje():
            def __init__(self, model: str = "GRS80"):
                """
                Parametry elipsoid:
                    a - duża półoś elipsoidy - promień równikowy
                    b - mała półoś elipsoidy - promień południkowy
                    flattening - spłaszczenie
                    e2 - mimośród^2
                    
                    
                Dostępne modele elipsoidy:
                    -GRS80
                    -WGS84
                    -Krasowskiego
                """
                
                if model == "GRS80":
                    self.a = 6378137
                    self.b = 6356752.31414036
                elif model == "WGS84":
                    self.a = 6378137
                    self.b = 6356752.31424518
                elif model == "Krasowski":
                    self.a = 6378245
                    self.b = 6356863.019
                else:
                    print(112*'!'+'\n')
                    print('''Podana wartosć nie jest obsługiwana poprzez program, wybierz z dostępnych uwzględniając wielkosć znaków:\n
                          -GRS80\n
                          -WGS84\n
                          -Krasowski\n\n\n''')
                    print(112*'!')
                        
                        
                    
        
                self.flattening = (self.a - self.b) / self.a
                self.e2 = (2 * self.flattening - self.flattening ** 2)
                
            def hirvonen(self,X,Y,Z):
                '''
                Funkcja pozwala wyznaczyć współrzędne geocentryczne punktu na powierzchni ziemi.
                
                INPUT:
                *******___
                X-odległość od środka masy ziemii do punktu, równoległa do kierunku północy || type==float, units==meters
                Y-odległość od środka masy ziemii do punktu, równoległa do kierunku wschodu || type==float, units==meters
                Z-odległość od środka masy ziemii do punktu, równoległa do osi obrotu ziemii  || type==float, units==meters
                
                OUTPUT:
                *******
                f-długość geocentryczna || type==float, units==radians
                l-szerokość geocentryczna || type==float, units==radians
                h-odległość pomiędzy punktami przecięcia pierwszego wertykału z wielką półosią oraz osią obrotu ziemi || type==float, units==meters
        
                Dodatkowy opis:
                ***************
                Wykorzystujemy iterację do wyznaczenia ostatecznej wartości f, pozwoli ona na wyznaczenie pozostałych parametrów.
                
                '''
                p = np.sqrt(X**2 + Y**2)
                #print('p=',p)
                f = np.arctan(Z /( p * (1 - self.e2)))
                #dms(f)
                while True:
                    N = self.a / np.sqrt(1- self.e2 * np.sin(f)**2)
                    #print('N = ',N)
                    h = (p / np.cos(f)) - N
                   # print('h = ',h)
                    fp = f
                    f = np.arctan(Z / (p * (1 - self.e2 * (N / (N + h)))))
                    #dms(f)
                    if np.abs(fp - f) <( 0.000001/206265):
                        break
                l = np.arctan2(Y,X)
                return (f,l,h)
            
            def flh2XYZ(self,f,l,h):
                '''
                Funkcja transformuje współrzędne geocyntryczne na współrzędne kartezjańskie.
        
                INPUT:
                *******___
                f-długość geocentryczna || type==float, units==radians
                l-szerokość geocentryczna || type==float, units==radians
                h-odległość pomiędzy punktami przecięcia pierwszego wertykału z wielką półosią oraz osią obrotu ziemi || type==float, units==meters
        
                OUTPUT:
                *******
                X-odległość od środka masy ziemii do punktu, równoległa do kierunku północy || type==float, units==meters
                Y-odległość od środka masy ziemii do punktu, równoległa do kierunku wschodu || type==float, units==meters
                Z-odległość od środka masy ziemii do punktu, równoległa do osi obrotu ziemii  || type==float, units==meters
        
                Dodatkowy opis:
                ***************
                
                '''
                N = self.a / np.sqrt(1- self.e2 * np.sin(f)**2)
                X = (N + h) * np.cos(f) * np.cos(l)
                Y = (N + h) * np.cos(f) * np.sin(l)
                Z = (N * (1 - self.e2) + h) * np.sin(f) 
                return(X,Y,Z)
                
            
            
            def NEU(self,X,Y,Z):
                '''
                Funkcja ma na celu wyznaczenie macierzy obrotu dla podanych współrzędnych kartezjańskich
        
                INPUT:
                *******___
                X-odległość od środka masy ziemii do punktu, równoległa do kierunku północy || type==float, units==meters
                Y-odległość od środka masy ziemii do punktu, równoległa do kierunku wschodu || type==float, units==meters
                Z-odległość od środka masy ziemii do punktu, równoległa do osi obrotu ziemii  || type==float, units==meters
        
                OUTPUT:
                *******
                NEU-macierz obrotu || type==array, units==none
                
                Dodatkowy opis:
                ***************
                Argumenty w macierzy są wynikami zaiplementowanych funkcji trygonometrycznych z czego wynika brak jednostek.
                '''
                p = np.sqrt(X**2 + Y**2)
                #print('p=',p)
                f = np.arctan(Z /( p * (1 - self.e2)))
                #dms(f)
                while True:
                    N = self.a / np.sqrt(1- self.e2 * np.sin(f)**2)
                    #print('N = ',N)
                    h = (p / np.cos(f)) - N
                   # print('h = ',h)
                    fp = f
                    f = np.arctan(Z / (p * (1 - self.e2 * (N / (N + h)))))
                    #dms(f)
                    if np.abs(fp - f) <( 0.000001/206265):
                        break
                l = np.arctan2(Y,X)
                NEU = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                              [-np.sin(f)*np.sin(l), np.cos(l), np.cos(f)*np.sin(l)],
                              [np.cos(f), 0, np.sin(f)]])
                return NEU
                
                
                
                
            def fl2xygk1992(self,f,l):
                '''
                Cel
                
                INPUT:
                *******___
                f-długość geocentryczna || type==float, units==radians
                l-szerokość geocentryczna || type==float, units==radians
        
                OUTPUT:
                *******
                
                Dodatkowy opis:
                ***************
                
                '''
                l0=radians(19)
                b2 = (self.a ** 2) * (1 - self.e2)
                ep2 = (self.a ** 2 - b2) / b2
                dl = l - l0
                t = tan(f)
                n2 = ep2 * (cos(f) ** 2)
                N = self.a / np.sqrt(1- self.e2 * np.sin(f)**2)
                A0 = 1 - (self.e2 / 4) - ((3 * self.e2 ** 2) / 64) - ((5 * self.e2 ** 3) / 256)
                A2 = (3 / 8) * (self.e2 + (self.e2 ** 2) / 4 + (15 * self.e2 ** 3) / 128)
                A4 = (15 / 256) * (self.e2 ** 2 + (3 * self.e2 ** 3) / 4)
                A6 = (35 * self.e2 ** 3) / 3072
                sig = self.a * ((A0 * f) - (A2 * sin(2 * f)) + (A4 * sin(4 * f)) - (A6 * sin(6 * f)))
                xgk1992 = sig + ((dl ** 2 / 2) * N * sin(f) * cos(f) * (1 + (((dl ** 2)/12) * (cos(f) ** 2) * (5 - t **2 + 9 * n2 + 4 * n2 ** 2)) + (((dl ** 4) / 360) * (cos(f) ** 4 ) * (61 - 58 * (t ** 2) + t ** 4 + 270 * n2 - 330 * n2 * (t ** 2)))))
                ygk1992 = dl * N * cos(f) * (1 + (((dl ** 2)/6) * (cos(f) ** 2) * (1 - t ** 2 + n2)) + (((dl ** 4 ) / 120) * (cos(f) ** 4) * (5 - 18 * t ** 2 + t ** 4 + 14 * n2 - 58 * n2 * t ** 2)))   
                return(xgk1992,ygk1992)    
            
            def fl2xygk2000(self,f,l,l0):
                '''
                Cel
                
                INPUT:
                *******___
                f-długość geocentryczna || type==float, units==radians
                l-szerokość geocentryczna || type==float, units==radians
        
                OUTPUT:
                *******
                
                Dodatkowy opis:
                ***************
                
                '''
                b2 = (self.a ** 2) * (1 - self.e2)
                ep2 = (self.a ** 2 - b2) / b2
                dl = l - l0
                t = tan(f)
                n2 = ep2 * (cos(f) ** 2)
                N = self.a / np.sqrt(1- self.e2 * np.sin(f)**2)
                A0 = 1 - (self.e2 / 4) - ((3 * self.e2 ** 2) / 64) - ((5 * self.e2 ** 3) / 256)
                A2 = (3 / 8) * (self.e2 + (self.e2 ** 2) / 4 + (15 * self.e2 ** 3) / 128)
                A4 = (15 / 256) * (self.e2 ** 2 + (3 * self.e2 ** 3) / 4)
                A6 = (35 * self.e2 ** 3) / 3072
                sig = self.a * ((A0 * f) - (A2 * sin(2 * f)) + (A4 * sin(4 * f)) - (A6 * sin(6 * f)))
                xgk2000 = sig + ((dl ** 2 / 2) * N * sin(f) * cos(f) * (1 + (((dl ** 2)/12) * (cos(f) ** 2) * (5 - t **2 + 9 * n2 + 4 * n2 ** 2)) + (((dl ** 4) / 360) * (cos(f) ** 4 ) * (61 - 58 * (t ** 2) + t ** 4 + 270 * n2 - 330 * n2 * (t ** 2)))))
                ygk2000 = dl * N * cos(f) * (1 + (((dl ** 2)/6) * (cos(f) ** 2) * (1 - t ** 2 + n2)) + (((dl ** 4 ) / 120) * (cos(f) ** 4) * (5 - 18 * t ** 2 + t ** 4 + 14 * n2 - 58 * n2 * t ** 2)))   
                return(xgk2000,ygk2000)     
            
            def xy1992(self,xgk1992,ygk1992):
                '''
                Cel
                
                INPUT:
                *******
        
                OUTPUT:
                *******
                
                Dodatkowy opis:
                ***************
                
                '''
                m = 0.9993 
                x1992 = xgk1992 * m - 5300000
                y1992 = ygk1992 * m + 500000
                return(x1992,y1992)
            
            def strefy2000(self,l):
                '''
                Cel
                
                INPUT:
                ******
                l-szerokość geocentryczna || type==float, units==radians
        
                OUTPUT:
                *******
                
                Dodatkowy opis:
                ***************
                
                '''
                l0 = 0
                n = 0
                def dms2rad(d,m,s):
                    kat_rad = radians(d + m/60 + s/3600)
                    return (kat_rad)
                
                if l > dms2rad(13, 30, 0) and l < dms2rad(16, 30, 0):
                    l0 = l0 + dms2rad(15, 0, 0)
                    n = n + 5
                if l > dms2rad(16, 30, 0) and l < dms2rad(19, 30, 0): 
                    l0 = l0 + dms2rad(18, 0, 0)
                    n = n + 6
                if l > dms2rad(19, 30, 0) and l < dms2rad(22, 30, 0): 
                    l0 = l0 + dms2rad(21, 0, 0)
                    n = n + 7
                if l > dms2rad(22, 30, 0) and l < dms2rad(25, 30, 0): 
                    l0 = l0 + dms2rad(24, 0, 0)
                    n = n + 8
                return(l0,n)
        
            def xy2000(self,xgk2000,ygk2000,n):
                '''
                Cel
                
                INPUT:
                *******
        
                OUTPUT:
                *******
                
                Dodatkowy opis:
                ***************
                
                '''
                m = 0.999923
                x2000 = xgk2000 * m
                y2000 = ygk2000 * m + n * 1000000 + 500000
                return(x2000,y2000)
            
            def XYZ(self,filepath):
                '''
                Cel
                
                INPUT:
                *******
        
                OUTPUT:
                *******
                
                Dodatkowy opis:
                ***************
                
                '''
                file=open(filepath,'r')
                wiersze=file.readlines()
                dane=[]
                for i in wiersze:
                        xyz=i.split(' ')
                        X=xyz[0]
                        Y=xyz[1]
                        Z=xyz[2]
                        if '\n' in Z:
                            Z=Z[:-1]
                        dane.append([float(X),float(Y),float(Z)])
                return(dane)
            
            def BLH(self,filepath):
                '''
                Cel
                
                INPUT:
                *******
        
                OUTPUT:
                *******
                
                Dodatkowy opis:
                ***************
                
                '''
                file=open(filepath,'r')
                wiersze=file.readlines()
                dane=[]
                for i in wiersze:
                        xyz=i.split(' ')
                        B=xyz[0]
                        L=xyz[1]
                        H=xyz[2]
                        if '\n' in L:
                            H=H[:-1]
                        dane.append([float(B),float(L),float(H)])   
                return(dane)
            
            def BL(self,filepath):
                '''
                Cel
                
                INPUT:
                *******
        
                OUTPUT:
                *******
                
                Dodatkowy opis:
                ***************
                
                '''
                file=open(filepath,'r')
                wiersze=file.readlines()
                dane=[]
                for i in wiersze:
                        xyz=i.split(' ')
                        B=xyz[0]
                        L=xyz[1]
                        dane.append([float(B),float(L)])   
                return(dane)
        
        
        if __name__=='__main__':
            parser=argparse.ArgumentParser(description='Transformacja współrzednych')
            parser.add_argument('-filepath','--filepath', help='Ścieżka do pliku .txt')
            parser.add_argument('-m','--model',help='Dostępne modele elipsoidy:\n-GRS80\n-WGS84\n-Krasowski',type=str,default='GRS80',required=False)
            parser.add_argument('-method', '--method',help='Podaj co chcesz wyznaczyć:\n-BLH\n-XYZ\n-NEU\n-PL2000\n-PL1992',default='BLH')
            args = parser.parse_args()
            
            print("\n     Podana scieżka do pliku:      ", args.filepath)
            print("\n     Wybrany model elipsoidy:      ", args.model)
            print("\n     Wybrana transformacja:        ", args.method)
            
            #------------------------------------------------------------------------
            trans=Transformacje(args.model)
            dane=trans.XYZ(args.filepath)
            kolejnosc=0
            
            def dms(x):
                sig = ' '
                if x < 0:
                    sig = '-'
                    x = abs(x)
                x = x * 180/pi
                d = int(x)
                m = int(60 * (x - d))
                s = (x - d - m/60)*3600
                if d>360:
                    calosc=d//360
                    d=d-calosc*360
                print(sig,'%3d' % d,'°', '%2d' % m,"'",'%7.5f' % s,'"')
                
        
            if args.method=='BLH':
                dane=trans.XYZ(args.filepath)
                export=open('Dane_Z_Transformacjii_BLH.txt','w')
                export.write(81*'-'+'\n')
                export.write('|                   Wykaz przetransformowanych wspolrzednych                     |\n')
                export.write(81*'-'+'\n')
                export.write('| NR PKT |          B[°]         |          L[°]         |          H[m]         |\n')
                export.write(81*'-'+'\n')
                for i in dane:
                    kolejnosc+=1
                    X=i[0]
                    Y=i[1]
                    Z=i[2]
                    f,l,h=trans.hirvonen(X,Y,Z)
                    B=f*180/pi
                    L=l*180/pi
                    H=h
                    export.write(f'|{kolejnosc:8}|{B:23.7f}|{L:23.7f}|{H:23.3f}|\n')
                export.write(81*'-')
                export.close()
                    
                    
            elif args.method=='XYZ':     
                dane=trans.BLH(args.filepath)
                export=open('Dane_Z_Transformacjii_XYZ.txt','w')
                export.write(81*'-'+'\n')
                export.write('|                   Wykaz przetransformowanych wspolrzednych                     |\n')
                export.write(81*'-'+'\n')
                export.write('| NR PKT |          X[m]         |          Y[m]         |          Z[m]         |\n')
                export.write(81*'-'+'\n')
                for i in dane:
                    kolejnosc+=1
                    B=i[0]
                    L=i[1]
                    H=i[2]
                    X,Y,Z=trans.flh2XYZ(B,L,H)
                    export.write(f'|{kolejnosc:8}|{X:23.3f}|{Y:23.3f}|{Z:23.3f}|\n')
                export.write(81*'-')
                export.close()
                    
                    
            elif args.method=='NEU':
                dane=trans.XYZ(args.filepath)
                export=open('Dane_Z_Transformacjii_NEU.txt','w')
                for i in dane:
                    kolejnosc+=1
                    X=i[0]
                    Y=i[1]
                    Z=i[2]
                    NEU=trans.NEU(X,Y,Z)
                    print(f'{NEU=}')
                    export.write(7*' '+f'Macierz obrotu dla pkt {kolejnosc}\n')
                    export.write(' _'+33*(' ')+'_\n')
                    export.write('|'+35*(' ')+'|\n')
                    export.write(f'|{NEU[0][0]:10.7f}  {NEU[0][1]:10.7f}   {NEU[0][2]:10.7f}|\n|{NEU[1][0]:10.7f}  {NEU[1][1]:10.7f}   {NEU[1][2]:10.7f}|\n|{NEU[2][0]:10.7f}  {NEU[2][1]:10.7f}   {NEU[2][2]:10.7f}|\n')
                    export.write('|_'+33*(' ')+'_|'+5*'\n')
                export.close()
                    
            elif args.method=='PL2000':
                dane=trans.BL(args.filepath)
                export=open('Dane_Z_Transformacjii_PL2000.txt','w')
                export.write(58*'-'+'\n')
                export.write('|       Wykaz przetransformowanych wspolrzednych         |\n')
                export.write(58*'-'+'\n')
                export.write('| NR PKT |          X[m]         |          Y[m]         |\n')
                export.write(58*'-'+'\n')
                for i in dane:
                    kolejnosc+=1
                    B=i[0]
                    L=i[1]
                    l0,n=trans.strefy2000(L)
                    xgk2000, ygk2000=trans.fl2xygk2000(B, L, l0)
                    x2000,y2000=trans.xy2000(xgk2000, ygk2000, n)
                    X=x2000
                    Y=y2000
                    export.write(f'|{kolejnosc:8}|{X:23.3f}|{Y:23.3f}|\n')
                export.write(58*'-')
                export.close()
                    
                    
            elif args.method=='PL1992':
                dane=trans.BL(args.filepath)
                export=open('Dane_Z_Transformacjii_1992.txt','w')
                export.write(58*'-'+'\n')
                export.write('|       Wykaz przetransformowanych wspolrzednych         |\n')
                export.write(58*'-'+'\n')
                export.write('| NR PKT |          X[m]         |          Y[m]         |\n')
                export.write(58*'-'+'\n')
                for i in dane:
                    kolejnosc+=1
                    B=i[0]
                    L=i[1]
                    xgk1992, ygk1992=trans.fl2xygk1992(B, L)
                    x1992,y1992=trans.xy1992(xgk1992, ygk1992)
                    X=x1992
                    Y=y1992
                    export.write(f'|{kolejnosc:8}|{X:23.3f}|{Y:23.3f}|\n')
                export.write(58*'-')
                export.close()
                
            else:
                print(112*'!'+'\n')
                print(f'{args.method} nie jest obsługiwane przez program, proszę o wybór z dostępnej listy atrybutów:\n -BLH\n -XYZ\n -NEU\n -PL2000\n -PL1992')
                print('\n'+112*'!'+'\n')
    #------------------------------------------------------------------------
    except AttributeError:
        print('')
except FileNotFoundError:
    print(112*'!'+'\n')
    print(f'Plik {args.filepath} nie został odnaleziony, sprawdź czy scieżka została prawidłowo wpisana')
    print('\n'+112*'!'+'\n')