import random
from .AdjMatrixStructure import AdjMatrix
from copy import deepcopy

def Mate( matrixObj1, matrixObj2, scorer ):
    matrix1 = matrixObj1.matrix
    matrix2 = matrixObj2.matrix
    
    to_cross_indices = set()
    matrix_size = len( matrix1 )
    
    for i in range( matrix_size ):
        to_cross_indices.add( random.randint( 0, matrix_size - 1 ) )
    
    to_cross_indices = list( to_cross_indices )
    
    child1 = deepcopy( matrix1 )
    child2 = deepcopy( matrix2 )
    
    for index in to_cross_indices:
        temp = child1[index]
        child1[index] = child2[index]
        child2[index] = temp
        
    childObj1 = AdjMatrix( child1, scorer )
    childObj2 = AdjMatrix( child2, scorer )
    
    offSpringListe = []

    if ( childObj1.score != -9999999 ):
        offSpringListe.append( childObj1 )
    if ( childObj2.score != -9999999 ):
        offSpringListe.append( childObj2 )

    return offSpringListe

################ Private Functions Section ###################

def GetSize( matrix ):
    size = 0
    for i in range( len( matrix ) ):
        for j in range( len( matrix[i]) ):
            size += 1
    return size

def GetAtIndex( matrix, index ):
    matrixLength = len( matrix )
    x = int(index/matrixLength)
    y = index%( matrixLength )
    return matrix[x][y]

def SetAtIndex( matrix, index, element ):
    matrixLength = len( matrix )
    x = int(index/matrixLength)
    y = index%( matrixLength )
    matrix[x][y] = element

def flattenMatrix( matrix ):
    flattened = []
    for i in range( len( matrix ) ):
        flattened += matrix[i]
    return flattened