import multiprocessing as mp
from time import sleep
from typing import List
import numpy as np
from queue import PriorityQueue
import os
import ast

class Philosopher:
    def __init__(self, time = None):
        self.readpipe = list()
        self.writepipe = list()
        self.readIDs = list()
        self.waitingQueue = list()
        self.clock = np.random.randint(0, 100 if time is None else time)

    #Sortira redove cekanja i odgovora po drugom elementu, tj. po clock-u
    def sortQueues(self):
        self.waitingQueue.sort(key=self.sortBySecond)

    def sortBySecond(self, elem):
        return elem[1]

    #broj identifier-a dobiva iz stvaranja procesa
    def work(self, identifier):
        self.identifier = identifier
        sleep(np.random.uniform(0.01, 3.))

        #Poruke su oblika [ID, CLOCK, Request_type]

        #trazenje ulaska u K.O.
        self.request(identifier)
        self.waitRequests()
        self.waitReplies()

        #sortiranje redova po Clock vrijednosti
        self.sortQueues()

        #provjera je li na redu za K.O.
        if self.waitingQueue[0][0] != identifier:
            self.waitYourTurn()

        #KRITICNI ODSJECAK
        print(f"Konferencija: Filozof {identifier} je za stolom.\n")
        sleep(3.)

        #izlazak iz K.O.
        self.exitKO()
        sleep(np.random.uniform(1.0, 2.5))

    #funkcije slanja, cekanja

    #Salje zahtjev (ID, Clock, REQ) i sprema u svoj red
    def request(self, identifier):
        request = prepareText(identifier, self.clock, "request")
        self.waitingQueue.append(request)
        print(f"Filozof {self.identifier} salje " + str(request))

        for pipe in self.writepipe:
            pipe.send(request)

    #Prima zahtjeve od drugih
    def waitRequests(self):
        for pipe in self.readpipe:
            response = pipe.recv()
            self.waitingQueue.append(response)
            self.clock = max(self.clock, response[1]) + 1
            print(f"Filozof {self.identifier} postavlja sat na " + str(self.clock))

            print(f"Filozof {self.identifier} prima: " + str(response))

        self.reply(self.identifier)

    #Slanje odgovora
    def reply(self, identifier):
        reply = prepareText(identifier, self.clock, "reply")
        print(f"Filozof {self.identifier} salje: " + str(reply))

        for pipe in self.writepipe:
            pipe.send(reply)

    #Ceka odgovore
    def waitReplies(self):
        for pipe in self.readpipe:
            reply = pipe.recv()

            print(f"Filozof {self.identifier} prima: " + str(reply))

    #Ceka svoj red za sudjelovanje na konferenciji
    def waitYourTurn(self):
        while True:
            currID = self.waitingQueue[0][0]
            if currID == self.identifier:
                break

            #cekamo na izlazak nekog drugog filozofa
            waitingID = currID
            if waitingID > self.identifier:
                waitingID -=1

            exitResponse = self.readpipe[waitingID].recv()

            self.waitingQueue.pop(0)

            print(f"Filozof {self.identifier} prima: " + str(exitResponse))

    #Izlazak iz kriticnog odsjecka
    def exitKO(self):
        queueMess = self.waitingQueue.pop(0)
        exitMess = prepareText(queueMess[0], queueMess[1], "exit")
        print(f"Filozof {self.identifier} salje: " + str(exitMess))
        
        for pipe in self.writepipe:
            pipe.send(exitMess)


#uzima elemente koji se trebaju poslati i stavlja ih u listu
def prepareText(t1, t2, t3:str):
    return [t1, t2, t3]

class Conference():
    def __init__(self, numOfPhilo = 3):
        self.numOfPhilo = numOfPhilo
        self.pipes = list()

    def start(self):
        #stvaranje polja koje sadrzi filozofe
        philosophers = [Philosopher() for _ in range(self.numOfPhilo)]
        #povezivanje filozofa
        self.connectPhilosophers(philosophers)

        #stvaranje procesa i pokretanje
        processes = list()
        for iden, philosopher in enumerate(philosophers):
            processes.append(mp.Process(
                    target = philosopher.work,
                    args = (iden,),
                    daemon = True,
                    name = f"Filozof {iden}"))
            processes[-1].start()

        #zavrsetak
        for process in processes:
            process.join()
        for pipe in self.pipes:
            pipe.close()
        print("Konferencija je zavrsila.")

    def connectPhilosophers(self, philosophers):
        #povezivanje svakog filozofa sa svakim, gdje poznajemo koja cijev povezuje s kojim
        for i in range(len(philosophers)):
            for j in range(i+1, len(philosophers)):
                #stvaranje cijevi
                i_read, i_write = mp.Pipe(False)
                j_read, j_write = mp.Pipe(False)
                #povezivanje
                philosophers[i].readpipe.append(j_read)
                philosophers[i].writepipe.append(i_write)
                philosophers[j].readpipe.append(i_read)
                philosophers[j].writepipe.append(j_write)
                #pamcenje
                self.pipes.extend([i_read, i_write, j_read, j_write])

def main():
    conference = Conference(4)
    conference.start()
    
if __name__ == "__main__":
    main() 

