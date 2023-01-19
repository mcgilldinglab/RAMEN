import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
import copy

class ParameterComputer( object ):
    def __init__ ( self, training_data_file, test_data_file ):
        self.training_df = pd.read_csv( training_data_file )
        self.test_df = pd.read_csv( test_data_file )
    
    def ComputeParameter( self, parents, child ):
        if ( len( parents ) < 1 ):
            raise Exception( "need some parents to evaluate parameter" )
        model = LogisticRegression( max_iter = 1000 ).fit( self.training_df[ parents ] , self.training_df[ child ] )
        score = model.score( self.test_df[ parents ], self.test_df[ child ] )
        if ( score < 0 ):
            return 0
        return score

    #TODO: remove the below 2 methods and test with an actual imputed dataset
    
def CompleteNaNInArray2D( array ):
    for i in range( len( array ) ):
        for j in range( len( array[ i ] ) ):
            if ( np.isnan( array[ i ][ j ] ) ):
                array[ i ][ j ] = 1
    return copy.deepcopy( array ) 

def CompleteNaNInArray1D( array ):
    for i in range( len( array ) ):
        if ( np.isnan( array[ i ] ) ):
            array[ i ] = 1
    return copy.deepcopy( array )