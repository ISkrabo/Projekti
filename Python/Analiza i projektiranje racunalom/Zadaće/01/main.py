import myMatrix

"""matA = myMatrix.mm(5, 3)
matB = myMatrix.mm(5, 3)

print (matA == matB)

matA.numbers[0][0] = 3
matB.numbers[1][2] = 6

#matA.__resize__(6, 4)

matA[1, 2] = 4

matA += 3
matA = matA + matB
#matA = matB

matA -= matB
matA *= 3

matA = ~matA"""

#   deklariranje praznih matrica za zadatke
matA = myMatrix.mm(3, 3)
matB = myMatrix.mm(3, 1)

#   Zadatci 2-6 - racunanje LU/LUP dekompozicije
#   Zad 2 
matA.__readFromFile__("zad2m1.txt")
matB.__readFromFile__("zad2m2.txt")
#   Zad 3
#matA.__readFromFile__("zad3m1.txt")
#matB.__readFromFile__("zad3m2.txt")
#   Zad 4
#matA.__readFromFile__("zad4m1.txt")
#matB.__readFromFile__("zad4m2.txt")
#   Zad 5
#matA.__readFromFile__("zad5m1.txt")
#matB.__readFromFile__("zad5m2.txt")
#   Zad 6 
#matA.__readFromFile__("zad6m1.txt")
#matB.__readFromFile__("zad6m2.txt")
#matA, matB = myMatrix.matrixAnalyze(matA, matB)

#   Zad 7-10 - racunanje inverza/determinante
#   Zad 7 (inverz)
#matA.__readFromFile__("zad7m.txt")
#   Zad 8 (inverz)
#matA.__readFromFile__("zad8m.txt")
#   zad 9 (determinanta)
#matA.__readFromFile__("zad9m.txt")
#   zad 10 (determinanta)
#matA.__readFromFile__("zad10m.txt")

#   Racunanje determinante i inverza matrice
"""
matLU, matP = myMatrix.LUPDecompose(matA)
determinant = myMatrix.matrixDeterminant(matLU)
if (determinant == 0):
    print("\nDeterminanta je 0, inverz ne postoji!")
else:
    print("\nDeterminanta iznosi " + str(determinant))
    matAinv = myMatrix.matrixInversion(matLU, matP)
    print("\nInverz matrice je ")
    matAinv.__print__()
"""
#   Racunanje LU i LUP dekompozicija

print("\nMatrica A")
matA.__print__()
print("\nMatrica B")
matB.__print__()
print()
#LU dekompozicija
matLU, matP = myMatrix.LUDecompose(matA)
#ispis LU i P
print("\nMatrica LU")
matLU.__print__()
print("\nMatrica P")
matP.__print__()
#ispis Y
matY = myMatrix.supstituteForwards(matLU, matP, matB)
print("\nMatrica Y")
matY.__print__()
#ispis X
matX = myMatrix.supstituteBackwards(matLU, matY)
print("\nMatrica X")
matX.__print__()

#LUP dekompozicija
matLU, matP = myMatrix.LUPDecompose(matA)
#ispis LU i P
print("\nMatrica LU")
matLU.__print__()
print("\nMatrica P")
matP.__print__()
#ispis Y
matY = myMatrix.supstituteForwards(matLU, matP, matB)
print("\nMatrica Y")
matY.__print__()
#ispis X
matX = myMatrix.supstituteBackwards(matLU, matY)
print("\nMatrica X")
matX.__print__()

print("\nKraj.")