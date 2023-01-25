import numpy as np
from pyitlib import discrete_random_variable as drv
import random
from .tools import CreateAdjMatrix
from .InitializeGraph import InitializeMutualInfoMatrixGraph
import pandas as pd


def MakeMutualInfoMatrixNoSave( df ):
    g = InitializeMutualInfoMatrixGraph( df )
    matrix = np.array(InitializeMutualInfoMatrix( g ) )
    print( "done" )
    return matrix

#assumption here is that data file is already processed ProcessDataframe.py
def MakeMutualInfoMatrixNpy( csv_file, save_file_name ):
    dataframe = pd.read_csv( csv_file )
    g = InitializeMutualInfoMatrixGraph( dataframe )
    matrix = np.array(InitializeMutualInfoMatrix( g ))
    print( matrix.shape )
    np.save( save_file_name, matrix )    

def ShuffleMutualInfo(MutualInfoMatrix):
    size = len(MutualInfoMatrix)
    for i in range(size):
        for j in range(size):
            randi = random.randint(0, size-1)
            randj = random.randint(0, size-1)

            temp = MutualInfoMatrix[i][j]

            MutualInfoMatrix[i][j] = MutualInfoMatrix[randi][randj]
            MutualInfoMatrix[j][i] = MutualInfoMatrix[randi][randj]

            MutualInfoMatrix[randi][randj] = temp
            MutualInfoMatrix[randj][randi] = temp

###################### Private Function Section ######################

def InitializeMutualInfoMatrix( g ):
    vector_matrix = GenerateGraphVectorMatrix( g )
    random_var1 = np.random.randint( 0, 10, vector_matrix.shape[1] )
    random_var2 = np.random.randint( 0, 10, vector_matrix.shape[1] )
    mi_tracker = []
    for i in range( 100 ):
        mi_tracker.append( ComputeMutualInformationVar( random_var1, random_var2 ) )
    mi_tracker.sort()
    lower_bound = mi_tracker[-5]
    mi_matrix = ComputeMutualInformation( vector_matrix, lower_bound )
    return mi_matrix

def GenerateGraphVectorMatrix(g):
    matrix = []
    for i in range(len(g.vs)):
        matrix.append(g.vs[i]["Vector"])
    return np.array(matrix)

def ComputeMutualInformation( array, lower_bound = 0 ):
    size = len( array )
    mutual_info_matrix = CreateAdjMatrix(size, size)
    for i in range( len( array ) ):
        current_var = array[i]
        for j in range( len( array ) ):
            inner_var = array[j]
            mutual_info_matrix[i][j] = max( ComputeMutualInformationVar( current_var, inner_var ), lower_bound )
    return mutual_info_matrix

def ComputeMutualInformationVar( var1, var2 ):
    mask = ( var1 != -999 ) * ( var2 != -999 )
    x1 = var1[ mask ]
    x2 = var2[ mask ]
    if ( len(x1) == 0 ):
        return 0
    else: 
        return drv.entropy( x1 ) - drv.entropy_conditional( x1, x2 )
        
        #return drv.information_mutual( x1.reshape( 1, x1.shape[0] ), x2.reshape( 1, x2.shape[0] ) )