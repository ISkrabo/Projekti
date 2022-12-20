import functions
import declarations
import sys

def printResults(x, iters):
    print("\nAlgoritam pronalazi minimum u točki:")
    for data in x:
        sys.stdout.write('{:.3f} '.format(data))
    print("\nBroj iteracija je " + str(iters))
    return
def printExtra(i1, i2):
    print("Broj iteracija gradijent je " + str(i1))
    if (i2 != -1):
        print("Broj iteracija hessian je " + str(i2))

print()

#Zadatak 1

print("\n-----Zadatak 1-----")
x = [0, 0]
fja = declarations.f3()
grad = declarations.g3()

xnew = functions.gradient_descent(x, fja, grad, 0, False)
print("Rezultati bez korištenja golden ratio:")
printResults(xnew, fja.step)
printExtra(grad.step, -1)

fja.step = 0
grad.step = 0
xnew = functions.gradient_descent(x, fja, grad, 0, True)
print("\nRezultati uz pomoć algoritma golden ratio:")
printResults(xnew, fja.step)
printExtra(grad.step, -1)

#Zadatak 2

print("\n-----Zadatak 2-----")
x = [-1.9, 2]
fja = declarations.f1()
grad = declarations.g1()
hessian = declarations.h1()

xnew = functions.newton_raphson(x, fja, grad, hessian, 0, True)
printResults(xnew, fja.step)
printExtra(grad.step, hessian.step)

x = [0.1, 0.3]
fja = declarations.f2()
grad = declarations.g2()
hessian = declarations.h2()

xnew = functions.newton_raphson(x, fja, grad, hessian, 0, True)
printResults(xnew, fja.step)
printExtra(grad.step, hessian.step)

#Zadatak 3

print("\n-----Zadatak 3-----")
x = [-1.9, 2]
fja = declarations.f1()
conditions = declarations.restrictions()
conditions.setForTask3()
borders = [-100, 100]

xnew = functions.boxAlgorithm(x, fja, conditions, borders, 0, 0)
printResults(xnew, fja.step)

x = [0.1, 0.3]
fja = declarations.f2()

xnew = functions.boxAlgorithm(x, fja, conditions, borders, 0, 0)
printResults(xnew, fja.step)

#Zadatak 4

print("\n-----Zadatak 4-----")
x = [-1.9, 2]
fja = declarations.f1()
conditions = declarations.restrictions()
conditions.setForTask3()

xnew, iters = functions.transformIntoProblem(x, fja, conditions.listOfRestrictions, 0, 0, None)
printResults(xnew, iters)

x = [0.1, 0.3]
fja = declarations.f2()

xnew, iters = functions.transformIntoProblem(x, fja, conditions.listOfRestrictions, 0, 0, None)
printResults(xnew, iters)


#Zadatak 5

print("\n-----Zadatak 5-----")
x = [0, 0]
fja = declarations.f4()
conditions = declarations.restrictions()
conditions.setForTask5()

xnew, iters = functions.transformIntoProblem(x, fja, conditions.listOfRestrictions, 0, 0, declarations.task5H)
printResults(xnew, iters)

print()