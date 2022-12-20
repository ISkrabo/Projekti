import boardcalculator as BC
from mpi4py import MPI
import time
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

igrac = "P"
cpu = "C"

labelKraj = "kraj"
labelPodaci = "podaci"
labelRezultat = "rezultat"
labelWait = "wait"
labelZadatak = "zadatak"
labelZahtjev = "zahtjev"

maxDubinaWorker = 4

comm.barrier()

def flush():
    sys.stdout.flush()
    return

#master
if rank == 0:
    #####   funkcije   #####
    def getPlayerInput():
        #print("ubaci broj izmedju 1 i 7")
        #print("Stupac: ")
        #flush()
        stupac = input()
        try:
            stupac = int(stupac)
        except ValueError:
            print("ubaci broj izmedju 1 i 7")
            flush()
        if stupac not in range(1, 8):
            return getPlayerInput()
        return stupac - 1

    def provjeriKrajIgre(stupac):
        return board.provjeriKraj(stupac)

    def saljiZavrsetakRada():
        for i in range(1, size):
            comm.send({"type" : labelKraj}, dest = i)

    def getZadatak():
        #zadaci = dictionary
        for key in zadaci.keys():
            #ako value nije unesen znaci da zadatak nije jos rijesen
            if (zadaci.get(key) is None):
                return key
        return None

    def getKvaliteta():
        #dictionary
        kvaliteta = {}
        #izracunaj kvalitetu po stupcu
        for i in range(0, 7):
            suma = 0.0
            for j in range(0, 7):
                suma += zadaci[(i, j)]
            kvaliteta[i] = suma / 7
        return kvaliteta
    
    #####    main     #####

    board = BC.boardcalculator2()
    totalTimes = list()

    while True:

        #igrac igra
        stupac = getPlayerInput()
        board.ubaci(igrac, stupac)
        rezultat = provjeriKrajIgre(stupac)

        if rezultat is not None:
            board.printPolje()
            print("Pobjeda igrac")
            flush()
            #print(totalTimes)
            #flush()
            saljiZavrsetakRada()
            break

        #racunalo igra
        timeStart = time.time()

        #Zadaci: program racuna sve mogucnosti ubacivanja u stupce
        zadaci = {}
        for i in range(0, 7):
            for j in range(0, 7):
                zadaci[(i, j)] = None

        #predaj svim radnicima plocu
        for x in range(1, size):
            poruka = {
                "type": labelPodaci, 
                "board": board
            }
            comm.send(poruka, dest = x)
        
        #dohvacaj zahtjeve od radnika i predaj im zadatke
        brojRadnika = size - 1
        zavrsioRacunanje = False

        while not zavrsioRacunanje:
            #ucitaj zahtjev
            status = MPI.Status()
            poruka = comm.recv(source = MPI.ANY_SOURCE, status = status)
            source = status.Get_source()
            #vrati zahtjev
            if (poruka["type"] == labelZahtjev):
                zadatak = getZadatak()
                if (zadatak != None):
                    zadaci[zadatak] = True #zadatak se obradjuje
                    odgovor = {
                        "type": labelZadatak, 
                        "zadatak": zadatak
                    }
                    comm.send(odgovor, dest = source)
                #nema vise zadataka
                else:
                    brojRadnika -= 1
                    if brojRadnika == 0:
                        zavrsioRacunanje = True
                    odgovor = {"type": labelWait}
                    comm.send(odgovor, dest = source)

            elif(poruka["type"] == labelRezultat):
                zadano = poruka["zadatak"]
                rezultat = poruka["rezultat"]
                zadaci[zadano] = rezultat

        kvaliteta = getKvaliteta()
        stupac = max(kvaliteta, key = lambda a: kvaliteta.get(a))
    
        timeEnd = time.time()
        printstring = ""
        for x in kvaliteta.values():
            printstring += ("%4.3f " % x )
        print(printstring)
        flush()
        totalTimes.append(timeEnd - timeStart)

        board.ubaci(cpu, stupac)
        board.printPolje()
        rezultat = provjeriKrajIgre(stupac)
        if rezultat is not None:
            board.printPolje()
            print("pobjednik racunalo")
            flush()
            #print(totalTimes)
            #flush()
            saljiZavrsetakRada()
            break



else:
    #kod je "prepisan" od sluzbenih rjesenja slijednog algoritma "connect4"
    def evaluate(lastPlayed, lastColumn, depth):
        result = 0.0
        #total = 0.0
        bAllLose = True
        bAllWin = True

        rezultat = board.provjeriKraj(lastColumn)
        if (rezultat):
            if (lastPlayed == cpu):
                return 1
            else:
                return -1

        if (depth == 0):
            return 0
        depth -= 1
        if (lastPlayed == cpu):
            nextPlayer = igrac
        else:
            nextPlayer = cpu

        total = 0.0
        #moves = 7
        for column in range(0, 7): #broj stupaca = 7
            #unutar funkcije "ubaci" se provjerava da li treba novi red nadodati
            board.ubaci(nextPlayer, column)
            result = evaluate(nextPlayer, column, depth)
            board.ponisti(column)
            if (result > -1):
                bAllLose = False
            if (result != 1):
                bAllWin = False
            if (result == 1 and nextPlayer == cpu):
                return 1
            if (result == -1 and nextPlayer == igrac):
                return -1
            total += result
        if (bAllWin == True):
            return 1
        if (bAllLose == True):
            return -1
        total /= 7 #tj. /= moves
        return total

    
    while True:
        poruka = comm.recv(source = 0)

        if (poruka["type"] == labelPodaci):
            board = poruka["board"]

        if (poruka["type"] == labelKraj):
            break

        while True:
            zahtjev = {"type": labelZahtjev}
            comm.send(zahtjev, dest = 0)
            odgovor = comm.recv(source = 0)

            if (odgovor["type"] == labelWait):
                time.sleep(2.0)
                break

            zadatak = odgovor["zadatak"]
            
            #provjeri za dobiveni zadatak krajnje vrijednosti
            board.ubaci(cpu, zadatak[0])
            if (board.provjeriKraj(zadatak[0]) is not None):
                rezultat = 1
                board.ponisti(zadatak[0])
                poruka = {
                    "type" : labelRezultat, 
                    "zadatak" : zadatak, 
                    "rezultat" : rezultat
                    }
                comm.send(poruka, dest = 0)
                continue
            
            board.ubaci(igrac, zadatak[1])
            if (board.provjeriKraj(zadatak[1]) is not None):
                rezultat = -1
                board.ponisti(zadatak[1])
                board.ponisti(zadatak[0])
                poruka = {
                    "type" : labelRezultat,
                    "zadatak" : zadatak,
                    "rezultat" : rezultat
                }
                comm.send(poruka, dest = 0)
                continue
            
            #u prva dva poteza nije gotovo onda racunaj 
            rezultat = evaluate(lastPlayed = igrac, lastColumn = zadatak[1], depth = maxDubinaWorker)
            board.ponisti(zadatak[1])
            board.ponisti(zadatak[0])

            poruka = {
                "type" : labelRezultat,
                "zadatak" : zadatak,
                "rezultat" : rezultat
            }
            comm.send(poruka, dest = 0)
