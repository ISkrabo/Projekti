from mpi4py import MPI
from time import sleep
import random
import sys

#mpiexec -n 3 python filozofi.py

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#globalne varijable
#unos vilica po zahtjevu zadatka: p = prljava, c = cista
vilice = {
    "l": "p" if rank == 0 else " ",
    "r": " " if rank == size - 1 else "p"
}
#zapisivanje indeksa od susjeda
susjedi = {
    "l": size - 1 if rank == 0 else rank - 1,
    "r": 0 if rank == size - 1 else rank + 1
}

#stanja
stanja = set()
#spremnik zahtjeva
zahtjevi = set()
#zapisivanje smjerova slusanja
slusaj = {}

#funkcije
#mislim i dajem svoje vilice po zahtjevu
def misli():
    ispisi("mislim")
    n = random.randint(5, 10)
    while (n > 0):
        provjeraZahtjeva()
        n -= 1
        sleep(.2)

def ispisi(poruka):
    global vilice
    ispis = ""
    ispis += ("\t" * rank)
    ispis += poruka
    vil = "[" + vilice["l"] + vilice["r"] + "]"
    ispis += vil
    print(ispis)
    sys.stdout.flush()

#provjeravam stare i nove zahtjeve
def provjeraZahtjeva():
    global zahtjevi
    global slusaj
    #provjeri stare postojece zahtjeve
    if (len(zahtjevi) != 0):
        for smjer in zahtjevi:
            poruka = "zahtjev"
            odgovori(smjer, "zahtjev")
        #stari zahtjevi su obradjeni; izbrisi ih
        zahtjevi.clear()

    #provjeri zahtjeve susjeda
    for smjer in "lr":
        #pogledaj je li dosao novi zahtjev
        primljenNoviZahtjev, poruka = slusaj[smjer].test()
        if (primljenNoviZahtjev):
            odgovori(smjer, poruka)
            #buffer se mora osvjeziti 
            slusaj[smjer] = comm.irecv(source = susjedi[smjer])

def odgovori(smjer, poruka):
    global vilice
    #poruka je zahtjev
    if (poruka == "zahtjev"):
        #da li imam vilicu spremnu za dati
        if (vilice[smjer] == "p"):
            comm.isend("c", dest = susjedi[smjer])
            vilice[smjer] = " "
            ispisi("dajem " + smjer)
        else:
            #spremam za kasnije
            if smjer not in zahtjevi:
                zahtjevi.add(smjer)
                ispisi("pamtim " + smjer)
    #primam vilicu
    elif (poruka in "pc"):
        vilice[smjer] = poruka
        ispisi("primio " + smjer)

def nabaviVilice():
    global vilice
    ispisi("trazim vilice")
    #trazi periodicki
    spavao = 11
    #dok mi fali jedna ili dvije vilice
    while (vilice["l"] == " " or vilice["r"] == " "):
        #zatrazi vilicu koja mi fali, ako dugo cekam
        for smjer in "lr":
            if vilice[smjer] == " " and spavao > 10:
                comm.isend("zahtjev", dest = susjedi[smjer])
                spavao = 0
                ispisi("zahtjev " + smjer)
        #provjeri je li dobio vilicu
        provjeraZahtjeva()
        sleep(0.5)
        spavao += 1

def jedi():
    global vilice
    ispisi("jedem")
    sleep(random.uniform(1, 2.5))
    #vilice postavi na prljavo
    vilice = {"l": "p", "r": "p"}
    ispisi("jeo")

if __name__ == "__main__":
    global slusaj
    for smjer in "lr":
        if smjer not in slusaj:
            slusaj[smjer] = comm.irecv(source = susjedi[smjer])
    while(True):
        misli()
        nabaviVilice()
        jedi()