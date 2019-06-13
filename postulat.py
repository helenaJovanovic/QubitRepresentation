import numpy as np

class POSTULAT:
    def __init__(self):
        print("Alfa:")
        x = float(input())
        print("Imaginarni deo:")
        xI = float(input())
        print("Beta:")
        y = float(input())
        print("Imaginarni deo:")
        yI = float(input())

        self.alfa = np.complex(x, xI)
        self.beta = np.complex(y, yI)
    
    def izracunajVerovatnoce(self):
        self.p0 = np.sqrt(self.alfa*np.conjugate(self.alfa))
        self.p1 = np.sqrt(self.beta*np.conjugate(self.beta))

    def izbaciResenje(self):
        ran_int = np.random.randint(0, 101)
        ran_float = float(ran_int)/100.0

        print("======================================================================================")
        if((self.p0 + self.p1) != 1):
            print("nije kjubit")

        if(ran_float <= self.p0):
            print("Kjubit je: 0")
        else:
            print("Kjubit je: 1")


pokreni = POSTULAT()
pokreni.izracunajVerovatnoce()
pokreni.izbaciResenje()