import multiprocessing as mp
from time import sleep
import time
import numpy as np
from typing import List

#Klasa auto koji ima smjer i registraciju
class Car:
    def __init__(self, registration):
        self.registration = registration
        self.direction = (np.random.randint(0, 2)) #[0, 2> uzima

    #pokrece procese
    def start(self, inQueue: mp.Queue, outQueue: mp.Queue):
        self.proc = mp.Process(
            target = self.work,
            args = (inQueue, outQueue),
            daemon = True,
            name = self.registration
        )
        self.proc.start()

    #funkcija prelaska mosta
    def work(self, inQueue: mp.Queue, outQueue: mp.Queue):
        sleep(np.random.uniform(0.5, 1.0))

        #javlja semaforu da zeli preci
        poruka = "Auto " + str(self.registration) + " zeli na most, smjer " + str(self.direction)
        outQueue.put([poruka, self.registration, self.direction])
        print(poruka)

        #ceka dozvolu za prelazak
        while True:
            message = inQueue.get()
            if message != str(self.registration):
                inQueue.put(message)
                sleep(np.random.uniform(0.01, 0.3))
            else: break
        
        #prelazak mosta i dojavljivanje semaforu da je presao
        print("Auto " + str(self.registration) + " prelazi most")
        sleep(np.random.uniform(1.0, 3.0))
        outQueue.put(["Presao", None, None])
        print("Auto " + str(self.registration) + " je presao most")

#Klasa koja kontrolira koji automobili smiju prijeci (u kojem smjeru) i mijenja smijer.
class Semafor:
    def __init__(self, numOfCars = None):
        self.numOfCars = 10 if numOfCars is None else numOfCars
        self.inQueue = mp.Queue()
        self.outQueue = mp.Queue()
        self.cars: List[Car] = list()
        self.direction = np.random.randint(0, 2)

    def activate(self):
        #inicijalizacija automobila
        for i in range(self.numOfCars):
            self.cars.append(Car(str(i)))

        #pokretanje auta. Automobili citaju iz outQueue, a pisu u inQueue
        for c in self.cars:
            c.start(self.outQueue, self.inQueue)
        
        #dok ima auta koji nisu presli
        while self.numOfCars > 0:
            carsToPass = 0
            startTime = time.time()
            carsReady = list()
            #semafor ceka 3 sekunde i 3 auta maksimalno
            while (carsToPass < 3 and (time.time() - startTime) < 3.0):
                #provjerava da li ima auta spremnih za preci
                if (not self.inQueue.empty()):
                    message = self.inQueue.get()
                else: break

                #provjera ispravnosti poruke i dopustenog smjera
                if (message[1] != None and message[2] == self.direction):
                    carsReady.append(message[1])
                    carsToPass+=1
                else:
                    self.inQueue.put(message)
            
            #javlja autima da smiju prijeci
            for c in carsReady:
                self.outQueue.put(c)

            #provjerava, tj. ceka da auti predju
            while (carsToPass > 0):
                message = self.inQueue.get()
                if (message[0] == "Presao"):
                    carsToPass-=1
                    self.numOfCars-=1
                else:
                    self.inQueue.put(message)

            #promjena smjera
            self.direction = 1 if self.direction == 0 else 0
        print("\nSvi auti su presli.")

def main():
    semafor = Semafor()
    semafor.activate()
    
if __name__ == "__main__":
    main()