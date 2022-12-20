import multiprocessing as mp
from time import sleep
from typing import List
import numpy as np

class Visitor:
    #numOfTickets je koliko puta ce se voziti
    def __init__(self, name, numOfTickets = None):
        self.name = "visitor" if name is None else name
        self.proc = None
        self.numOfTickets = 5 if numOfTickets is None else numOfTickets

    def start(self, inQueue: mp.Queue, outQueue: mp.Queue):
        self.proc = mp.Process(
                target = self.work,
                args = (inQueue, outQueue),
                daemon = True,
                name = self.name)
        self.proc.start()

    def work(self, inQueue: mp.Queue, outQueue: mp.Queue):
        for _ in range(self.numOfTickets):
            sleep(np.random.uniform(0.3, 2.0))
            #Javlja da zeli na voznju
            outQueue.put("Zelim na vrtuljak")

            #Ceka poruku
            while True:
                message = inQueue.get()
                #ako je kriva poruka vraca ju
                if message != "Sjedni":
                    inQueue.put(message)
                else:
                    break
            print("\nPosjetitelj " + self.name + " je sjeo na vrtuljak.")

            #Ceka kraj voznje
            while True:
                message = inQueue.get()
                #ako je kriva poruka vraca ju
                if message != "Ustani":
                    inQueue.put(message)
                else:
                    break
            print("\nPosjetitelj " + self.name + " je sisao sa vrtuljka.")
            
        print("\nPosjetitelj " + self.name + " vise nema karti za vrtuljak.")


class Carousel:
    def __init__(self, maxVisitors = None, numOfTickets = None):
        self.maxVisitors = 4 if maxVisitors is None else maxVisitors
        self.numOfTickets = 2 if numOfTickets is None else numOfTickets
        self.inQueue = mp.Queue()
        self.outQueue = mp.Queue()
        self.visitors: List[Visitor] = list()

    def work(self, numOfVisitors = None):
        #Stvara posjetitelje i stavlja ih u listu za pracenje
        numOfVisitors = 8 if numOfVisitors is None else numOfVisitors
        for i in range(numOfVisitors):
            self.visitors.append(Visitor(f"visitor{i}", self.numOfTickets))

        #Aktivira ih
        for visitor in self.visitors:
            visitor.start(self.outQueue, self.inQueue)
        
        remainingVisitors = numOfVisitors

        while remainingVisitors >= self.maxVisitors:
            #provjerava svoju listu zahtjeva
            while self.inQueue.get() != "Zelim na vrtuljak":
                sleep(0.1)
            
            #Dopusta n (n = broj sjedala) posjetitelja na vrtuljak
            for _ in range(self.maxVisitors):
                self.outQueue.put("Sjedni")

            #ceka da se mjesta popune
            while self.outQueue.qsize() != 0:
                sleep(0.1)
            
            sleep(0.5)
            print("\nVrtuljak pokrenut")
            sleep(np.random.uniform(2.0, 4.0))
            print("\nVrtuljak zaustavljen, posjetitelji su razoracani s trajanjem voznje.")

            #salje poruku posjetiteljima da se mogu ustati
            for _ in range(self.maxVisitors):
                self.outQueue.put("Ustani")

            #ceka da se ustanu
            while self.outQueue.qsize() != 0:
                sleep(0.1)

            sleep(1.5)
            #Prebrojava preostali broj posjetitelja
            remainingVisitors = np.count_nonzero(np.array([x.proc.exitcode is None for x in self.visitors]))

        print("\nVrtuljak zavrsio s radom.")
        

def main():
    carousel = Carousel()
    carousel.work()
    
if __name__ == "__main__":
    main()