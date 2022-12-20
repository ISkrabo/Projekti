import math
import numpy as np
import declarations
import random

#Definiranje golden ratio algoritma
k = 0.5 * (math.sqrt(5) - 1)
def goldenRatio(x, i, e, function):
    """L i R se izracunavaju u funkciji.

    x = pocetna tocka  
    i = element pretraživanja u X  
    e = preciznost (0 za automatsko postavljanje)  
    function = funkcija nad kojom se racuna min
    
    return: L i R granice intervala, step broj koliko je puta racunata funkcija"""

    L, R = unimodalInterval(1, x, function, i)

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
        while(True):
            l = m.copy()
            m = r.copy()
            fm = fr
            step *= 2
            r[i] = dot[i] + h * step
            fr = function.calculate(r)
            if (fm < fr):
                break
    else:
        while (True):
            r = m.copy()
            m = l.copy()
            fm = fl
            step *= 2
            l[i] = dot[i] - h * step
            fl = function.calculate(l)
            if(fm < fl):
                break
    
    return l, r

def gradient_descent(x, fja, grad, e, useGR):
    if (e == 0):
        e = 1e-6
    x0 = x.copy()
    old = fja.calculate(x0)
    curr = old
    counter = 0
    gr = grad.calculate(x0)
    sum = getEuclid(gr)
    while(sum > e):
        #check loop
        if (curr != old):
            counter = 0
        else: 
            counter+=1
        if (counter > 100):
            print("Funkcija divergira. Zaustavljanje algoritma.")
            return x
        
        v = gr.copy()
        v[0] *= -1
        v[1] *= -1
        lambd = 1
        
        if (useGR):
            fz = declarations.fz(x0, v, fja)
            L = [0.0]
            GR = goldenRatio(L, 0, 0, fz)
            fja.step += fz.step
            lambd = (GR[0][0] + GR[1][0]) / 2
        
        x0[0] += lambd * v[0]
        x0[1] += lambd * v[1]

        old = curr
        curr = fja.calculate(x0)
        gr = grad.calculate(x0)
        sum = getEuclid(gr)
    return x0
        
def getEuclid(dot):
    sum = 0.0
    for i in range(dot.__len__()):
        sum += (dot[i]**2)
    return math.sqrt(sum)

def newton_raphson(x, fja, grad, hess, e, useGR):
    if (e == 0):
        e = 1e-6
    x0 = x.copy()
    old = fja.calculate(x0)
    curr = old
    counter = 0

    gr = np.array(grad.calculate(x0))
    hs = np.array(hess.calculate(x0))
    shift = np.dot(hs, gr)

    sum = getEuclid(shift)
    while(sum > e):
        #check loop
        if (curr != old):
            counter = 0
        else: 
            counter+=1
        if (counter > 100):
            print("Funkcija divergira. Zaustavljanje algoritma.")
            return x

        gr = np.array(grad.calculate(x0))
        hs = np.array(hess.calculate(x0))
        shift = np.dot(hs, gr)

        v = shift.copy()
        v[0] *= -1
        v[1] *= -1
        lambd = 1
        
        if (useGR):
            fz = declarations.fz(x0, v, fja)
            L = [0.0]
            GR = goldenRatio(L, 0, 0, fz)
            fja.step += fz.step
            lambd = (GR[0][0] + GR[1][0]) / 2
        
        x0[0] += lambd * v[0]
        x0[1] += lambd * v[1]
        
        old = curr
        curr = fja.calculate(x0)

        sum = getEuclid(shift)
    return x0

def boxAlgorithm(x, fja, conds, bor, e, alpha):
    if (e == 0):
        e = 1e-6
    if (alpha == 0):
        alpha = 1.3
    x0 = x.copy()

    if not (conds.validate(x0)):
        print("ERROR")
    
    xc = x.copy()
    n = x0.__len__()
    xs = []

    for i in range(2*n):
        xs.append(x0.copy())
    for t in range(2*n):
        for i in range(n):
            r = random.random()
            xs[t][i] = bor[0] + r * (bor[1] - bor[0])
        while not (conds.validate(xs[t])):
            xs[t] = (0.5 * (np.array(xs[t]) + np.array(xc))).tolist()
        xc = simplexFindCentroid(xs, -1)

    old = fja.calculate(xc)
    curr = old
    counter = 0
    while(True):
        #check loop
        if (curr != old):
            counter = 0
        else: 
            counter+=1
        if (counter > 100):
            print("Funkcija divergira. Zaustavljanje algoritma.")
            return xc

        h1 = getWorst(fja, xs, -1)
        h2 = getWorst(fja, xs, h1)
        xc = simplexFindCentroid(xs, h1)
        xr = simplexReflection(xc, xs[h1], alpha)

        for i in range(n):
            if (xr[i] < bor[0]):
                xr[i] = bor[0]
            elif (xr[i] > bor[1]):
                xr[i] = bor[1]
        
        while not (conds.validate(xr)):
            xr = (0.5 * (np.array(xr) + np.array(xc))).tolist()
        if (fja.calculate(xr) > fja.calculate(xs[h2])):
            xr = (0.5 * (np.array(xr) + np.array(xc))).tolist()

        xs[h1] = xr
        old = curr
        curr = fja.calculate(xc)

        if (boxStopCondition(fja, xs, xc) <= e):
            return xc

def getWorst(fja, xs, h):
    worst = -1
    for i in range(xs.__len__()):
        if (i == h):
            continue
        if (worst == -1):
            worst = i
            worstValue = fja.calculate(xs[i])
        else:
            if (fja.calculate(xs[i]) > worstValue):
                worst = i
                worstValue = fja.calculate(xs[i])
    return worst

def boxStopCondition(fja, xs, xc):
    sum = 0.0
    for i in range(xs.__len__()):
        sum += (fja.calculate(xs[i]) - fja.calculate(xc))**2
    return math.sqrt(sum / float(xs.__len__()))

def simplexFindCentroid(simpleks, h):
    n = simpleks.__len__()
    if (h >= 0):
        n-=1
    for i in range(simpleks.__len__()):
            if (i == h): 
                continue
            if 'centroid' not in locals():
                centroid = simpleks[i].copy()
            else:
                for j in range(centroid.__len__()):
                    centroid[j] += simpleks[i][j]
    for i in range(centroid.__len__()):
        centroid[i] /= n
    return centroid

def simplexReflection(centroid, xHigh, alfa):
    Xr = centroid.copy()
    for i in range(Xr.__len__()):
        Xr[i] = (Xr[i] * (1 + alfa) - alfa * xHigh[i])
    return Xr

def transformIntoProblem(x, fja, conds, t, e, h):
    if (e == 0):
        e = 1e-5
    if (t == 0):
        t = 1
    Tfja = declarations.transformedFunction(fja, conds, t, h) 

    x0 = x.copy()
    while True:
        old = x0.copy()
        curr = Hooke_Jeeves(x0, Tfja)

        Tfja.t *= 10
        x0 = curr.copy()

        if transformedCheckStop(old, curr, e):
            return curr, int(math.log(Tfja.t, 10) + 1)


def transformedCheckStop(old, curr, e):
    for i in range(old.__len__()):
        if abs(old[i] - curr[i]) > e:
            return False
    return True

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
    Dx = 0.5
    eps = 1e-5
    n = x.__len__()

    xB = x.copy()
    xP = x.copy()
    while(True):
        xN = research(xP, Dx, Fja, n)
        if (Fja.calculate(xN) < Fja.calculate(xB)):
            for j in range(n):
                xP[j] = 2 * xN[j] - xB[j]
            xB = xN
        else:
            Dx*= 0.5
            xP = xB
        if (Dx <= eps):
            return xB

def research(xP, Dx, Fja, n):
    x = xP.copy()
    for i in range(n):
        P = Fja.calculate(x)
        x[i] += Dx
        N = Fja.calculate(x)
        if (N > P):
            x[i] -= 2*Dx
            N = Fja.calculate(x)
            if (N > P):
                x[i] += Dx
    return x