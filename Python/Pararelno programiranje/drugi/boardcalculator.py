from __future__ import print_function
import sys

def flush():
    sys.stdout.flush()
    return

class boardcalculator2():

    def __init__(self):
        self.polje = []
        for _ in range(0, 7):
            self.polje.append(["="] * 7)

    def dodajRed(self):
        self.polje.append(["="] * 7)
        return

    def printPolje(self):
        #ispis red po red, obrnuti redoslijed zato sto je polje pisano "naopacke"
        for x in reversed(self.polje):
            i = 0
            while (i < len(x)):
                print(x[i], sep = " ", end = " ")
                flush()
                i += 1
            print()
            flush()
        print()
        flush()
        return

    def provjeriKraj(self, odigraniStupac):
        #krivo predan stupac
        if (odigraniStupac not in range(0, 7)):
            return
        #stupac prazan
        if (self.polje[0][odigraniStupac] == "="):
            return None

        #pronalazak indeksa zadnje plocice
        i = len(self.polje) - 1 #od zadnjeg reda
        while (i >= 0):
            if (self.polje[i][odigraniStupac] != "="):
                break
            i -= 1

        return self.provjeriSveSmjerove(i, odigraniStupac)

    def provjeriSveSmjerove(self, i, odigraniStupac):
        label = self.polje[i][odigraniStupac]
        linija = self.dohvatiRedak(i)
        if (self.provjeriLiniju(linija, label)):
            return label

        linija = self.dohvatiStupac(odigraniStupac)
        if (self.provjeriLiniju(linija, label)):
            return label

        linija = self.dohvatiSlashDijagonalu(i, odigraniStupac)
        if (self.provjeriLiniju(linija, label)):
            return label

        linija = self.dohvatiBackslashDijagonalu(i, odigraniStupac)
        if (self.provjeriLiniju(linija, label)):
            return label
        return None
        
    def provjeriLiniju(self, linija, label):
        #dobivamo liniju i u njoj gledamo da li igdje ima niz od cetiri [label]
        duljina = len(linija) - 3
        for i in range(0, duljina):
            if (linija[i : i+4] == [label] * 4):
                return True
        return False

    def dohvatiRedak(self, red):
        return self.polje[red]

    def dohvatiStupac(self, stupac):
        linija = []
        #upisati element u stupcu "stupac" za svaki red
        for i in range(0, len(self.polje)):
            linija.append(self.polje[i][stupac])
        return linija

    def dohvatiSlashDijagonalu(self, red, stupac):
        i = red
        j = stupac
        linija = []
        #polje 3x3 ima labele:
        #00 01 02
        #10 11 12
        #20 21 22
        #za 11 dohvacamo liniju [00 11 22]
        while (i > 0 and j > 0):
            i -= 1
            j -= 1
        #pomaknuli smo se skroz dolje-lijevo
        #sad se micemo gore-desno dok i < ukupni broj redova i j < broj stupaca
        while (i < len(self.polje) and j < len(self.polje[0])):
            linija.append(self.polje[i][j])
            i += 1
            j += 1
        return linija

    def dohvatiBackslashDijagonalu(self, red, stupac):
        i = red
        j = stupac
        linija = []
        while (i > 0 and j < (len(self.polje[0])-1) ):
            i -= 1
            j += 1
        
        while (i < len(self.polje) and j >= 0):
            linija.append(self.polje[i][j])
            i += 1
            j -= 1
        return linija
            
    def ubaci(self, label, stupac):
        #provjeri zadnji element u stupcu, da li treba dodati red
        if (self.polje[len(self.polje) - 1][stupac] != "="):
            self.dodajRed()

        #nadji mjesto za ubaciti u stupac
        i = len(self.polje) - 1
        while (i >= 0):
            if ((self.polje[i][stupac]) != "="):
                self.polje[i+1][stupac] = label
                break
            i -= 1
        #stupac je prazan
        if(i == -1):
            self.polje[0][stupac] = label
        
    def ponisti(self, stupac):
        i = len(self.polje) - 1
        while (i >= 0):
            if ((self.polje[i][stupac]) != "="):
                self.polje[i][stupac] = "="
                break
            i -= 1