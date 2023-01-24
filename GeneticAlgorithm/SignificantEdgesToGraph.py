import networkx as nx
from pgmpy.models import BayesianNetwork
import pandas as pd
from .TwoDMatrixIterator2 import IsDAG
import tools as tools
import .DisplayGraph as dg
import ReadCSV as rcsv
import pgmpy
import timeit
import copy    
import pickle
import .GeneticAlgorithm as GA
import .CrossBreeder as TMI
import .BinaryStringToBayesianN as BSTB
import random
from .SortedList import SortedList
from .AdjMatrixStructure import AdjMatrix
import numpy as np

def InitializeVarToIndexDictionary( IndexToVarListe ):
    var_to_index = {}
    for i in range( len( IndexToVarListe ) ):
        var_to_index[ IndexToVarListe[i] ] = i
    return var_to_index

def SignificantEdgeListToBayesianNetwork( edges_list ):
    return BayesianNetwork( edges_list )

def SignificantEdgesToBayesianNetwork( filename ):
    edges = []
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    for line in Lines:
        bounds = GetVerticesFromString( line )
        edges.append( (bounds[0], bounds[1]) )
    file1.close()
    edges = RemoveSelfEdges( edges )
    bn = BayesianNetwork( edges )
    return bn

def SignificantEdgesToVertices( filename ):
    vertices = set()
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    for line in Lines:
        bounds = GetVerticesFromString( line )
        vertices.add( bounds[0] )
        vertices.add( bounds[1] )
    return list( vertices )
    

def SignificantEdgesToGraph( filename ):
    g = nx.DiGraph()
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    edges = []
    for line in Lines:
        bounds = GetVerticesFromString( line )
        g.add_edge( bounds[0], bounds[1] )
        edges.append( (bounds[0], bounds[1]) )
    file1.close()
    return g

def SignificantEdgesToGraph2( filename ):
    g = nx.DiGraph()
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    edges = []

    for line in Lines:
        bounds = GetVerticesFromString( line )
        reverse_edge = ( bounds[ 1 ], bounds[ 0] )
        if ( bounds[ 0 ] == bounds[ 1 ] ):
            continue
        elif ( reverse_edge in edges ):
            coin = random.randint( 0, 1 )
            if ( coin == 1 ):
                edges.remove( reverse_edge )
                edges.append( ( bounds[0], bounds[1] ) )
        else:
            edges.append( bounds[0], bounds[1] )

    for edge in edges:
        g.add_edge( edge[ 0 ], edge[ 1 ] )
    file1.close()
    return g

def MakeCandidates( number, filename, index_to_vertex ):
    candidates = SortedList( 10, index_to_vertex )
    for i in range( number ):
        network = SignificantEdgesToGraph2( filename )
        if ( not IsDAG( network, index_to_vertex )):
            continue
        adj_matrix = BSTB.NetworkTo2dMatrix( network, index_to_vertex )
        candidates.insert( adj_matrix )
    return candidates


def GetVerticesFromString( string ):
    pre_strings = string.split( ";;;" )
    strings = pre_strings[0].split( "--- ")
    last_colon = FindLastColon( strings[1] )
    strings[1] = strings[ 1 ][ 0:last_colon ]
    return strings

def FindLastColon( string ):
    size = len( string )
    for i in range( size ):
        if ( string[ size -1 -i ] == ":"):
            return size-1-i
    return 0

def RemoveSelfEdges( edges ):
    new_set = []
    for i in range( len( edges ) ):
        if ( edges[i][0] != edges[i][1] ):
            new_set.append( edges[i] )
    return new_set

def GetDataFromDataframe( dataframe, cols ):
    data = []
    for col in cols:
        one_col = tools.ConvertToVector( dataframe[col], col )
        tools.SetNaNOnCol( one_col )
        data.append( one_col )
    return data

def CreateNewDataFrame( data, cols ):
    dataframe_dict = {}
    for i in range( len( cols ) ):
        dataframe_dict[ cols[i] ] = data[i]
    return pd.DataFrame( dataframe_dict )

def NewDataFrameFromCols( dataframe, cols ):
    data = GetDataFromDataframe( dataframe, cols )
    new_dataframe = CreateNewDataFrame( data, cols )
    return new_dataframe

def ScoreGraph(g, method = 'k2', data=None):
    if type(data) == type(None):
        data=pd.read_csv('ScoringDataframe.csv')
    if method == 'k2':
        grader = pgmpy.estimators.K2Score(data,complete_samples_only=False)
    
    severity = 'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?'
    graphscore = 0
    for node in g.nodes:
        if node == severity:
            continue
        parents = list(g.predecessors(node))
        edgescore = grader.local_score(node,parents)
        graphscore += edgescore
    return graphscore


def Score( adjMatrix, index_to_vertex ):
    graph =  BSTB.MatrixToNetwork( adjMatrix, index_to_vertex )
    if ( nx.is_directed_acyclic_graph( graph ) == False ):
        return -9999999
    else:
        return ScoreGraph( graph )
    

def btog(b,es,g1):
    to_rm = []
    g2=copy.deepcopy(g1)
    for j in range(13):  # remove 13 out of 26 edges
        if b[j] == '0':
            to_rm.append(es[j][0])
        else:
            to_rm.append(es[j][1])
    for e in to_rm:
        g2.remove_edge(e[0],e[1])
    return g2

def bidirectional_edges():
    f= open('e.txt')
    lines = f.readlines()
    bie=[]
    for l in lines:
        #print(l)
        n1=l.split('---')[0]
        n2=l.split('---')[1][:-1]
        bie.append((n1,n2))
    
    es=[]
    for i in range(13):
        es.append([bie[2*i],bie[2*i+1]])
    return es

def WriteEdgesToTxt( matrix, index_to_vertex ):
    f = open( "NonRandomFinalGraph.txt", "w" )
    for i in range( len( matrix ) ):
        for j in range( len( matrix[i] ) ):
            if ( matrix[i][j] == 1 ):
                v1 = index_to_vertex[i]
                v2 = index_to_vertex[j]
                f.write( v1 + "---" + v2 )
                f.write( "\n" )
    f.close()