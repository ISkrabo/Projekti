import main
import numpy as np
import random
import math
import sys

def zad1CalculateTruex1(t):
    return math.cos(t) + math.sin(t)

def zad1CalculateTruex2(t):
    return math.cos(t) - math.sin(t)

def euler(x0, A, B, T, tmax, mode):
    t = 0
    error = 0
    xNext = x0.copy()
    while (t <= tmax):
        if (mode == 1):
            Bn = np.dot(B, np.array([[1], [1]]))
        else:
            Bn = np.dot(B, np.array([[T], [T]]))
        t += T
        x = xNext.copy()
        #Euler
        xNext = x + T * (np.dot(A, x) + Bn)
        xTrue = [zad1CalculateTruex1(t), zad1CalculateTruex2(t)]
        error += (abs(xNext[0] - xTrue[0]) + abs(xNext[1] - xTrue[1]))
    return xNext, error
    #sys.stdout.write("%15s %10.3f %10.3f %10.3f\n" %("Euler:", xNext[0], xNext[1], error))

def backwardEuler(x0, A, B, T, tmax, mode):
    U = np.eye(2)
    #matrica za po formuli
    P = np.linalg.inv(U - A*T)
    t = 0
    error = 0
    xNext = x0.copy()
    while (t<= tmax):
        if (mode == 1):
            Bn = np.dot(B, np.array([[1], [1]]))
        else:
            Bn = np.dot(B, np.array([[T], [T]]))
        Q = np.dot(np.linalg.inv(U - A*T)*T, Bn)
        t += T
        x = xNext.copy()
        #backwards euler
        xNext = np.dot(P, x) + Q
        xTrue = [zad1CalculateTruex1(t), zad1CalculateTruex2(t)]
        error += (abs(xNext[0] - xTrue[0]) + abs(xNext[1] - xTrue[1]))
    return xNext, error
    #sys.stdout.write("%15s %10.3f %10.3f %10.3f\n" %("Obrnuti Euler:", xNext[0], xNext[1], error))

def trapez(x0, A, B, T, tmax, mode):
    U = np.eye(2)
    #matrica za po formuli
    R = np.dot(np.linalg.inv(U - A*T/2), (U + A*T/2))
    t = 0
    error = 0
    xNext = x0.copy()
    while (t<= tmax):
        if (mode == 1):
            Bn = np.dot(B, np.array([[1], [1]]))
        else:
            Bn = np.dot(B, np.array([[T], [T]]))
        S = np.dot(np.linalg.inv(U - A*T/2) * T/2, Bn)
        t += T
        x = xNext.copy()
        #trapez
        xNext = np.dot(R, x) + S
        xTrue = [zad1CalculateTruex1(t), zad1CalculateTruex2(t)]
        error += (abs(xNext[0] - xTrue[0]) + abs(xNext[1] - xTrue[1]))
    return xNext, error
    #sys.stdout.write("%15s %10.3f %10.3f %10.3f\n" %("Trapez:", xNext[0], xNext[1], error))

def RungeKutta4(x0, A, B, T, tmax, mode):
    t = 0
    error = 0
    xNext = x0.copy()
    while (t<= tmax):
        if (mode == 1):
            Bn = np.dot(B, np.array([[1], [1]]))
        else:
            Bn = np.dot(B, np.array([[T], [T]]))
        t += T
        x = xNext.copy()
        m1 = np.dot(A, x) + Bn
        m2 = np.dot(A, (x + (T/2) * m1)) + Bn
        m3 = np.dot(A, (x + (T/2) * m2)) + Bn
        m4 = np.dot(A, (x + T * m3)) + Bn
        xNext = x + T/6 * (m1 + 2*m2 + 2*m3 + m4)

        xTrue = [zad1CalculateTruex1(t), zad1CalculateTruex2(t)]
        error += (abs(xNext[0] - xTrue[0]) + abs(xNext[1] - xTrue[1]))
    return xNext, error
    #sys.stdout.write("%15s %10.3f %10.3f %10.8f\n" %("Runge-Kutta r4", xNext[0], xNext[1], error))

def PECE(x0, A, B, T, tmax, mode):
    #prediktor euler
    #korektor trapez
    t = 0
    error = 0
    xNext = x0.copy()
    while (t<= tmax):
        if (mode == 1):
            Bn = np.dot(B, np.array([[1], [1]]))
        else:
            Bn = np.dot(B, np.array([[T], [T]]))
        t += T
        x = xNext.copy()
        xNextPE = eulerJednom(x, A, Bn, T)
        xNext = trapezJednom(x, xNextPE, A, Bn, T)

        xTrue = [zad1CalculateTruex1(t), zad1CalculateTruex2(t)]
        error += (abs(xNext[0] - xTrue[0]) + abs(xNext[1] - xTrue[1]))
    return xNext, error

def PECECE(x0, A, B, T, tmax, mode):
    #prediktor euler
    #korektor obrnuti euler
    t = 0
    error = 0
    xNext = x0.copy()
    while (t<= tmax):
        if (mode == 1):
            Bn = np.dot(B, np.array([[1], [1]]))
        else:
            Bn = np.dot(B, np.array([[T], [T]]))
        t += T
        x = xNext.copy()
        xNextPE = eulerJednom(x, A, Bn, T)
        xNextCE = backwardEulerJednom(x, xNextPE, A, Bn, T)
        xNext = backwardEulerJednom(x, xNextCE, A, Bn, T)

        xTrue = [zad1CalculateTruex1(t), zad1CalculateTruex2(t)]
        error += (abs(xNext[0] - xTrue[0]) + abs(xNext[1] - xTrue[1]))
    return xNext, error

def eulerJednom(x0, A, Bn, T):
    return x0 + T * (np.dot(A, x0) + Bn)

def backwardEulerJednom(x0, xP, A, Bn, T):
    return x0 + T * np.dot(A, xP)

def trapezJednom(x0, xP, A, Bn, T):
    return x0 + T/2 * (np.dot(A, x0) + Bn + np.dot(A, xP))

if __name__ == "__main__":
    main.main()
