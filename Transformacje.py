from math import pi,radians,tan,cos,sin
import numpy as np
import argparse

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


        self.flattening = (self.a - self.b) / self.a
        self.e2 = (2 * self.flattening - self.flattening ** 2)
        
    def hirvonen(self,X,Y,Z):
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
        
        
    def flh2XYZ(self,f,l,h):
        N = self.a / np.sqrt(1- self.e2 * np.sin(f)**2)
        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - self.e2) + h) * np.sin(f) 
        return(X,Y,Z)
        
    
    
    def NEU(self,X,Y,Z):
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
        R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                      [-np.sin(f)*np.sin(l), np.cos(l), np.cos(f)*np.sin(l)],
                      [np.cos(f), 0, np.sin(f)]])
        return R
        
        
        
        
    def fl2xygk1992(self,f,l):
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
        m = 0.9993 
        x1992 = xgk1992 * m - 5300000
        y1992 = ygk1992 * m + 500000
        return(x1992,y1992)
    
    def strefy2000(self,l):
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
        m = 0.999923
        x2000 = xgk2000 * m
        y2000 = ygk2000 * m + n * 1000000 + 500000
        return(x2000,y2000)
    
    def XYZ(self,filepath):
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