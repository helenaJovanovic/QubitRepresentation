import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
from matplotlib import rc
from tkinter import *
from tkinter.ttk import *
import threading
from tkinter import messagebox

""" 
    Od biblioteka uvozimo:

    1. numpy - koji sluzi za matematicka izracunavanja i za predstavljanje odredjenih tipova koje inace ne bi imali u pajtonu,
    kao sto su numpy.complex koji se koristi ovde i float64 koji je superiorniji float tip nego onaj sa kojim pajton dolazi jer
    moze da sadrzi vise decimala. U kodu koristimo brojne matematcike funkcije kao sto su npr. numpy.random.choice i cojugate

    2. matplotlib - i njene podklase koje sluze za efikasno grafiranje funkcija, objekata i statistickih prikaza bilo u 2d ili 3d.
    matplot.pyplot predstavlja klasu koja sadrzi podatke o povrsini/prostoru na koju grafiramo i funkcije za prikaz na povrsini
    mpl_toolkits.mplot3d.axes3d je podklasa kojom implementiramo 3d objekte i u njoj imamo nekoliko predefinisanih tipova specificnih za 3d
    
    3. tkinter - je klasa za pravljenje GUI prikaza programa koja dolazi upakovana uz Pajton. Ova klasa izgleda malo zastarelo pa smo
    uveli i tkinter.ttk da bi modernizovali izgled prema danasnjim standardima

    4. threading - zbog cinjenice da otvaramo vise prozora u ovom programu i da zelimo da svaki funkcionise u isto vreme a ne da
    glavni ceka izvrsavanje prozora koji je pokrenuo (I samim tim se zaustavi) dodali smo jednu komponentu multiprogramiranja 
    i implementirali niti. Svaki otvoren prozor ima svoju nit

    Program smo implementirali koristeci objektno orijentisano programiranje zbog intuitivnosti i bolje citljivosti
    koda s obzirom na njegov obim.
"""


class PROGRAM:
    def __init__(self):
        """
            U konsuktorskoj funkciji pravimo GUI

        """
        
        self.root = Tk() #Poziv za pokretanje tkintera, self.root predstavlja ime glavnog prozora

        self.AlfaR = DoubleVar()#Promenjive koje sadrze ono sto je upisano u Entry
        self.AlfaI = DoubleVar()#Imaju svoj tip koji je definisan preko tkinter
        self.BetaR = DoubleVar()
        self.BetaI = DoubleVar()
        
        self.root.geometry("500x300")#rezolucija i naziv prozora
        self.root.title("Simulacija kjubita")

        label1 = Label(text = "Alfa (Realni deo): ")#Label koji sadrzi tekst
        label1.place(x=50, y=50)#.place funkcija koja postavlja objekat na (x, y) tacku na prozoru

        self.AlfaREntry = Entry(textvar=self.AlfaR, width=5)#Element za upis podataka. U textvar definisemo promenljivu koja sadrzi podatke iz Entry
        self.AlfaREntry.place(x=180, y=50)

        #Sve dalje je isto

        label2 = Label(text = "(Imaginarni deo): ")
        label2.place(x=250, y=50)
        self.AlfaIEntry = Entry(textvar=self.AlfaI, width=5)
        self.AlfaIEntry.place(x=380, y=50)

        label3 = Label(text = "Beta (Realni deo): ")
        label3.place(x=50, y = 150)
        self.BetaREntry = Entry(textvar=self.BetaR, width=5)
        self.BetaREntry.place(x=180, y = 150)
    
        label4 = Label(text = "(Imaginarni deo): ")
        label4.place(x=250, y = 150)
        self.BetaIEntry = Entry(textvar=self.BetaI, width=5)
        self.BetaIEntry.place(x=380, y = 150)

        self.button = Button(text="Pokreni bloh", command=self.Bloh) #Dugme koje ako prisinemo idemo na self.Bloh i pozivamo prikaz Blohove sfere
        self.button.place(x=100, y=220)

        self.button = Button(text="Izracunaj", command=self.Izracunaj) #Dugme, command je funkcija koja se poziva ako se pritisne.
        self.button.place(x=325, y=220)
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

        if(self.uslov()):#Proveravam uslov u odvojenoj funkciji koja vraca True ili False
            threading.Thread(target=self.pokreniBloh).start()#I pokrecem odvojenu nit i u njoj prozor koji ce prikazivati Blohovu sferu
        else:
            messagebox.showerror("Greska", "Nije kjubit") #Inace ako nije kjubit iskace prozor za greske
    
    def pokreniBloh(self):
        u = np.linspace(0, np.pi, 15)#Definisemo vektore koji su specificni za sferu
        v = np.linspace(0, 2 * np.pi, 15)



        x = np.outer(np.sin(u), np.sin(v))#I mnozimo sinuse ovih vektora i kao povratnu vrednost dobijamo matricu 
        y = np.outer(np.sin(u), np.cos(v))
        z = np.outer(np.cos(u), np.ones_like(v))#np.ones_like -> Return an array of ones with the same shape and type as a given array.

        fig = plt.figure() #Konstruisemo prozor i prostor za prikaz
        fig.canvas.set_window_title('Blohova sfera')#ime
        ax = plt.axes(projection='3d')#Tip projekcije

        ax.set_axis_off()#Iskljucujem default ose

        ax.text(0, 0, 1.4, '|0>', fontsize=14)#Malo teskta na ovim koordinatama (0, 0, +-1.4)
        ax.text(0, 0, -1.4, '|1>', fontsize=14) #Teksta sa vrha i donjeg dela sfere

        ax.quiver(0, 0, 0, np.float64(1.0), 0, 0, length = 1, normalize = True, color="green")
        ax.quiver(0, 0, 0, 0, np.float64(1.0), 0, length = 1, normalize = True, color="red")
        ax.quiver(0, 0, 0, 0, 0, np.float64(1.0),length = 1, normalize = True, color ="blue")
        #Ose koje pravim kao vektore prva tri broja predstavljaju pocetnu tacku a sledecih tri predstavlja krajnju tacku vektora
        #normalizujem ih i dajem im boje


        ax.quiver(0, 0, 0, self.x, self.y, self.z, length = 1, normalize = True, color="black")
        #Vektor koji predstavlja kjubit u sferi i pokazuje na tacku izracunatu u self.uslov()

        ax.plot_wireframe(x, y, z, color="grey", linewidth=0.5)#Pravimo sferu kao wireframe, tj kao kostur da se tako izrazim
        #Onda mozemo da vidimo unutar nje
        plt.show()#I prikazujemo napravljen prikaz/prostor

    def Izracunaj(self):
        #Proveravamo uslov za kjubit stanje u if pozivom funkcije self.uslov
        if(self.uslov()):
            threading.Thread(target=self.pokreniIzracunaj).start() #Pokrecemo funkciju unutar nove niti i tad se poziva prozor
        else:
            messagebox.showerror("Greska", "Nije kjubit") #Inace iskace prozor sa greskom

    def pokreniIzracunaj(self):
        fig = plt.figure(figsize=(8, 4)) #Pokrecemo prozor na kojem cemo da prikazemo prostor i podesavamo velicinu prozora
        fig.canvas.set_window_title('Merenje')#Ime prozora
        ax = plt.axes(projection='3d')#Ovde moramo da kazemo da zelimo da prikazemo 3d prostor
        ax.set_axis_off()#Uklanjam ose koje se nalaze sa strane jer mi ne trebaju za ovaj prikaz
        ax.dist = 30#I posmatram prikaz sa daljine od 30

        ax.quiver(0, 0, 0, np.float64(4.0), 0, 0, length = 1, color="green")
        #quiver predstavlja vektor, gde prva tri broja predstavljaju pocetnu tacku a sledeca tri zavrsnu
        #Prva tri quiver-a su x, y i z ose
        ax.quiver(0, 0, 0, 0, np.float64(4.0), 0, length = 1, color="red")
        ax.quiver(0, 0, 0, 0, 0, np.float64(4.0),length = 1, color ="blue")
       
        ax.quiver(0, 0, 0, 0, 0, 1, length=1, normalize = True, color="black")
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
            ax.quiver(0, 0, np.float64(1), np.float64(1), 0, np.float64(.5), color="red") #Vektor ka |1> ako je izmeren 1
        else:
            ax.quiver(0, 0, np.float64(1), np.float64(-1), 0, np.float64(.5), color="red")#Vektor ka |0> ako je izmeren 0

        ax.text(0, 1.2, 1, 'M0 ', fontsize=14)#Naziv pored pravougaonika koji predstavlja operator merenja
        ax.text(-1, 1.9, 1, 'P0 = ' + str(np.float64(p0)), fontsize=14) #Rezultat racunanja p0

        x = np.linspace(-1,1,2)#Definisem neke koordinate pravougaonika koji pravim
        y = np.linspace(-1,1,2)

        X,Y = np.meshgrid(x,y)#Vraca koordinatne matrice od koordinatnih vektora (Nemam pojma iskreno)
        Z=0*X + 0*Y + 1.0 #Z predstavlja 1 ne znam zasto ovo radim sebi
        surf = ax.plot_surface(X, Y, Z, color=(0.94, 0.99, 0.16, 0.5))#Crtam pravougaonik u zutoj boji u 3d
        plt.show()#Onda prikazujem formiran prostor
   
      
        
A = PROGRAM() #Pokrecemo klasu lol
