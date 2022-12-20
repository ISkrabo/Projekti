import numpy as np
import math

###################
#  funkcija 1
###################

class f1(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        """ x = dot """
        self.step+=1
        return 100 * (x[1] - x[0]**2)**2 + (1 -x [0])**2

class g1(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        """ x = dot  
            return = new dot"""
        self.step+=1
        d1 = 400 * x[0] * (x[0]**2 - x[1]) + 2 * (x[0] - 1)
        d2 = 200 * (x[1] - x[0]**2)
        return [d1, d2]

class h1(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        """ x = dot  
            return = Hessian matrix"""
        self.step+=1
        d11 = 400 * (3 * x[0]**2 - x[1]) + 2
        d12 = -400 * (x[0])
        d21 = -400 * (x[0])
        d22 = 200
        return np.linalg.inv([[d11, d12],[d21,d22]]).tolist()

###################
#  funkcija 2
###################

class f2(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        """ x = dot """
        self.step+=1
        return (x[0] - 4)**2 + 4 * (x[1] - 2)**2

class g2(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        """ x = dot  
            return = new dot"""
        self.step+=1
        d1 = 2 * (x[0] - 4)
        d2 = 8 * (x[1] - 2)
        return [d1, d2]

class h2(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        """ x = dot  
            return = Hessian matrix"""
        self.step+=1
        d11 = 2
        d12 = 0
        d21 = 0
        d22 = 8
        return np.linalg.inv([[d11, d12],[d21,d22]]).tolist()

###################
#  funkcija 3
###################

class f3(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        """ x = dot """
        self.step+=1
        return (x[0] - 2)**2 + (x[1] + 3)**2

class g3(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        """ x = dot  
            return = new dot"""
        self.step+=1
        d1 = 2 * (x[0] - 2)
        d2 = 2 * (x[1] + 3)
        return [d1, d2]

###################
#  funkcija 4
###################

class f4(object):
    def __init__(self):
        self.step = 0

    def calculate(self, x):
        """ x = dot """
        self.step+=1
        return (x[0] - 3)**2 + x[1]**2

###################
#  funkcija zamjene
###################

class fz(object):
    def __init__(self, x, v, fja):
        self.x = x
        self.v = v
        self.step = 0
        self.fja = fja
    
    def calculate(self, t):
        self.step+=1
        val1 = self.x[0] + t[0] * self.v[0]
        val2 = self.x[1] + t[0] * self.v[1]
        val = [val1, val2]
        return self.fja.calculate(val)

###################
#  ogranicenja
###################

class restrictions(object):
    def __init__(self):
        self.listOfRestrictions = []

    def setForTask3(self):
        self.listOfRestrictions = [task3cond1, task3cond2, var1above100, var2above100, var1below100, var2below100]

    def setForTask4(self):
        self.listOfRestrictions = [task3cond1, task3cond2]

    def setForTask5(self):
        self.listOfRestrictions = [task5cond1, task5cond2]

    def validate(self, x0):
        for l in self.listOfRestrictions:
            if l(x0) < 0:
                return False
        return True

###################
#  ogranicenja - formule
###################
#G ogranicenja
def task3cond1(x):
    return x[1]-x[0]

def task3cond2(x):
    return 2-x[0]

def var1above100(x):
    return x[0]+100

def var2above100(x):
    return x[1]+100

def var1below100(x):
    return 100-x[0]

def var2below100(x):
    return 100-x[1]


def task5cond1(x):
    return 3-x[0]-x[1]

def task5cond2(x):
    return 3+1.5*x[0]-x[1]
#Ogranicenje koje je zadano ne kao >= vec kao =, H ogranicenje
def task5H(t, x):
    return t * (x[1] - 1)**2

###################
#  Deklaracija racunanja formule Transformacija u problem bez ogranicenja
###################

class transformedFunction(object):
    def __init__(self, fja, conds, t, h):
        self.fja = fja
        self.conds = conds
        self.t = t
        self.h = h

    def calculate(self, x):
        sum = 0
        if (self.h != None):
            sum += self.h(self.t, x)
        calc = 0
        for i in range(self.conds.__len__()):
            if (self.conds[i](x) <= 0):
                return float("inf")
            else:
                calc += math.log(self.conds[i](x))
        sum -= 1/self.t * calc
        return sum + self.fja.calculate(x)

    