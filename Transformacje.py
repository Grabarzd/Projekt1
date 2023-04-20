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