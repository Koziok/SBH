from re import L
from generate import generate
import math
import random
import numpy as np

def readFile(file):
    f = open(file, "r")
    return f.readline()

def portionDNA(sequence, k):
    oligo = []
    for i in range(0, len(sequence)-k+1):
        oligo.append(sequence[i:i+k])
    return oligo

def addErrors(oligo, errors, k):
    errNumber = math.floor(len(oligo) * 0.05)
    if (errors == "positive"):
        for i in range(0, errNumber):
            oligo.append(''.join(generate(k)))
    elif (errors == "negative"):
        for i in range(0, errNumber):
            randomIndex = random.randint(1, len(oligo)-1)
            del oligo[randomIndex]
    elif (errors == "both"):
        for i in range(0, errNumber):
            randomIndex = random.randint(1, len(oligo)-1)
            del oligo[randomIndex]
        for i in range(0, errNumber):
            oligo.append(''.join(generate(k)))
    return oligo

def addEdge(matrix, node1, node2, weight):
    matrix[node1][node2] = weight

def checkCov(word1, word2):
    if (word1 == word2):
        return len(word1)
    else:
        for i in range(1, len(word1)):
            newWord1 = word1[i:]
            newWord2 = word2[:len(word1)-i]
            if(newWord1 == newWord2):
                return i
        return len(word1)        

def createGraph(oligo):
    numOfNodes = len(oligo)
    adjMatrix = [[0 for column in range(numOfNodes)] for row in range(numOfNodes)]
    for i in range(numOfNodes):
        #print('---------',oligo[i] ,'---------')
        for j in range(numOfNodes):
            cov = checkCov(oligo[i], oligo[j])
            if (cov != 0):
                addEdge(adjMatrix, i, j, len(oligo[0])-cov)
                #print('Adding ', oligo[i], '--', cov, '-->', oligo[j])
    return adjMatrix

def generateSolution(oligo, initNodeIndex, initNode, maxLen, spectOligos, weights, spectGraph, probabilities):
    solution = []
    solution.append(initNode)
    currLen = len(initNode)
    currIndex = initNodeIndex
    length = 1
    
    while(currLen < maxLen):
        choiceOligo = np.random.choice(oligo, p=weights[currIndex])
        choice = oligo.index(choiceOligo)
        choiceCost = spectGraph[currIndex][choice]
        probabilities[currIndex][choice] /= 2
        for i in range(0, len(oligo)):
            weights[currIndex][i] = probabilities[currIndex][i]/sum(probabilities[currIndex])

        #print(choiceOligo, choice, choiceCost, weights[currIndex][choice])
        #print(weights[currIndex])

        currLen += (len(initNode) - choiceCost)
        if (currLen > maxLen):
            currLen -= (len(initNode) - choiceCost)
            currIndex = choice
            return solution, length/spectOligos
        solution.append(oligo[choice])
        currIndex = choice
        length += 1
    #print(solution)
    return solution, length/spectOligos

def generateSolutions(colonySize, oligo, initNodeIndex, initNode, maxLen, spectOligos, probabilities, spectGraph):
    solutions = []
    weights = [[0 for column in range(len(oligo))] for row in range(len(oligo))]
    for i in range(0, len(oligo)):
        for j in range(0, len(oligo)):
            weights[i][j] = probabilities[i][j]/sum(probabilities[i])
    #print(weights)
    for i in range(0, colonySize):
        solutions.append(generateSolution(oligo, initNodeIndex, initNode, maxLen, spectOligos, weights, spectGraph, probabilities))
    return solutions

def compareSolutions(solutions):
    topTen = []
    solutions.sort(key=lambda row: (row[1]), reverse=True)
    for i in range(0, 19):
        topTen.append(solutions[i])
    return topTen

def pheromoneUpdate(topTen, pheromones, oligo, evaporationRate):
    currIndex = 0
    nextIndex = 0
    for i in range(0, len(topTen)):
        for j in range(0, len(topTen[i][0])-1):
            currIndex = oligo.index(topTen[i][0][j])
            nextIndex = oligo.index(topTen[i][0][j+1])
            pheromones[currIndex][nextIndex] += topTen[i][1]
    for i in range(0, len(oligo)):
        for j in range(0, len(oligo)):
            pheromones[i][j] *= evaporationRate       
    return pheromones

def antColony(spectGraph, oligo, initNodeIndex, initNode, maxLen, spectOligos):
    generations = 10
    colonySize = 50
    evaporationRate = 0.65 #ile procent feromonów wyparuje po co iteracje
    alpha = 1 #waga feromonów
    beta = 7 #waga pokrycia
    pheromones = [[0 for column in range(len(oligo))] for row in range(len(oligo))]
    probabilities = [[0 for column in range(len(oligo))] for row in range(len(oligo))]
    for i in range(0, len(oligo)):
        for j in range(0, len(oligo)):
            probabilities[i][j] = spectGraph[i][j]
    i = 0
    while (i < generations):
        solutions = generateSolutions(colonySize, oligo, initNodeIndex, initNode, maxLen, spectOligos, probabilities, spectGraph)
        #print(solutions)
        topTen = compareSolutions(solutions)
        #print('Nowe wyniki')
        print(topTen[0][-1])
        pheromones = pheromoneUpdate(topTen, pheromones, oligo, evaporationRate)
        #print(pheromones)
        for j in range(0, len(oligo)):
            for k in range(0, len(oligo)):
                if (pheromones[j][k] != 0):
                    probabilities[j][k] = pheromones[j][k]**alpha * spectGraph[j][k]**beta
                else:
                    probabilities[j][k] = 0.1**alpha * spectGraph[j][k]**beta
        #print(probabilities)
        i += 1
    return topTen

if __name__ == '__main__':
    k = 8
    #errors = "positive"
    #errors = "negative"
    errors = "both"
    sequence = readFile('sequence.txt')
    oligo = portionDNA(sequence, k)
    spectOligos = len(oligo)
    initNode = oligo[0]
    oligo = addErrors(oligo, errors, k)
    oligo.sort()
    oligo = list(dict.fromkeys(oligo))
    #print(initNode, oligo)
    spectGraph = createGraph(oligo)
    initNodeIndex = 0
    for i in range(len(oligo)):
        if(oligo[i] == initNode):
            initNodeIndex = i
    #print(spectGraph)
    

    topTen = antColony(spectGraph, oligo, initNodeIndex, initNode, len(sequence), spectOligos)
    #print(oligo)
    print('Ostateczne wyniki: ')
    print(topTen[0])