import main
import numpy as np
import random
import math
import sys
import matplotlib.pyplot as plt

def geneticAlgorithm(minimum, maximum, popSize, binDisplayPrecision, fja, maxIters, pMutate, opMode, tournament):
    """
    minimum = donja granica  
    maximum = gornja granica  
    fja = funckija za ocjenjivanje  
    popSize = velicina populacije  
    ~~displayMode = binarno (dispMode = 1) ili s pomičnom točkom (dispMode = 2)~~  
    maxIters = koliko puta se provodi genetski algoritam  
    pMutate = vjerojatnost mutiranja  
    opMode = nacin krizanja i mutacija (1 = aritmeticko i jednolika; 2 = uniformno i jednostavna)  
            UJEDNO I DISPLAY MODE.
    tournament = broj elemenata u turniru
    """

    if opMode not in (1, 2):
        print("Error, display mode not set to 1 or 2.")
        return
    if (tournament < 3):
        print("Error, tournament size must be 3 or higher.")
        return

    #Maksimalni broj bitova potrebnih za bilo koji broj
    #iznosi (max - min) * 10^preciznost
    maxBinLen = "{0:b}".format((maximum[0] - minimum[0]) * 10**binDisplayPrecision).__len__()

    #stvori populaciju; popis ocjena clanova pop i najbolji
    population, populationBinary, ratings, best = createPopulation(minimum, maximum, popSize, fja, maxBinLen)
    
    currIter = 0
    while (checkIfNotFinished(ratings[best], currIter, maxIters)):
        #odaberi koji sudjeluju u turniru
        tournamentMembers = getTournamentParticipants(popSize, tournament)
        firstBest, secondBest, worst = evaluateTournamentParticipants(tournamentMembers, tournament, ratings)

        #Krizaj
        if (opMode == 1):
            #Aritmeticko krizanje i istim
            new = arithmeticCross(population[firstBest], population[secondBest])
            #Jednolika mutacija
            equalizedMutation(new, pMutate)
        else:
            #Uniformno krizanje
            newBin = uniformCross(populationBinary[firstBest], populationBinary[secondBest], maxBinLen)
            #Jednostavna mutacija
            simpleMutation(newBin, pMutate)
            #azuriranje decimalnog broja 
            new = getDecimal(newBin, minimum, maximum, maxBinLen, binDisplayPrecision)

        rat = fja.calculate(new)
        #print("New rating: " + str(rat))
        #print("Old rating: " + str(ratings[worst]))
        if (rat < ratings[worst]):
            #print("New member is " + str(new[0]) + " " + str(new[1]))
            #print("replacing " + str(population[worst][0]) + " " + str(population[worst][1]))

            #TAKODJER AZURIRAJ POLOZAJ BEST AKO JE WORST MANJI OD BEST.
            if (worst < best):
                best -= 1
            del ratings[worst]
            del population[worst]
            if(opMode == 2):
                del populationBinary[worst]
                populationBinary.append(newBin)
            ratings.append(fja.calculate(new))
            population.append(new)

        if (ratings[worst] < ratings[best]):
            best = worst
            #print("Changed best " + str(best))

        if (currIter % 100 == 0):
            printResults(opMode, currIter, population[best], populationBinary[best], ratings[best])
           
        currIter+=1
    printResults(opMode, -1, population[best], populationBinary[best], ratings[best])

    ####################### odkomentiraj za boxplot
    """
    plt.cla()
    plt.clf()
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    one = []
    two = []
    for i in range(population.__len__()):
        one.append(population[i][0])
        two.append(population[i][1])
    three = []
    three.append(one)
    three.append(two)
    bp = ax.boxplot(three)
    fig.savefig('figure'+str(opMode)+'.png', bbox_inches='tight')
    """
    ####################### odkomentiraj za boxplot

    return

def printResults(mode, iters, best, bestbin, rating):
    if (mode == 1):
        #final print
        if (iters == -1):
            sys.stdout.write("Finally, best found is [")
        #prints every 100 iters
        else:
            sys.stdout.write("(iter: %i) Current best is [" %(iters))
        for i in range(best.__len__()):
            sys.stdout.write("{:.3f}".format(best[i]))
            if (i != best.__len__()-1):
                sys.stdout.write(", ")
        sys.stdout.write("] with a rating of %.03f\n" %(rating))
    elif (mode == 2):
        #final print
        if (iters == -1):
            sys.stdout.write("Finally, best found is [")
        else:
            sys.stdout.write("(iter: %i) Current best is [" %(iters))
        for i in range(best.__len__()):
            sys.stdout.write(bestbin[i])
            if (i != bestbin.__len__()-1):
                sys.stdout.write(", ")
        sys.stdout.write("] (")
        for i in range(best.__len__()):
            sys.stdout.write("{:.3f}".format(best[i]))
            if (i != best.__len__()-1):
                sys.stdout.write(", ")
        sys.stdout.write(") with a rating of %.03f\n" %(rating))



def createPopulation(minimum, maximum, popSize, fja, maxBinLen):
    pop = []
    popBin = []
    rating = []
    best = None
    i = 0
    while (pop.__len__() < popSize):
        number = minimum.copy()
        for j in range(number.__len__()):
            number[j] += (maximum[j] - minimum[j]) * random.uniform(0, 1)
        rate = fja.calculate(number)
        pop.append(number)
        numBin = getBinary(number, minimum, maximum, maxBinLen)
        popBin.append(numBin)
        rating.append(rate)
        if (best == None):
            best = i
        elif (rate < rating[best]):
            best = i
        i+=1
    return pop, popBin, rating, best

def getBinary(num, minimum, maximum, maxBinLen):
    numBin = []
    for i in range(num.__len__()):
        numBin.append(0)
        value = num[i] - minimum[i]
        value *= (2**maxBinLen - 1)
        value /= (maximum[i] - minimum[i])
        valueInt = int(value)
        stringed = "{0:b}".format(valueInt)
        for _ in range(stringed.__len__(), maxBinLen):
            stringed = '0' + stringed
        numBin[i] = stringed
    return numBin

def getDecimal(numBin, minimum, maximum, maxBinLen, precision):
    new = []
    for i in range(numBin.__len__()):
        new.append(0)
        binList = [char for char in numBin[i]]
        for j in range(numBin[i].__len__()):
            new[i] += int(binList[j]) * 2**(maxBinLen-1-j)
        new[i] = minimum[i] + new[i] * (maximum[i]-minimum[i]) /(math.pow(2, maxBinLen)-1)
    return new

def checkIfNotFinished(best, currI, maxI):
    if (best < 1e-5 or currI > maxI):
        return False
    return True

def getTournamentParticipants(popSize, size):
    members = []
    while(members.__len__() < size):
        r = random.randint(0, popSize-1)
        if (members.__contains__(r)):
            continue
        members.append(r)
    return members

def evaluateTournamentParticipants(tM, size, ratings):
    fBest = 0
    worst = 0
    for i in range(size):
        #print(ratings[tM[i]])
        if (ratings[tM[i]] < ratings[tM[fBest]]):
            fBest = i
        if (ratings[tM[i]] > ratings[tM[worst]]):
            worst = i

    if (fBest == 0):
        sBest = 1
    else:
        sBest = 0
    for i in range(size):
        if (i == fBest):
            continue
        if (ratings[tM[i]] < ratings[tM[sBest]]):
            sBest = i

    return tM[fBest], tM[sBest], tM[worst]

def arithmeticCross(firstBest, secondBest):
    new = []
    rand = random.random()
    for i in range(firstBest.__len__()):
        new.append(0)
        new[i] = firstBest[i] * rand + secondBest[i] * (1-rand)
    return new

def equalizedMutation(new, pMutate):
    for i in range(new.__len__()):
        rand = random.random()
        #da li mutira
        if (rand <= pMutate):
            #ako mutira, broj ce se promjeniti za random u intervalu [-0.8, 0.8]
            mutDirection = random.random()
            if (mutDirection <= 0.5):
                new[i] -= 0.8*random.random()
            else:
                new[i] += 0.8*random.random()

def uniformCross(firstBest, secondBest, maximumBinLen):
    new = []
    for i in range(firstBest.__len__()):
        new.append(0)
        first = [char for char in firstBest[i]]
        second = [char for char in secondBest[i]]
        string = ""
        for j in range(first.__len__()):
            a = random.random()
            if (a <= 0.5):
                string += first[j]
            else:
                string += second[j]
        new[i] = string
    return new

def simpleMutation(new, pMutate):
    #mutating a single bit
    for i in range(new.__len__()):
        rand = random.random()
        rand = 0.2
        if (rand <= pMutate):
            #odlucili smo da ce mutirati; random odabiremo koji ce bit mutirati
            #lomim string reprezentaciju bin broja u listu
            value = [char for char in new[i]]
            randomBit = random.randint(0, new[i].__len__()-1)
            value[randomBit] = ('1' if value[randomBit] == '0' else '0') #flip value
            #vracanje liste char-ova u jedan string
            value = "".join(value) 
            new[i] = value

if __name__ == "__main__":
    main.main()
