import math
import random
import numpy as np
from Discretization import *

##################################################################

def TwoDArrayToOneDArray( array ):
    new_array = []
    for i in range( len( array ) ):
        for j in range( len( array[i] ) ):
            new_array.append( array[i][j] )
    return new_array 

##################################################################

def SumProbMatrix(matrix):
    summed = []
    for i in range(len(matrix)):
        sum = 0
        for j in range(len(matrix[i])):
            sum += matrix[i][j]
        summed.append(sum)
    return summed


def AverageListValue( liste ):
    total = len( liste )
    sum = 0
    for i in range( total ):
        sum += liste[i]
    return sum/total


def Sumlist( liste ):
    sum = 0
    for i in range( len( liste ) ):
        sum += liste[i]
    return sum

##################################################################


def FindClinicVarIndex(graph, clinic_var):
    for i in range(len(graph.vs)):
        if (graph.vs[i]["clinic_vars"] == clinic_var):
            return i
    return -1

def StopMovement(index, prob_array):
    for i in range(len(prob_array[index])):
        prob_array[index][i] = 0
    prob_array[index][index] = 1


def SetNextToItself(clinic_var, graph, prob_array):
    index = FindClinicVarIndex(graph, clinic_var)
    StopMovement(index, prob_array)


##################################################################


def CreateArrayOfZeros(n):
    listofzeros = [0] * n
    return listofzeros


def CreateAdjMatrix(x, y):
    AdjMatrix = []
    for i in range(y):
        newlist = CreateArrayOfZeros(x)
        AdjMatrix.append(newlist)
    return AdjMatrix


def Swap2D(matrix, x1, y1, x2, y2):
    temp = matrix[x1][y1]
    matrix[x1][y1] = matrix[x2][y2]
    matrix[x2][y2] = temp


##################################################################


def RollRandom(interval):
    randomRoll = random.uniform(0, interval[len(interval)-1])
    for i in range(len(interval)):
        if (randomRoll <= interval[i]):
            return i
    return -1

def Shuffle2DMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            randomx = random.randint(0, len(matrix)-1)
            randomy = random.randint(0, len(matrix[i])-1)
            Swap2D(matrix, i, j, randomx, randomy)

##################################################################


#can be optimized by storing in dictionary instead of computing everytime
def ComputeProbA(v, value):
    positive = 0
    mask = (np.array(v) == value)
    return mask.sum()/len(v)


def ComputeProbAB(v1, v2, value1, value2):
    maskA = (np.array(v1) == value1)
    maskB = (np.array(v2) == value2)

    maskAB = maskA*maskB

    return (maskAB.sum()/len(v1))