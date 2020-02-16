import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
from matplotlib import rc
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox


class PROGRAM:
    def __init__(self):
        
        self.root = Tk()
        self.root.resizable(0, 0)
        #Promenjive koje sadrze ono sto je upisano u Entry
        self.AlfaR = DoubleVar()
        self.AlfaI = DoubleVar()
        self.BetaR = DoubleVar()
        self.BetaI = DoubleVar()

        #rezolucija i naziv prozora
        self.root.geometry("500x300")
        self.root.title("Qubit Representation")

        #Ucitavamo vrednosti :
        label1 = Label(text = "Alpha (Real part): ")
        label1.place(x=50, y=50)
        self.AlfaREntry = Entry(textvar=self.AlfaR, width=5)
        self.AlfaREntry.place(x=180, y=50)
 
        label2 = Label(text = "(Imaginary part): ")
        label2.place(x=250, y=50)
        self.AlfaIEntry = Entry(textvar=self.AlfaI, width=5)
        self.AlfaIEntry.place(x=380, y=50)

        label3 = Label(text = "Beta (Real part): ")
        label3.place(x=50, y = 120)
        self.BetaREntry = Entry(textvar=self.BetaR, width=5)
        self.BetaREntry.place(x=180, y = 120)
    
        label4 = Label(text = "(Imaginary part): ")
        label4.place(x=250, y = 120)
        self.BetaIEntry = Entry(textvar=self.BetaI, width=5)
        self.BetaIEntry.place(x=380, y = 120)


        label5 = Label(text = "The sum of absolute alpha squared and absolute beta squared must be 1!", background='green',  font='Helvetica 10 bold')
        label5.place(x=15, y=200)
        
    
        self.button = Button(text="Bloch's sphere", command=self.Bloh) #Dugme koje ako prisinemo idemo na self.Bloh i pozivamo prikaz Blohove sfere
        self.button.place(x=100, y=250)

        self.button = Button(text="Calculate", command=self.Izracunaj) #Dugme, command je funkcija koja se poziva ako se pritisne.
        self.button.place(x=325, y=250)
        #Kada pritisnemo izracunaj idemo na funkciju self.Izracunaj

        #Pozivamo petlju koja ce da osvezava prikaz prozora i da ga menja ako treba
        self.root.mainloop()


    def uslov(self):
        #implementiramo numpy tip za kompleksan broj, prvi element je realan broj a drugi imaginarni
        #Iz promenjive koja sadrzi podatke koji su stavljeni u Entry uzimamo trenutnu vrednost preko  .get()
        self.alfa = np.complex(self.AlfaR.get(), self.AlfaI.get())
        self.beta = np.complex(self.BetaR.get(), self.BetaI.get())

        Theta = 2* (np.arccos(self.alfa))
        i_constant = np.complex(0, 1)

        #Prema formuli izracunavamo uglove vektora kjubita sa osama unutar Blohove svere
        #To smo implementirali ovde jer cuvamo za kasnije rezultat jer ce nam trebati

        if(self.beta == 0):
            Phi=0
        else:
            tmp = self.beta/(np.sin(Theta/2))
            tmp = np.log(tmp)
            Phi = tmp/i_constant

        self.x = np.sin(Theta)*np.cos(Phi)
        self.y = np.sin(Theta)*np.sin(Phi)
        self.z = np.cos(Theta)
        
        #Ovde unapred racunam tacku na Blohovoj sferi na koju vektor tog kjubita pokazuje
        normala = np.sqrt((self.alfa*np.conjugate(self.alfa) + self.beta*np.conjugate(self.beta)))
        #Formula sqrt(a^2 + b^2)

        if(normala <= 1.02 and normala >= 0.98): #Zbog aproksimacije korena. Ovde proveravamo da li je jednako 1
        # i na osnovu toga vracamo logicku vrednost
            return True
        else:
            return False

    def Bloh(self):

        if(self.uslov()):
            self.root.destroy()
            self.pokreniBloh()
            self.__init__()
            
        else:
            messagebox.showerror("Error", "Not a  qubit")       #Inace ako nije kjubit iskace prozor za greske
    
    def pokreniBloh(self):
        u = np.linspace(0, np.pi, 15)                           #Definisemo vektore koji su specificni za sferu
        v = np.linspace(0, 2 * np.pi, 15)

        x = np.outer(np.sin(u), np.sin(v))#I mnozimo sinuse ovih vektora i kao povratnu vrednost dobijamo matricu 
        y = np.outer(np.sin(u), np.cos(v))
        z = np.outer(np.cos(u), np.ones_like(v))#np.ones_like -> Return an array of ones with the same shape and type as a given array.

        fig = plt.figure() #Konstruisemo prozor i prostor za prikaz
        fig.canvas.set_window_title('Bloch sphere')
        ax = plt.axes(projection='3d')

        ax.set_axis_off()

        ax.text(0, 0, 1.4, '|0>', fontsize=14)
        ax.text(0, 0, -1.4, '|1>', fontsize=14) 

        ###KOORDINATE###
        ax.quiver(0, 0, 0, np.float64(1.0), 0, 0, arrow_length_ratio = 0.1, length = 1, normalize = True, color="green")
        ax.quiver(0, 0, 0, 0, np.float64(1.0), 0, arrow_length_ratio = 0.1, length = 1, normalize = True, color="red")
        ax.quiver(0, 0, 0, 0, 0, np.float64(1.0), arrow_length_ratio = 0.1, length = 1, normalize = True, color ="blue")
        

        #Vektor koji predstavlja kjubit u sferi i pokazuje na tacku izracunatu u self.uslov()
        
        ax.quiver(0, 0, 0, self.x, self.y, self.z, arrow_length_ratio = 0.1,length = 1, normalize = True, color="black")
        

        ax.plot_wireframe(x, y, z, color="grey", linewidth=0.5)#Pravimo sferu kao wireframe, tj kao kostur
        
        plt.show()#I prikazujemo napravljen prikaz/prostor

    def Izracunaj(self):
        
        if(self.uslov()):
            self.root.destroy()
            self.pokreniIzracunaj()
            self.__init__()
        else:
            messagebox.showerror("Error", "Not a qubit")           #Inace iskace prozor sa greskom

    def pokreniIzracunaj(self):
        fig = plt.figure(figsize=(8, 4)) 
        fig.canvas.set_window_title('Measurement')
        ax = plt.axes(projection='3d')
        ax.set_axis_off()
        ax.dist = 30#I posmatram prikaz sa daljine od 30

        ax.quiver(0, 0, 0, np.float64(4.0), 0, 0, length = 1, color="green", arrow_length_ratio = 0.05)
        #quiver predstavlja vektor, gde prva tri broja predstavljaju pocetnu tacku a sledeca tri zavrsnu
        #Prva tri quiver-a su x, y i z ose
        ax.quiver(0, 0, 0, 0, np.float64(4.0), 0, length = 1, color="red", arrow_length_ratio = 0.05)
        ax.quiver(0, 0, 0, 0, 0, np.float64(4.0),length = 0.5, color ="blue", arrow_length_ratio = 0.05)
       
        ax.quiver(0, 0, 0, 0, 0, 1, length=1, normalize = True, color="black", arrow_length_ratio = 0.1)
        #Vektor koji predstavlja ilustraicju kjubita koji dolazi u dodir sa operatorom merenja (pre merenja)



        M0 = np.array([[1, 0], [0, 0]])
        M1 = np.array([[0, 0], [0, 1]])

        Bra = np.array([np.conjugate(self.alfa), np.conjugate(self.beta)])
        ket = np.array([self.alfa, self.beta])

        p0 = Bra.dot(M0)
        p0 = p0.dot(ket)

        p1 = 1.0-p0

        """
        p0 = self.alfa*np.conjugate(self.alfa)
        #Racunam verovatnoce konjugovanjem alfa
        p1 = self.beta*np.conjugate(self.beta)
        """

        p0 = round(p0, 2)
        p1 = round(p1, 2)
        #Zaokruzujem decimale

        #U slucaju da se ne sabiraju do 1 za 0.01 zbog zaokruzivanja
        #Treba nam zbog funkcije da se verovatnoce sabiraju do tacno 1
        if((p0+p1) < 1):
            while((p0+p1)!=1):
                p0 += 0.01
                if((p0+p1)==1):
                    break
                p1+= 0.01
        elif((p0+p1) > 1):
            while((p0+p1)!=1):
                p0 -= 0.01
                if((p0+p1)==1):
                    break
                p1 -= 0.01

        result = np.random.choice([0, 1], 1, p=[p0, p1]) 
        #Random sa verovatnocom p0 za 0 i verovatnocom p1 za 1

        ax.text(-1, 0, 1.5, '|0>', fontsize=14)
        ax.text(1, 0, 1.5, '|1>', fontsize=14)
        #Stavljamo tekst na prostor prema kojem ce vektor pokazivati u zavisnosti od merenja

        if(result==1):
            ax.quiver(0, 0, np.float64(1), np.float64(1), 0, np.float64(.5), color="red", arrow_length_ratio = 0.1) #Vektor ka |1> ako je izmeren 1
        else:
            ax.quiver(0, 0, np.float64(1), np.float64(-1), 0, np.float64(.5), color="red", arrow_length_ratio = 0.1)#Vektor ka |0> ako je izmeren 0

        ax.text(0, 1.2, 1, 'M0 ', fontsize=14)#Naziv pored pravougaonika koji predstavlja operator merenja
        ax.text(-1, 1.9, 1, 'P0 = ' + str(np.float64(p0)), fontsize=14) #Rezultat racunanja p0

        x = np.linspace(-1,1,2)
        y = np.linspace(-1,1,2)

        X,Y = np.meshgrid(x,y)
        Z=0*X + 0*Y + 1.0 
        surf = ax.plot_surface(X, Y, Z, color=(0.94, 0.99, 0.16, 0.5))
        plt.show()#Onda prikazujem formiran prostor
   
      
        
A = PROGRAM() 
