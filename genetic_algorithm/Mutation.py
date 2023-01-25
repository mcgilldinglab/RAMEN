import copy
from .AdjMatrixStructure import AdjMatrix

def MutationMake( matrixObj, changeList, affected_nodes, scorer ):
    mutation = Mutation( matrixObj, changeList, affected_nodes, scorer )
    if ( mutation.IsValid() ):
        return [ mutation ]
    else:
        return []

################ Private Functions Section ###################

#change is a 3 tuple ( i, j, value )
#Mutation obj field
#self.matrix -> reference to original matrix of the mutation
#self.originalScore -> Overall Score of the original Matrix
#self.changes -> changes to be made on the original matrix
#self.scoreDiff -> difference in score for the original matrix and modified matrix
#self.valid -> Indicates if the mutation is valid or no

class Mutation( object ):
    def __init__ ( self, matrixObj, changeList, affected_nodes, scorer ):
        self.matrix = matrixObj.matrix
        self.originalScore = matrixObj.score
        oldScore = scorer.Score( self.matrix, nodes_to_score = affected_nodes )
        
        self.valid = True
        self.changes = MakeChanges( self.matrix, changeList )

        newScore = scorer.Score( self.matrix, nodes_to_score = affected_nodes )
        
        if ( oldScore == -9999999 ):
            self.scoreDiff = -9999999
        
        else:
            if ( newScore == -9999999 ):
                self.valid = False
                self.scoreDiff = -9999999
            else:
                self.scoreDiff = newScore - oldScore
        RevertChanges( self.matrix, self.changes )
            
    def GenerateNewMatrix( self ):
        new_matrix = copy.deepcopy( self.matrix )
        MakeChanges( new_matrix, self.changes )
        new_obj = AdjMatrix( new_matrix, None, score = self.originalScore + self.scoreDiff, Computed=True )
        return new_obj
    
    def IsValid( self ):
        return self.valid

def MakeChanges( matrix, changeList ):
    changedList = []
    for change in changeList:
        i, j, v = change
        if ( matrix[ i ][ j ] != v ):
            matrix[ i ][ j ] = v
            changedList.append( change ) 
    return changedList

def RevertChanges( matrix, changeList ):
    for change in changeList:
        i, j, v = change
        matrix[ i ][ j ] = 1 - v