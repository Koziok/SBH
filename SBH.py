from itertools import count
from generate import generate
import math
import random

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
                addEdge(adjMatrix, i, j, cov)
                #print('Adding ', oligo[i], '--', cov, '-->', oligo[j])
    return adjMatrix

def findMinimalNext(spectGraph, visited, currNode):
    return 0

def greedy(spectGraph, oligo, initNodeIndex, initNode, maxLen):
    currNode = initNodeIndex
    currLen = len(initNode)
    currSeq = initNode
    visited = []
    visited.append(initNode)
    while (currLen < maxLen):
        weight = 100000000
        chosenNode = 0
        for i in range(0, len(oligo)):
            if (oligo[i] not in visited):
                minWeight = 100000000
                for j in range(0, len(oligo)):
                    if (oligo[j] not in visited):
                        if (minWeight >= spectGraph[i][j]):
                            minWeight = spectGraph[i][j]
                if (weight >= (minWeight+spectGraph[currNode][i])):
                    weight = minWeight+spectGraph[currNode][i]
                    chosenNode = i
        currLen += (spectGraph[currNode][chosenNode])
        currSeq += oligo[chosenNode][-spectGraph[currNode][chosenNode]:]
        currNode = chosenNode
        visited.append(oligo[currNode])
    return currSeq
    

if __name__ == '__main__':
    k = 4
    #errors = "positive"
    #errors = "negative"
    errors = "both"
    sequence = readFile('sequence.txt')
    oligo = portionDNA(sequence, k)
    initNode = oligo[0]
    #oligo = addErrors(oligo, errors, k)
    oligo.sort()
    oligo = list(dict.fromkeys(oligo))
    #print(initNode, oligo)
    spectGraph = createGraph(oligo)
    initNodeIndex = 0
    for i in range(len(oligo)):
        if(oligo[i] == initNode):
            initNodeIndex = i   
    greedySeq = greedy(spectGraph, oligo, initNodeIndex, initNode, len(sequence))
    #greedySeq = greedy(spectGraph, oligo, initNodeIndex, initNode, 10)
    print(sequence)
    print(greedySeq)