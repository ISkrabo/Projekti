import math

class f1(object):
    """init X = [-1.9, 2], minimum = [1, 1], F(min) = 0"""
    def __init__(self):
        self

    def calculate(self, x):
        """ x = dot """
        return 100 * (x[1] - x[0]**2)**2 + (1 -x[0])**2

class f3(object):
    """init X = NulVector, minimum = [1, 2, ..., n], F(min) = 0"""
    def __init__(self):
        self

    def calculate(self, x):
        """ x = dot """
        sum = 0
        n = x.__len__()
        for i in range(n):
            sum += math.pow((x[i] - (i + 1)), 2)
        return sum

class f6(object):
    """Global minimum = NulVector, F(min) = 0"""
    def __init__(self):
        self

    def calculate(self, x):
        """ x = dot """
        sumX = 0
        for i in range(x.__len__()):
            sumX += math.pow(x[i], 2)
        temp = math.pow(math.sin(math.sqrt(sumX)), 2)
        return (0.5 + ((temp - 0.5) / math.pow((1 + 0.001 * sumX), 2)))

class f7(object):
    """Global minimum = NulVector, F(min) = 0"""
    def __init__(self):
        self

    def calculate(self, x):
        """ x = dot """
        sumX = 0
        for i in range(x.__len__()):
            sumX += x[i]**2 
        return math.pow(sumX, 0.25) * (1 + math.pow(math.sin(50 * math.pow(sumX, 0.1)), 2))