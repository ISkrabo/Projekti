import functions
import declarations
import numpy as np

def main():
    print()
    min = []
    max = []
    maxPopSize = 150
    precision = 3
    fja = None
    #displayMode = 1
    #Display mode ce biti jednak kao calculationMode
    numOfIters = 10000
    pMutate = 0.25
    tournamentSize = 5

    #Zadatak 1
    """
    ispitati GA nad svim funkcijama u granicama [-50, 150], oba nacina prikaza rjesenja
    binarni prikaz min 3 decimalna mjesta.
    f3 pet varijabli
    f6 i f7 dvije varijable
    """
    """
    #Funkcija 1
    min = [-50, -50]
    max = [150, 150]
    fja = declarations.f1()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)

    #Funkcija 3 - 5 varijabli
    min = [-50, -50, -50, -50, -50]
    max = [150, 150, 150, 150, 150]
    fja = declarations.f3()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)

    #Funkcija 6, 7 - 2 varijable
    min = [-50, -50]
    max = [150, 150]
    fja = declarations.f6()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    fja = declarations.f7()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    """

    #Zadatak 2
    """GA na funkcijama 6, 7
    mijenjati dimenzionalnost (1, 3, 6, 10)
    """
    """
    min = [-50]
    max = [150]
    fja = declarations.f6()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    fja = declarations.f7()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    min = [-50, -50, -50]
    max = [150, 150, 150]
    fja = declarations.f6()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    fja = declarations.f7()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    min = [-50, -50, -50, -50, -50, -50]
    max = [150, 150, 150, 150, 150, 150]
    fja = declarations.f6()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    fja = declarations.f7()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    min = [-50, -50, -50, -50, -50, -50, -50, -50, -50, -50]
    max = [150, 150, 150, 150, 150, 150, 150, 150, 150, 150]
    fja = declarations.f6()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    fja = declarations.f7()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    """

    #Zadatak 3
    """
    za f6, f7 usporedi GA bin preciznost 4 i GA pomične točke.
    dimenzije 3, 6
    """
    """
    min = [-50, -50, -50]
    max = [150, 150, 150]
    fja = declarations.f6()
    precision = 4
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    fja = declarations.f7()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    min = [-50, -50, -50, -50, -50, -50]
    max = [150, 150, 150, 150, 150, 150]
    fja = declarations.f6()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    fja = declarations.f7()
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    """

    #zadatak 4
    """box-plot
    f6
    populacija (30, 50, 100, 200)
    vjerojatnost mutacije (0.1, 0.3, 0.6, 0.9)
    """
    """
    #ODKOMENTIRAJ BOXPLOT U functions.geneticAlgorithm
    min = [-50, -50]
    max = [150, 150]
    fja = declarations.f6()
    maxPopSize = 30
    pMutate = 0.1
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    maxPopSize = 50
    pMutate = 0.3
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    maxPopSize = 100
    pMutate = 0.6
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    maxPopSize = 200
    pMutate = 0.9
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    """

    #zadatak 5
    """ 
    nad f6 ili f7 provedi algoritam s razlicitim velicinama turnira
    """
    """
    min = [-50, -50]
    max = [150, 150]
    fja = declarations.f6()
    tournamentSize = 3
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    tournamentSize = 9
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    tournamentSize = 20
    getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize)
    """

    print("\naa")


def getGeneticBoth(min, max, maxPopSize, precision, fja, numOfIters, pMutate, tournamentSize):
    calculationMode = 1
    functions.geneticAlgorithm(min, max, maxPopSize, precision, fja, numOfIters, pMutate, calculationMode, tournamentSize)
    calculationMode = 2
    functions.geneticAlgorithm(min, max, maxPopSize, precision, fja, numOfIters, pMutate, calculationMode, tournamentSize)
    

if __name__ == "__main__":
    main()