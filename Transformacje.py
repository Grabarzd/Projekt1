from math import *
import numpy as np
import statistics as st

class Transformacje():
    def __init__(self, elipsoida: str = "GRS80"):
        """

        """
        if elipsoida == "GRS80":
            self.a = 6378137
            self.b = 6356752.31414036
        elif elipsoida == "WGS84":
            self.a = 6378137
            self.b = 6356752.31424518 


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
            print(f,l,h)
            return (f,l,h)
    
    
        def flh2XYZ(self,f,l,h):
            N = self.a / np.sqrt(1- self.e2 * np.sin(f)**2)
            X = (N + h) * np.cos(f) * np.cos(l)
            Y = (N + h) * np.cos(f) * np.sin(l)
            Z = (N * (1 - self.e2) + h) * np.sin(f) 
            print(X,Y,Z)
            return(X,Y,Z)
        