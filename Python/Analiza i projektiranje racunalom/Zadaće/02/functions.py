import math
import numpy as np

#Definiranje obicnih funkcija
class f1(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        self.step+=1
        return (100 * math.pow((x[1] - math.pow(x[0], 2)), 2) + math.pow((1 - x[0]), 2))

class f2(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        self.step+=1
        return (math.pow((x[0] - 4), 2) + 4 * math.pow((x[1] - 2), 2))

class f3(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        self.step+=1
        sum = 0
        n = x.__len__()
        for i in range(n):
            sum += math.pow((x[i] - (i + 1)), 2)
        return sum

class f4(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        self.step+=1
        return abs((x[0] - x[1]) * (x[0] + x[1])) + math.sqrt(math.pow(x[0], 2) + math.pow(x[1], 2))

class f5(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        self.step+=1
        sum = 0
        n = x.__len__()
        for i in range(n):
            sum += math.pow(x[i], 2)
        return 0.5 * (math.pow(math.sin(math.sqrt(sum) - 0.5), 2) / math.pow((1 + 0.001 * sum), 2))

class f6(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        self.step+=1
        sumX = 0
        for i in range(x.__len__()):
            sumX += math.pow(x[i], 2)
        return 0.5 + ((math.pow((math.sin(math.sqrt(sumX))), 2) - 0.5) / (1 + 0.0001 * sumX))

class fprvizadatak(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        self.step+=1
        return math.pow((x[0] - 3), 2)


#Definiranje golden ratio algoritma
k = 0.5 * (math.sqrt(5) - 1)
def goldenRatio(x, i, e, function):
    """L i R se izracunavaju u funkciji.

    x = pocetna tocka  
    i = element pretrazivanja u X  
    e = preciznost (0 za automatsko postavljanje)  
    function = funkcija nad kojom se racuna min
    
    return: L i R granice intervala, step broj koliko je puta racunata funkcija"""

    L, R = unimodalInterval(0, x, function, i)

    #if interval nije predan racunaj unimodalni else preskoci

    if (e == 0):
        e = 1e-6
    
    c = R.copy()
    d = L.copy()
    c[i] -= k * (R[i] - L[i])
    d[i] += k * (R[i] - L[i])
    fc = function.calculate(c)
    fd = function.calculate(d)

    diff = R[i] - L[i]

    while (diff > e):
        if (fc < fd):
            R = d.copy()
            d = c.copy()
            c = R.copy()
            c[i] -= k * (R[i] - L[i])
            fd = fc
            fc = function.calculate(c)
        else:
            L = c.copy()
            c = d.copy()
            d = L.copy() 
            d[i] += k * (R[i] - L[i])
            fc = fd
            fd = function.calculate(d)
        diff = R[i] - L[i]
    return L, R

#Definiranje algoritma unimodalnog intervala
def unimodalInterval(h, dot, function, i):
    """h = vrijednost pomaka u pretrazivanju (0 za automatsko postavljanje  
    dot = jedna vrijednost tocke / komponenta  
    function = funkcija nad kojom se racuna
    
    return: L i R granice intervala"""
    if (h == 0):
        h = 0.000001
    l = dot.copy()
    r = dot.copy()
    l[i] -= h
    r[i] += h
    m = dot.copy()
    step = 1

    fm = function.calculate(dot)
    fl = function.calculate(l)
    fr = function.calculate(r)

    if (fm < fr and fm < fl):
        return l, r
    elif (fm > fr):
        while(fm > fr):
            l = m.copy()
            m = r.copy()
            fm = fr
            step *= 2
            r[i] = dot[i] + h * step
            fr = function.calculate(r)
    else:
        while (fm > fl):
            r = m.copy()
            m = l.copy()
            fm = fl
            step *= 2
            l[i] = dot[i] - h * step
            fl = function.calculate(l)
    
    return l, r

#Definiranje algoritma pretrazivanja po koordinatama
def searchByCoordinates(x0, Fja, eps):
    """x0 = vektor pocetne tocke  
    Fja = funkcija nad kojom se trazi minimum  
    eps = preciznost
    
    return: X, iteracije"""
    x = x0.copy()
    if (eps == 0):
        eps = 1e-6
    n = x.__len__()
    stopCondition = False
    while True:
        xS = x.copy()
        for i in range(n):
            GR = goldenRatio(x, i, 0, Fja)
            newValue = (GR[0][i] + GR[1][i]) / 2
            oldValue = xS[i]
            x[i] = newValue
            if (abs(newValue - oldValue) <= eps):
                stopCondition = True
        if (stopCondition):
            break
    return x

#Definiranje simplex algoritma po Nelderu i Meadu
def simplex(x0, function, alfa, beta, gamma, sigma, h, eps):
    """x0 = pocetna tocka  
    function = funkcija nad kojom se racuna  
    alfa = u racunanju refleksije  
    beta = u racunanju kontrakcije  
    gamma = u racunanju ekspanzije  
    sigma = za pomicanje svih u simpleksu  
    h = step  
    h, eps = 0 za automatsko

    return: Xsimplex, iteracije
    """
    if (h == 0):
        h = 1
    if (eps == 0):
        eps = 1e-6
    #Izracunaj tocke simpleksa
    simpleks = []
    simpleks.append(x0)
    n = x0.__len__()
    for i in range(n):
        temp = x0.copy()
        temp[i] += h
        simpleks.append(temp)

    while(True):
        #Odredi indekse H, L, koji su max i min funkcije
        h, l = findHighAndLow(simpleks, function)
        #Odredi centroid Xc
        centroid = []
        simplexFindCentroid(simpleks, centroid, h, n)
        #Izracunaj refleksiju
        Xr = simplexReflection(centroid[0], simpleks[h], alfa)
        
        #If
        if (function.calculate(Xr) < function.calculate(simpleks[l])):
            #Ekspanzija
            Xe = simplexExpansion(centroid[0], Xr, gamma)
            if (function.calculate(Xe) < function.calculate(simpleks[l])):
                simpleks[h] = Xe
            else:
                simpleks[h] = Xr
        #Else
        else:
            #provjera je li F(Xr) > F(X[j]) za svaki j (osim H)
            isWorst = True
            fXr = function.calculate(Xr)
            for i in range(simpleks.__len__()):
                if (i == h):
                    continue
                if (fXr < function.calculate(simpleks[i])):
                    isWorst = False
                    break
            
            #IF-anje tog gore uvjeta
            if(isWorst):
                if(fXr < function.calculate(simpleks[h])):
                    simpleks[h] = Xr
                Xk = simplexContraction(centroid[0], simpleks[h], beta)
                if (function.calculate(Xk) < function.calculate(simpleks[h])):
                    simpleks[h] = Xk
                else:
                    #Pomakni sve tocke prema X[l]
                    simplexMoveAll(simpleks, sigma, l)
            #Else
            else:
                simpleks[h] = Xr
        #dok nije zavodoljen uvjet zaustavljanja
        if (simplexCheckStop(simpleks, eps, function, h, x0)):
            break
    centroid = []
    simplexFindCentroid(simpleks, centroid, h, n)
    return centroid[0]

def findHighAndLow(simpleks, function):
    h = 0
    l = 0
    fh = function.calculate(simpleks[h])
    fl = function.calculate(simpleks[l])
    for i in range(simpleks.__len__()):
        fi = function.calculate(simpleks[i])
        if (fi > fh):
            h = i
            fh = function.calculate(simpleks[h])
        if (fi < fl):
            l = i
            fl = function.calculate(simpleks[l])
    return h, l

def simplexFindCentroid(simpleks, centroid, h, n):
    for i in range(simpleks.__len__()):
            if (i == h): 
                continue
            if (centroid.__len__() == 0):
                centroid.append(simpleks[i].copy())
            else:
                for j in range(n):
                    centroid[0][j] += simpleks[i][j]
    for i in range(centroid[0].__len__()):
        centroid[0][i] /= n

def simplexReflection(centroid, xHigh, alfa):
    Xr = centroid.copy()
    for i in range(Xr.__len__()):
        Xr[i] = (Xr[i] * (1 + alfa) - alfa * xHigh[i])
    return Xr

def simplexExpansion(centroid, Xr, gamma):
    Xe = centroid.copy()
    for i in range(Xe.__len__()):
        Xe[i] = (Xe[i] * (1 - gamma) + gamma * Xr[i])
    return Xe

def simplexContraction(centroid, xHigh, beta):
    Xk = centroid.copy()
    for i in range(Xk.__len__()):
        Xk[i] = (Xk[i] * (1 - beta) + beta * xHigh[i])
    return Xk

def simplexMoveAll(simpleks, sigma, l):
    Xl = simpleks[l].copy()
    for i in range(simpleks.__len__()):
        if (i == l):
            continue
        for j in range(Xl.__len__()):
            simpleks[i][j] += Xl[j]
            simpleks[i][j] *= sigma
    return

def simplexCheckStop(simpleks, eps, function, h, x0):
    temp = 0.0
    centroid = []
    simplexFindCentroid(simpleks, centroid, h, x0.__len__())
    Fc = function.calculate(centroid[0])
    for i in range(simpleks.__len__()):
        value = function.calculate(simpleks[i])
        temp += math.pow((Fc - value), 2)
    temp /= simpleks.__len__()
    temp = math.sqrt(temp)
    if (temp < eps):
        return True
    return False

#Definiranje Hooke-Jeeves algoritma
def Hooke_Jeeves(x, Fja):
    """Hooke-Jeeves postupak.

    x - pocetna tocka  
    Fja - funkcija nad kojom trazimo  
    xB - bazna tocka  
    xP - pocetna tocka pretrazivanja  
    xN - tocka dobivena pretrazivanjem  

    vraca xB i broj iteracija
    """
    Dx = 1
    eps = 1e-6
    n = x.__len__()

    xB = x.copy()
    xP = x.copy()
    while(True):
        xN = research(xP, Dx, Fja, n)
        if (Fja.calculate(xN) < Fja.calculate(xB)):
            for j in range(n):
                xP[j] = 2 * xN[j] - xB[j]
            xB = xN.copy()
        else:
            Dx*= 0.5
            xP = xB.copy()
        if (Dx <= eps):
            break

    return xB

def research(xP, Dx, Fja, n):
    x = xP.copy()
    for i in range(n):
        P = Fja.calculate(xP)
        x[i] += Dx
        N = Fja.calculate(x)
        if (N > P):
            x[i] -= 2*Dx
            N = Fja.calculate(x)
            if (N > P):
                x[i] += Dx
    return x



def PowellMethod(x0, fja, v1, v2):

    #odaberi pocetni x0 i dva vektora
    #iz x0 napravi 1D optimizaciju niz vektor v1 do ekstrema x1
    #iz x1 napravi 1D optimizaciju niz vektor v2 do ekstrema x2
    #izracunaj v3 kao (x2 - x0) (i odbaci v1)

    #iz x2 napravi .... v3 do x3
    #iz x3 napravi .... v2 do x4
    #iz x4 napravi .... v3 do x5
    #izracunaj v4 kao (x5 - x3)

    #iz x5 napravi .... v4 do konacnog ekstrema (ako je fja kvadratna doci cemo tocno u ekstrem,
    #                                           inace dolazimo u vrijednost jako blizu ekstremu)


    #pomocu unimodalnog postupka pronaci optimalni lambda za v1

    #GoldenRatioVector ponajprije izracuna unimodalni interval za x0 u smjeru v1
    #Zatim racuna po golden ratio funkciji minimum funkcije za tocku (x0 + k+v1) (tj. trazi optimalni k)
    x1 = goldenRatioVector(x0, 0, fja, v1)
    x2 = goldenRatioVector(x1, 0, fja, v2)
    v3 = x2 - x0 

    x3 = goldenRatioVector(x2, 0, fja, v3)
    x4 = goldenRatioVector(x3, 0, fja, v2)
    x5 = goldenRatioVector(x4, 0, fja, v3)
    v4 = x5 - x3
    
    extreme = goldenRatioVector(x5, 0, fja, v4)

    return extreme

#Definiranje algoritma unimodalnog intervala
def unimodalIntervalVector(h, x0, function, vector):
    """h = vrijednost pomaka u pretrazivanju (0 za automatsko postavljanje  )
    x0 = jedna vrijednost tocke / komponenta  
    function = funkcija nad kojom se racuna
    
    return: L i R granice intervala"""
    if (h == 0):
        h = 0.000001
    l = x0.copy()
    r = x0.copy()
    l -= h * vector
    r += h * vector
    
    m = x0.copy()
    step = 1

    fm = function.calculate(x0)
    fl = function.calculate(l)
    fr = function.calculate(r)

    if (fm < fr and fm < fl):
        return l, r
    elif (fm > fr):
        while(fm > fr):
            l = m.copy()
            m = r.copy()
            fm = fr
            step *= 2
            r = x0 + h * step * vector
            fr = function.calculate(r)
    else:
        while (fm > fl):
            r = m.copy()
            m = l.copy()
            fm = fl
            step *= 2
            l = x0 - h * step * vector
            fl = function.calculate(l)
    
    return l, r
    
def goldenRatioVector(x0, e, function, v1):
    """L i R se izracunavaju u funkciji.

    x = pocetna tocka  
    v1 = vektor
    e = preciznost (0 za automatsko postavljanje)  
    function = funkcija nad kojom se racuna min
    
    return: L i R granice intervala, step broj koliko je puta racunata funkcija"""

    L, R = unimodalIntervalVector(0, x0, function, v1)

    #if interval nije predan racunaj unimodalni else preskoci

    if (e == 0):
        e = 1e-6
    
    c = R.copy()
    d = L.copy()
    c -= k * (R - L)
    d += k * (R - L)
    fc = function.calculate(c)
    fd = function.calculate(d)

    diff = np.abs(R[0] - L[0]) + np.abs(R[1] - L[1])

    while (diff > e):
        if (fc < fd):
            R = d.copy()
            d = c.copy()
            c = R.copy()
            c -= k * (R - L)
            fd = fc
            fc = function.calculate(c)
        else:
            L = c.copy()
            c = d.copy()
            d = L.copy() 
            d += k * (R - L)
            fc = fd
            fd = function.calculate(d)
        diff = np.abs(R[0] - L[0]) + np.abs(R[1] - L[1])
    return (L + R) / 2

def PowellMethod2Dots(x1, x2, fja, vector):
    x3 = goldenRatioVector(x1, 0, fja, vector)
    x4 = goldenRatioVector(x2, 0, fja, vector)
    direction = (x3 - x4)
    
    extreme = goldenRatioVector(x3, 0, fja, direction)

    return extreme