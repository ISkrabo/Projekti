from copy import copy, deepcopy

epsilon = 0.000001

class mm(object):
    def __init__(self, rows, columns):
        #create a list containing (ROWS) lists, each with (COLUMNS) elements, all set to 0
        self.numbers = [[0 for x in range(columns)] for y in range(rows)] 
        self.rows = rows
        self.columns = columns

    def __resize__(self, newRows, newColumns):
        temp = [[0 for x in range(newColumns)] for y in range(newRows)] 
        maxRow = min(self.rows, newRows)
        maxColumns = min(self.columns, newColumns)
        for i in range(maxRow):
            for j in range(maxColumns):
                temp[i][j] = self.numbers[i][j]
        self.numbers = temp

    def __readFromFile__(self, fileName):
        f = open(fileName, "r")
        matrix = []
        contents = f.readline()
        self.rows = 0
        
        while contents:
            self.rows +=1
            contents = contents.split()
            contents = [float(i) for i in contents]
            matrix.append(contents)
            contents = f.readline()

        f.close()
        self.numbers = matrix
        self.columns = self.numbers[0].__len__()
        return self

    def __print__(self):
        for x in range(self.rows):
            print (self.numbers[x])
        return

    def __getitem__(self, number):
        return self.numbers[number]

    def __setitem__(self, number, value):
        i, j = number
        self.numbers[i][j] = value
        return self

    def __add__(self, other):
        if (isinstance(other, mm)):
            for i in range(self.rows):
                for j in range(self.columns):
                    self.numbers[i][j] += other.numbers[i][j]
        else:
            matrix = []
            for i in range(self.rows):
                row = []
                for j in range(self.columns):
                    row.append(self.numbers[i][j] + other)
                matrix.append(row)
            self.numbers = matrix

        return self

    def __sub__(self, other):
        if (isinstance(other, mm)):
            for i in range(other.rows):
                other.numbers[i] = [-1*x for x in other.numbers[i]]
            return self.__add__(other)
        else:
            return self.__add__(-other)
            

    def __mul__(self, other):
        for i in range(self.rows):
            for j in range(self.columns):
                self.numbers[i][j] *= other
        return self

    def __invert__(self):
        matrix = []
        for j in range(self.columns):
            row = []
            for i in range(self.rows):
                row.append(self.numbers[i][j])
            matrix.append(row)
        self.numbers = matrix
        return self

    def __eq__(self, other):
        x = 0
        if (self.rows == other.rows):
            if (self.columns == other.columns):
                while True:
                    for i in range(self.rows):
                        for j in range(self.columns):
                            if (self.numbers[i][j] != other.numbers[i][j]):
                                x = -1
                    if (x == -1): 
                        break
                    return True
        return False

    def __swapRows__(self, first, second):
        secondRow = self.numbers[second]
        self.numbers[second] = self.numbers[first]
        self.numbers[first] = secondRow

    def copy(self, matA):
        for i in range(matA.rows):
            for j in range(matA.columns):
                self[i][j] = matA[i][j]

    def unixMatrix(self, size):
        mat = mm(size, size)
        for i in range(size):
            mat[i][i] = 1
        return mat      

#Self methods
def matrixMultiply(matA, matB):
    matC = mm(matA.rows, matB.columns)
    for i in range(matA.rows):
        for j in range(matB.columns):
            for k in range(matA.columns):
                matC[i][j] += matA[i][k]*matB[k][j]
    
    return matC

def LUDecompose(matA):
    matP = mm(3, 3)
    matP = matP.unixMatrix(matA.rows)
    matLU = mm(matA.rows, matA.columns)
    matLU.copy(matA)

    for i in range(matLU.rows):
        #dohvacanje pivota i provjera vrijednosti
        pivot = matLU[i][i]
        if (pivot == 0.0 or abs(pivot) < epsilon):
            print("Error! Prekid rada; stozerni element je 0!")
            return matLU, matP
        #daljnje racunanje
        for j in range(i+1, matLU.rows):
            element = matLU[0][i]
            if (element == 0.0 or abs(element) < epsilon):
                element = 0.0
            else:
                element = matLU[j][i] / matLU[i][i]
            matLU[j][i] = element
            for k in range(i+1, matLU.rows):
                element = matLU[j][k] - matLU[j][i] * matLU[i][k]
                matLU[j][k] = element

    return matLU, matP

def LUPDecompose(matA):
    matP = mm(3, 3)
    matP = matP.unixMatrix(matA.rows)
    matLU = mm(matA.rows, matA.columns)
    matLU.copy(matA)

    for i in range(matLU.rows):
        #pivotiranje - pronalazak najveceg
        matLU, matP = pivoteAround(matLU, matP, i)

        #dohvacanje pivota i provjera vrijednosti
        pivot = matLU[i][i]
        if (pivot == 0.0 or abs(pivot) < epsilon):
            print("Error! Prekid rada; stozerni element je 0!")
            return matLU, matP
        #daljnje racunanje
        for j in range(i+1, matLU.rows):
            element = matLU[0][i]
            if (element == 0.0 or abs(element) < epsilon):
                element = 0.0
            else:
                element = matLU[j][i] / matLU[i][i]
            matLU[j][i] = element
            for k in range(i+1, matLU.rows):
                element = matLU[j][k] - matLU[j][i] * matLU[i][k]
                matLU[j][k] = element

    return matLU, matP

def supstituteForwards(matLU, matP, matB):
    matY = mm(3, 3)
    matY = matrixMultiply(matP, matB)
    for i in range(matLU.rows):
        for j in range(i+1, matLU.rows):
            element = matY[j][0] - matLU[j][i] * matY[i][0]
            matY[j][0] = element
    return matY

def supstituteBackwards(matLU, matY):
    for i in range(matLU.rows-1, -1, -1):
        pivot = matLU[i][i]
        if (pivot == 0.0 or abs(pivot) < epsilon):
            print("Error! Prekid rada; stozerni element je 0!")
            return matY
        element = matY[i][0]
        if (element == 0.0 or abs(element) < epsilon):
            element = 0.0
        else:
            element = matY[i][0] / matLU[i][i]
        matY[i][0] = element
        for j in range(i):
            element = matY[j][0] - matLU[j][i] * matY[i][0]
            matY[j][0] = element
    return matY

def pivoteAround(matLU, matP, index):
    maxIndex = index
    maxValue = abs(matLU[index][index])

    for i in range (index+1, matLU.rows):
        value = abs(matLU[i][index])
        if (value > maxValue):
            maxValue = value
            maxIndex = i

    if (maxIndex != index):
        matLU.__swapRows__(index, maxIndex)
        matP.__swapRows__(index, maxIndex)
        print("Zamijenjeni su redovi " + str(index) + " i " + str(maxIndex))

    return matLU, matP

# Mnozenje istih redova u obje matrice; ne mijenja konačni rezultat. 
# Kod gleda da li se brojevi u redu mogu podijeliti ili pomnoziti s 10.
def matrixAnalyze(matA, matB):
    for i in range(matA.rows):
        while (matA[i][0] % 10 == 0 and matB[i][0] % 10 == 0):
            for j in range(matA.columns):
                matA[i][j] /= 10
            matB.numbers[i][0] /= 10
        while(matA[i][0] * 10 < 10 and matB[i][0] * 10 < 10):
            for j in range(matA.columns):
                matA[i][j] *= 10
            matB.numbers[i][0] *= 10
    return matA, matB

def matrixInversion(matLU, matP):
    #izracunaj supstforw i back za 100, 010, 001
    matAinv = mm(3, 3)
    for i in range(matLU.rows):
        matB = mm(3, 1)
        matB.numbers[i][0] = 1.0
        matY = supstituteForwards(matLU, matP, matB)
        matX = supstituteBackwards(matLU, matY)
        for j in range(matLU.rows):
            matAinv[j][i] = matX[j][0]
    return matAinv

def matrixDeterminant(matLU):
    determinant = 1
    for i in range(matLU.rows):
        element = matLU[i][i]
        if (element == 0.0 or abs(element) < epsilon):
            return 0.0
        determinant *= matLU[i][i]
    return determinant