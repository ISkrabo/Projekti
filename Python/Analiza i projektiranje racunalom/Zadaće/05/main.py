import functions
import numpy as np
import sys

def main():
    
    #zadatak 1
    
    print()
    sys.stdout.write("\u0332".join("%15s|%10s|%10s|%10s\n" %("Metoda", "x", "y", "err")))
    A = np.array([[0, 1], [-1, 0]])
    x0 = np.array([[1], [1]])
    B = np.array([[0, 0], [0, 0]])
    T = 0.01
    tmax = 10

    final, error = functions.euler(x0, A, B, T, tmax, 1)
    printResult("Euler", final, error)

    final, error = functions.backwardEuler(x0, A, B, T, tmax, 1)
    printResult("Obrnuti Euler", final, error)

    final, error = functions.trapez(x0, A, B, T, tmax, 1)
    printResult("Trapez", final, error)
    
    final, error = functions.RungeKutta4(x0, A, B, T, tmax, 1)
    printResult("Runge-Kutta r4", final, error)
    
    final, error = functions.PECE(x0, A, B, T, tmax, 1)
    printResult("PECE (E, T)", final, error)

    final, error = functions.PECECE(x0, A, B, T, tmax, 1)
    printResult("PE(CE)^2 (E OE)", final, error)
    
    #zadatak 2
    
    print()
    sys.stdout.write("\u0332".join("%15s|%10s|%10s\n" %("Metoda", "x", "y")))
    A = np.array([[0, 1], [-200, -102]])
    x0 = np.array([[1], [-2]])
    B = np.array([[0, 0], [0, 0]])
    T = 0.1
    tmax = 1

    final, error = functions.euler(x0, A, B, T, tmax, 1)
    printResult("Euler", final, None)

    final, error = functions.backwardEuler(x0, A, B, T, tmax, 1)
    printResult("Obrnuti Euler", final, None)

    final, error = functions.trapez(x0, A, B, T, tmax, 1)
    printResult("Trapez", final, None)
    
    final, error = functions.RungeKutta4(x0, A, B, T, tmax, 1)
    printResult("Runge-Kutta r4", final, None)

    final, error = functions.PECE(x0, A, B, T, tmax, 1)
    printResult("PECE (E, T)", final, None)

    final, error = functions.PECECE(x0, A, B, T, tmax, 1)
    printResult("PE(CE)^2 (E OE)", final, None)

    print("\n" + " "*16 + "Promjena varijable T\n")
    #Promjena perioda za RungeKutta4
    T = 0.01
    final, error = functions.RungeKutta4(x0, A, B, T, tmax, 1)
    printResult("Runge-Kutta r4", final, None)

    final, error = functions.PECE(x0, A, B, T, tmax, 1)
    printResult("PECE (E, T)", final, None)

    final, error = functions.PECECE(x0, A, B, T, tmax, 1)
    printResult("PE(CE)^2 (E OE)", final, None)

    #zadatak 3
    
    print()
    sys.stdout.write("\u0332".join("%15s|%10s|%10s\n" %("Metoda", "x", "y")))
    A = np.array([[0, -2], [1, -3]])
    x0 = np.array([[1], [3]])
    B = np.array([[2, 0], [0, 3]])
    T = 0.01
    tmax = 10
    
    final, error = functions.euler(x0, A, B, T, tmax, 1)
    printResult("Euler", final, None)

    final, error = functions.backwardEuler(x0, A, B, T, tmax, 1)
    printResult("Obrnuti Euler", final, None)
    
    final, error = functions.trapez(x0, A, B, T, tmax, 1)
    printResult("Trapez", final, None)
    
    final, error = functions.RungeKutta4(x0, A, B, T, tmax, 1)
    printResult("Runge-Kutta r4", final, None)
    
    final, error = functions.PECE(x0, A, B, T, tmax, 1)
    printResult("PECE (E, T)", final, None)

    final, error = functions.PECECE(x0, A, B, T, tmax, 1)
    printResult("PE(CE)^2 (E OE)", final, None)

    #Zadatak 4
    
    print()
    sys.stdout.write("\u0332".join("%15s|%10s|%10s\n" %("Metoda", "x", "y")))
    A = np.array([[1, -5], [1, -7]])
    x0 = np.array([[-1], [3]])
    B = np.array([[5, 0], [0, 3]])
    T = 0.01
    tmax = 1
    
    final, error = functions.euler(x0, A, B, T, tmax, 2)
    printResult("Euler", final, None)

    final, error = functions.backwardEuler(x0, A, B, T, tmax, 2)
    printResult("Obrnuti Euler", final, None)
    
    final, error = functions.trapez(x0, A, B, T, tmax, 2)
    printResult("Trapez", final, None)
    
    final, error = functions.RungeKutta4(x0, A, B, T, tmax, 2)
    printResult("Runge-Kutta r4", final, None)
    
    final, error = functions.PECE(x0, A, B, T, tmax, 2)
    printResult("PECE (E, T)", final, None)

    final, error = functions.PECECE(x0, A, B, T, tmax, 2)
    printResult("PE(CE)^2 (E OE)", final, None)

def printResult(Str, x, err):
    if (Str.__contains__("Runge")):
        sys.stdout.write("%15s|%10.6f|%10.6f" %(Str, x[0], x[1]))
        if (err != None):
            sys.stdout.write("|%10.8f" %(err))
        sys.stdout.write("\n")
    else:
        sys.stdout.write("%15s|%10.6f|%10.6f" %(Str, x[0], x[1]))
        if (err != None):
            sys.stdout.write("|%10.3f" %(err))
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()