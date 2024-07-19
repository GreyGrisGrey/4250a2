from numpy import linalg
equations = []
data = open("systems.txt", "r")
blockA = data.readline()
dataA = blockA.split(" ")
dataA[24] = -1
data.readline()
for i in range(25):
    equation = []
    newBlock = data.readline()
    equation = newBlock.split(" ")
    equation[24] = equation[24][::-1]
    for j in range(25):
        if equation[j] == "1":
            equation[j] = float(equation[j])*0.95
        elif equation[j] == "2":
            equation[j] = float(equation[j])*0.95
        else:
            equation[j] = float(equation[j])*0.95
    equation[i] -= 1
    equations.append(equation)
for i in range(25):
    dataA[i] = -float(dataA[i])
x = linalg.solve(equations, dataA)
for i in range(5):
    newLine = []
    for j in range(5):
        newLine.append(x[i*5 + j])
    print(newLine)