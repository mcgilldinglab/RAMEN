import numpy as np
import copy

class AdjMatrix( object ):
    def __init__ ( self, matrix, scorer, score = -9999999, Computed = False ):
        self.matrix = np.array( matrix )
        if ( Computed ):
            self.score = score
        else:
            self.score = scorer.Score( self.matrix )
            
        self.edges = []
        for i in range( len( self.matrix ) ):
            for j in range( len( self.matrix[ i ] ) ):
                if ( self.matrix[i][j] == 1 ):
                    self.edges.append( ( i, j ) )
    
    def selfClone( self ):
        return AdjMatrix( copy.deepcopy(self.matrix), None, self.score, Computed = True )