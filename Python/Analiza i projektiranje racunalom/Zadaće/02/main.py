import functions
import sys
import random
import numpy as np

def main():
    print("")
    
    """
    zad 1
    definirati Fju 3
    minimum u točki 3
    početna točka 10
    svi postupci
    ispisi minimum, broj evaluacija svakog postupka
    """
    #
    """
    Fja = functions.fprvizadatak()
    tocka = [10]
    #L, R = functions.unimodalInterval(1, tocka[0], Fja)

    #prvi nacin - zlatni rez za index i
    Lrez, Rrez = functions.goldenRatio(tocka, 0, 0, Fja)
    printGoldenRatio(Lrez, Rrez, Fja.step)
    Fja.step = 0

    #drugi nacin - pretrazivanje po KOOS-ima
    KooSTocka = functions.searchByCoordinates(tocka, Fja, 0)
    printSearchByCoordinates(KooSTocka, Fja.step)
    Fja.step = 0

    #treci nacin - simpleks 
    Xsimp = functions.simplex(tocka, Fja, 1.0, 0.5, 2, 0.5, 1, 0.000001)
    printSimplex(Xsimp, Fja.step)
    Fja.step = 0

    #cetvrti nacin - Hooke-Jeeves
    Xhj = functions.Hooke_Jeeves(tocka, Fja)
    printHooke_Jeeves(Xhj, Fja.step)
    
    """

    """
    Zad 2: 
    KooS, Simplex i H-J na funkcijama 1-4 uz zadane parametre i početne točke (Fja 3 imati 5 varijabli min)
    Prikaži rezultate tablično.
    """
    #
    """
    Fja1 = functions.f1()
    Fja2 = functions.f2()
    Fja3 = functions.f3()
    Fja4 = functions.f4()
    X1 = [-1.9, 2]
    X2 = [0.1, 0.3]
    X3 = [5, 5, 5, 5, 5]
    X4 = [5.1, 1.1]

    XrKooS1 = functions.searchByCoordinates(X1, Fja1, 0)
    XrKooS2 = functions.searchByCoordinates(X2, Fja2, 0)
    XrKooS3 = functions.searchByCoordinates(X3, Fja3, 0)
    XrKooS4 = functions.searchByCoordinates(X4, Fja4, 0)
    printTablicno("Pretrazivanje po koordinatim osima: ", XrKooS1, XrKooS2, XrKooS3, XrKooS4, Fja1.step, Fja2.step, Fja3.step, Fja4.step)
    Fja1.step = 0
    Fja2.step = 0
    Fja3.step = 0
    Fja4.step = 0

    XrSimp1 = functions.simplex(X1, Fja1, 1.0, 0.5, 2, 0.5, 1, 0.000001)
    XrSimp2 = functions.simplex(X2, Fja2, 1.0, 0.5, 2, 0.5, 1, 0.000001)
    XrSimp3 = functions.simplex(X3, Fja3, 1.0, 0.5, 2, 0.5, 1, 0.000001)
    XrSimp4 = functions.simplex(X4, Fja4, 1.0, 0.5, 2, 0.5, 1, 0.000001)
    printTablicno("Simpleks algoritam: ", XrSimp1, XrSimp2, XrSimp3, XrSimp4, Fja1.step, Fja2.step, Fja3.step, Fja4.step)
    Fja1.step = 0
    Fja2.step = 0
    Fja3.step = 0
    Fja4.step = 0

    XrHJ1 = functions.Hooke_Jeeves(X1, Fja1)
    XrHJ2 = functions.Hooke_Jeeves(X2, Fja2)
    XrHJ3 = functions.Hooke_Jeeves(X3, Fja3)
    XrHJ4 = functions.Hooke_Jeeves(X4, Fja4)
    printTablicno("Postupak Hooke-Jeeves: ", XrHJ1, XrHJ2, XrHJ3, XrHJ4, Fja1.step, Fja2.step, Fja3.step, Fja4.step)
    """

    """
    Hooke-Jeeves i Simplex na Fju 4 uz X = [5, 5]
    """
    #
    """
    X = [5, 5]
    Fja = functions.f4()

    XHJ = functions.Hooke_Jeeves(X, Fja)
    printHooke_Jeeves(XHJ, Fja.step)
    Fja.step = 0

    XS = functions.simplex(X, Fja, 1.0, 0.5, 2, 0.5, 1, 0.000001)
    printSimplex(XS, Fja.step)
    """

    """
    Simplex na Fji 1
    X = [0.5, 0.5], provedi s različitim koracima za generiranje simpleksa (npr 1 do 20)
    X = [20, 20], isto
    """
    #
    """
    X = [0.5, 0.5]
    Fja = functions.f1()
    for i in range(20):
        XS = functions.simplex(X, Fja, 1.0, 0.5, 2, 0.5, (i+1), 0.000001)
        printSimplex(XS, Fja.step)
        Fja.step = 0
    """

    """
    Primijeni jedan postupak optimizacije na Fju 6, 2D
    Više puta pokrenuti iz random točke iz [-50, 50]. 
    Može li se naći global ovako?
    Global min je otprilike manji od 0.0001
    """
    #
    """
    Fja = functions.f6()
    x = [0, 0]
    for i in range(100):
        x[0] = random.uniform(-50, 50)
        x[1] = random.uniform(-50, 50)
        print("-------------------------------------------------------------------------------")
        print("Točka iznosi [" + str(x[0]) + ", " + str(x[1]) + "].\n")
        zadatak6Racuni(x, Fja)
    """

    x = np.array([0.1, 0.3])
    fja = functions.f2()
    v1 = np.array([0.3, 0.6])
    v2 = np.array([-0.1, 0.7])
    
    minimum = functions.PowellMethod(x, fja, v1, v2)

    print("Tocka minimuma je " + str(minimum))
    print("Stvarni minimum je [4, 2]")
    print("Iznos funkcije u minimumu je " + str(fja.calculate(minimum)))
    print("Stvarni minimum funkcije je 0")

    print("\nDrugi nacin - putem dvije tocke\n")

    x1 = np.array([0.1, 0.3])
    x2 = np.array([-4.0, -1.0])
    vector = np.array([3, 0.3])

    minimum2 = functions.PowellMethod2Dots(x1, x2, fja, vector)

    print("Tocka minimuma je " + str(minimum2))
    print("Stvarni minimum je [4, 2]")
    print("Iznos funkcije u minimumu je " + str(fja.calculate(minimum2)))
    print("Stvarni minimum funkcije je 0")

    print("\n\nUsporedba dobivenih minimuma: \nMin1: " + str(minimum) + "\nMin2: " + str(minimum2) + "\nRazlika: " + str(minimum2 - minimum))

    


def zadatak6Racuni(x, Fja):
    XKooS = functions.searchByCoordinates(x, Fja, 0)
    printSearchByCoordinates(XKooS, Fja.step)
    Fja.step = 0
    XS = functions.simplex(x, Fja, 1.0, 0.5, 2, 0.5, 1, 0.000001)
    printSimplex(XS, Fja.step)
    Fja.step = 0
    XHJ = functions.Hooke_Jeeves(x, Fja)
    printHooke_Jeeves(XHJ, Fja.step)
    Fja.step = 0



#Printevi
def printGoldenRatio(Lrez, Rrez, iters):
    print("Rezultati algoritma zlatnog reda su:\n"
        "Lijeva granica: %f\n"
        "Desna granica: %f\n"
        "Broj iteracija: %i\n" % (Lrez[0], Rrez[0], iters))

def printSearchByCoordinates(KooSTocka, iters):
    print("Rezultati algoritma pretraživanja po koordinatama su:\n"
        "Točka u sustavu: ")
    for data in KooSTocka:
        sys.stdout.write('{:.3f} '.format(data))
    print("\n"
        "Broj iteracija: " + str(iters) + "\n")

def printSimplex(Xsimp, iters):
    print("Rezultati algoritma simplex postupka su:\n"
        "Simplex: ")
    for data in Xsimp:
        sys.stdout.write('{:.3f} '.format(data))
    print("\n"
        "Broj iteracija: " + str(iters) + "\n")
    
def printHooke_Jeeves(Xhj, iters):
    print("Rezultati Hooke-Jeeves postupka su:\n"
        "Točka: ")
    for data in Xhj:
        sys.stdout.write('{:.3f} '.format(data))
    print("\n"
        "Broj iteracija: " + str(iters) + "\n")

def printTablicno(text, x1, x2, x3, x4, i1, i2, i3, i4):
    print("\n" + text)
    print("\nTočke: ")
    printDot(x1)
    printDot(x2)
    printDot(x3)
    printDot(x4)
    print("\nIteracije: " + str(i1) + "  " + str(i2) + "  " + str(i3) + "  " + str(i4))

def printDot(x):
    for data in x:
        sys.stdout.write('{:.3f} '.format(data))
    print(" ")

if __name__ == "__main__":
    main()