import sknetwork
from pyitlib import discrete_random_variable as drv
import numpy as np
import math
from sklearn.impute import KNNImputer
import timeit
import sys
import math

class Scorer( object ):
    def __init__( self, index_to_vertex, scoring_dataframe, regular_factor, var_to_index_dict ):
        self.index_to_vertex = index_to_vertex
        self.regular_factor = regular_factor
        self.var_to_index_dict = var_to_index_dict
        columns = []
        for vertex in self.index_to_vertex:
            columns.append( list( scoring_dataframe[ vertex ] ) )
        columns = np.array( columns )
        self.columns = columns
    
    def Score( self, matrix, nodes_to_score = [] ):
        if ( not ( IsAcyclic( matrix ) and IsConnected( matrix ) ) ):
            return -9999999
        score = 0
        
        if ( nodes_to_score == [] ):
            score = ScoreEntireGraphFromAdjMatrix( matrix, self.regular_factor, self.columns )
        else:
            score = ScoreSelectNodesFromAdjMatrix( matrix, nodes_to_score, self.regular_factor, self.columns )
        return score
    
    def SetRegularFactor( self, regular_factor ):
        self.regular_factor = regular_factor

################ Private Function Section #####################
     
def ScoreSelectNodesFromAdjMatrix( matrix, nodes_to_score, regular_factor, all_patients ):
    graphscore = 0
    for i in range( len( nodes_to_score ) ):
        node = nodes_to_score[ i ]
        to_score, edge_counter = GetPredecessors( matrix, node )
        graphscore -= ( edge_counter * regular_factor )
        parents = MakeEvaluationMatrix( to_score, all_patients )
        to_score = np.append( to_score, [ nodes_to_score[ i ] ] )
        parents_and_node = MakeEvaluationMatrix( to_score, all_patients )

        if ( parents.size != 0 ):
            score = - ( drv.entropy_joint( parents_and_node ) - drv.entropy_joint( parents ) )
        else:
            score = - ( drv.entropy_joint( parents_and_node ) )
        if ( score > 0 ):
            score = 0
        elif ( np.isnan(score) ):
            score = -1
        graphscore += score
    return graphscore    
    

def ScoreEntireGraphFromAdjMatrix( matrix, regular_factor, all_patients ):
    graphscore = 0
    for i in range( len( matrix ) ):
        to_score, edge_counter = GetPredecessors( matrix, i )
        graphscore -= ( edge_counter * regular_factor )
        parents = MakeEvaluationMatrix( to_score, all_patients )
        to_score = np.append( to_score, [ i ] )
        parents_and_node = MakeEvaluationMatrix( to_score, all_patients )
        
        if ( parents.size != 0 ):
            score = - ( drv.entropy_joint( parents_and_node ) - drv.entropy_joint( parents ) )
        else:
            score = - ( drv.entropy_joint( parents_and_node ) )
        if ( score > 0 ):
            score = 0
        elif ( np.isnan(score) ):
            score = -1
        graphscore += score
    return graphscore

#matrix[m][n] is an edge m -> n
def GetPredecessors( matrix, node_index ):
    pot_pred = matrix[:,node_index]
    pred = np.where( pot_pred == 1 )[0]
    return ( pred , pred.size )

def MakeEvaluationMatrix( indices_to_evaluate, variables ):
    eval_matrix = variables[ indices_to_evaluate ]
    mask = ( eval_matrix.sum(axis=0) > 0 )
    return eval_matrix[ :, mask ]

def Count_Number_Of_Ones( matrix, index ):
    return ( np.count_nonzero( matrix[ :, index ] == 1 ) + np.count_nonzero( matrix[ index ] == 1 ) )

def IsConnected( input_matrix ):
    return sknetwork.topology.is_connected( input_matrix )

def IsAcyclic( input_matrix ):
    return sknetwork.topology.is_acyclic( input_matrix )
