import math
import random
import numpy as np

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

def IncrementEdgeVisited(graph, increment_vector):
    for i in range(len(increment_vector)):
        graph.es[i]["Time_Visited"] += increment_vector[i]


def FindClinicVarIndex(graph, clinic_var):
    for i in range(len(graph.vs)):
        if (graph.vs[i]["clinic_vars"] == clinic_var):
            return i
    return -1

def FindClinicVarName(graph, index):
     return graph.vs[index]["clinic_vars"]


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
        

#binary only
def ComputeMutualInfo(v1, v2):
    P00 = ComputeProbAB(v1,v2, 0, 0)+0.001
    P01 = ComputeProbAB(v1,v2, 0, 1)+0.001
    P10 = ComputeProbAB(v1,v2, 1, 0)+0.001
    P11 = ComputeProbAB(v1,v2, 1, 1)+0.001
    
    PA0 = ComputeProbA(v1, 0)+0.001
    PA1 = ComputeProbA(v1, 1)+0.001

    PB0 = ComputeProbA(v2, 0)+0.001
    PB1 = ComputeProbA(v2, 1)+0.001
    
    part1 = P00*math.log(P00/(PA0*PB0))
    part2 = P01*math.log(P01/(PA0*PB1))
    part3 = P10*math.log(P10/(PA1*PB0))
    part4 = P11*math.log(P11/(PA1*PB1))
    
    return round(part1+part2+part3+part4, 4)

def SetNaNOnCol( data ):
    for i in range( len( data ) ):
        if ( data[i] == -999 ):
            data[i] = np.nan