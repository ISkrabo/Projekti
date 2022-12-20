import multiprocessing as mp
from time import sleep
import time
import numpy as np
from typing import List

#azuriranje baze podataka
def updateDatabase(database, ID_proces, logical_clock_value):
    #pronalazi ispravni unos u bazi podataka i azurira
    for i, entry in enumerate(database):
        if (entry[0] == ID_proces):
            entry[1] = logical_clock_value
            entry[2] += 1
            database[i] = entry
            print(database)
            sleep(np.random.uniform(0.1, 2.0))

class Worker:
    def __init__(self, identifier):
        self.identifier = identifier
        self.readpipe = list()
        self.writepipe = list()
        self.waitingQueue = list()
        self.clock = np.random.randint(0, 100)

    #Sortira redove cekanja i odgovora po drugom elementu, tj. po clock-u
    def sortQueues(self):
        self.waitingQueue.sort(key=self.sortBySecond)

    def sortBySecond(self, elem):
        return elem[1]

    #broj identifier-a dobiva iz stvaranja procesa
    def work(self, database):
        sleep(np.random.uniform(0.01, 3.))

        #Poruke su oblika [ID, CLOCK, Request_type]

        #trazenje ulaska u K.O.
        self.request(self.identifier)
        self.waitRequests()
        self.waitReplies()

        #sortiranje redova po Clock vrijednosti
        self.sortQueues()

        #provjera je li na redu za K.O.
        if self.waitingQueue[0][0] != self.identifier:
            self.waitYourTurn()

        #KRITICNI ODSJECAK
        for _ in range(5):
            updateDatabase(database, self.identifier, self.clock)

        #izlazak iz K.O.
        self.exitKO()
        sleep(np.random.uniform(1.0, 2.5))

    #### funkcije slanja, cekanja ####

    #Salje zahtjev (ID, Clock, REQ) i sprema u svoj red
    def request(self, identifier):
        request = prepareText(identifier, self.clock, "request")
        self.waitingQueue.append(request)
        #print(f"Proces {self.identifier} salje " + str(request))

        for pipe in self.writepipe:
            pipe.send(request)

    #Prima zahtjeve od drugih
    def waitRequests(self):
        for pipe in self.readpipe:
            response = pipe.recv()
            self.waitingQueue.append(response)
            self.clock = max(self.clock, response[1]) + 1
            #print(f"Proces {self.identifier} postavlja sat na " + str(self.clock))

            #print(f"Proces {self.identifier} prima: " + str(response))

        self.reply(self.identifier)

    #Slanje odgovora
    def reply(self, identifier):
        reply = prepareText(identifier, self.clock, "reply")
        #print(f"Proces {self.identifier} salje: " + str(reply))

        for pipe in self.writepipe:
            pipe.send(reply)

    #Ceka odgovore
    def waitReplies(self):
        for pipe in self.readpipe:
            reply = pipe.recv()

            #print(f"Proces {self.identifier} prima: " + str(reply))

    #Ceka svoj red za azuriranje
    def waitYourTurn(self):
        while True:
            currID = self.waitingQueue[0][0]
            if currID == self.identifier:
                break

            #cekamo na zavrsetak nekog drugog procesa
            waitingID = currID
            if waitingID > self.identifier:
                waitingID -=1

            exitResponse = self.readpipe[waitingID].recv()

            self.waitingQueue.pop(0)

            #print(f"Proces {self.identifier} prima: " + str(exitResponse))

    #Izlazak iz kriticnog odsjecka
    def exitKO(self):
        queueMess = self.waitingQueue.pop(0)
        exitMess = prepareText(queueMess[0], queueMess[1], "exit")
        #print(f"Proces {self.identifier} salje: " + str(exitMess))
        
        for pipe in self.writepipe:
            pipe.send(exitMess)


class Database:
    def __init__(self):
        #database sadrzi elemente oblika:
        #       [ID_proces, logical_clock_value, No_of_critical_part_entries]
        self.workers: List[Worker] = list()
        self.pipes = list()

    #priprema procesa za rad s bazom
    def initialize(self, numOfProcesses):
        #manager koristen da bi svi procesi mogli raditi na istoj bazi podataka
        with mp.Manager() as manager: 
            numOfProcesses = 3 if numOfProcesses is None or numOfProcesses not in range(3, 11) else numOfProcesses
            #stvaranje baze
            database = manager.list([]) 

            #inicijalizacija procesa i stvaranje entry-a u bazi podataka
            for i in range(numOfProcesses):
                self.workers.append(Worker(i))
                database.append([i, None, 0])

            #povezivanje radnika za medjusobnu komunikaciju
            self.connectWorkers(self.workers)

            #pokretanje procesa + procesi dobivaju vezu s bazom podataka za uredjivanje
            processes = list()
            for i, w in enumerate(self.workers):
                processes.append(mp.Process(
                        target = w.work,
                        args = (database,),
                        daemon = True,
                        name = f"Proces {i}"))
                processes[-1].start()

            #zatvaranje procesa i cijevi
            for process in processes:
                process.join()
            for pipe in self.pipes:
                pipe.close()
            print("Zavrsilo.")

        
    def connectWorkers(self, workers):
        #povezivanje svakog procesa sa svakim, gdje poznajemo koja cijev povezuje s kojim
        for i in range(len(workers)):
            for j in range(i+1, len(workers)):
                #stvaranje cijevi
                i_read, i_write = mp.Pipe(False)
                j_read, j_write = mp.Pipe(False)
                #povezivanje
                workers[i].readpipe.append(j_read)
                workers[i].writepipe.append(i_write)
                workers[j].readpipe.append(i_read)
                workers[j].writepipe.append(j_write)
                #pamcenje
                self.pipes.extend([i_read, i_write, j_read, j_write])

def prepareText(t1, t2, t3:str):
    return [t1, t2, t3]

def main():
    database = Database()
    #inicijalizacija rada s bazom za zadani broj procesa
    database.initialize(3)

if __name__ == "__main__":
    main()
