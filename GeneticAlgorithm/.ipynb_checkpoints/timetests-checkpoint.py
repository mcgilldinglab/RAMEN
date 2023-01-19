import timeit
from tracemalloc import start
import sknetwork
import networkx as nx
import BinaryStringToBayesianN as BSBN
import SignificantEdgesToGraph as SETG
import pandas as pd
import numpy as np
import Scorer as score
from Mutation import Mutation
from AdjMatrixStructure import AdjMatrix

#short good
def IsConnectedTimeTest( network, times ):
    starttime = timeit.default_timer()
    for i in range( times ):
        sknetwork.topology.is_connected( network )
    endtime =  timeit.default_timer()
    return endtime - starttime

#short good
def IsAcyclicTimeTest( network, times ):
    startime = timeit.default_timer()
    for i in range( times ):
        sknetwork.topology.is_acyclic( network )
    endtime = timeit.default_timer()
    return endtime - startime

#very long, need to find how to optimize
def ScoreTimeTest( network, index_to_vertex, scoring_dataframe, times ):
    startime = timeit.default_timer()
    for i in range( times ):
        score.Score( network, index_to_vertex, scoring_dataframe )
    endtime = timeit.default_timer()
    return endtime - startime

#a bit long, should just initialize it once and then leave it
def PandasOpenTest( csv_file ):
    startime = timeit.default_timer()
    pd.read_csv( csv_file )
    endtime = timeit.default_timer()
    return endtime - startime

def PartialScoreTimeTest( matrix, index_to_vertex, scoring_dataframe, nodes_to_score ):
    startime = timeit.default_timer()
    score.Score( matrix, index_to_vertex, scoring_dataframe, nodes_to_score = nodes_to_score )
    endtime = timeit.default_timer()
    return endtime - startime

def OneMutationTest( matrix, index_to_vertex, scoring_dataframe ):
    matrixObj = AdjMatrix( matrix, index_to_vertex )
    changeList = [ ( 1, 2, 1), ( 2, 3, 1 ) ]
    affected_nodes = [ 1, 2, 3 ]
    
    startime = timeit.default_timer()

    mutation = Mutation( matrixObj, changeList, index_to_vertex, affected_nodes, scoring_dataframe )
    endtime = timeit.default_timer()
    return 2*(endtime - startime)


if __name__ == "__main__":
    graph = nx.read_gpickle( "koinetwork.gpickle" )
    g = SETG.SignificantEdgesToGraph( "notcorrectedSorted11005.txt")
    index_to_vertex = list( g.nodes )
    var_to_index_dict = SETG.InitializeVarToIndexDictionary( index_to_vertex )
    ScoringDataframe = pd.read_csv('ScoringDataframe.csv')
    adjMatrix = np.array( BSBN.NetworkTo2dMatrix( graph, var_to_index_dict ) )

    #print( IsConnectedTimeTest( adjMatrix, 1 ) )
    #print( IsAcyclicTimeTest( adjMatrix, 1 ) )
    #print( ScoreTimeTest( adjMatrix, index_to_var_liste, ScoringDataframe, 1 ) )
    #print( PandasOpenTest( 'ScoringDataframe.csv' ) )
    #print( PartialScoreTimeTest( adjMatrix, index_to_var_liste, ScoringDataframe, [ 16, 15, 14 ] ) )
    print( OneMutationTest( adjMatrix, index_to_vertex, ScoringDataframe ) )

        