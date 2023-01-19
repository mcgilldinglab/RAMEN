from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
from ParameterComputerSklearn import ParameterComputer
import networkx as nx

def ComputeParameter( network_edge_file, training_data_file, test_data_file ):
    dir_graph = EdgesToGraph( network_edge_file )
    param_computer = ParameterComputer( training_data_file, test_data_file )
    nodes = SignificantEdgesToVertices( network_edge_file )
    for node in nodes:
        parents = list( dir_graph.predecessors( node ) )
        if ( parents == [] ):
            continue
        try:
            print( param_computer.ComputeParameter( parents, node ) )
        except:
            print( node + " has failed computing parameter" )

    
    
    
def SignificantEdgesToVertices( filename ):
    vertices = set()
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    for line in Lines:
        bounds = GetVerticesFromString( line )
        vertices.add( RemoveNewLineChar( bounds[0] ) )
        vertices.add( RemoveNewLineChar( bounds[1] ) )
    return list( vertices )

def EdgesToGraph( filename ):
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    edges = []
    for line in Lines:
        bounds = GetVerticesFromString( line )
        edge = ( RemoveNewLineChar( bounds[ 0 ] ), RemoveNewLineChar( bounds[ 1 ] ) )        
        edges.append( edge )
    file1.close()
    return nx.DiGraph( edges )

def GetVerticesFromString( string ):
    return string.split( "---")

def RemoveNewLineChar( string ):
    new_string = ""
    for i in range( len( string ) ):
        if ( string[ i ] != "\n" ):
            new_string += string[ i ]
    return new_string

########################### To Delete ################################

def MakeDataframe( dataframe, variables ):
    new_data_dict = {}
    for variable in variables:
        new_data_dict[ variable ] = list( dataframe[ variable ] )
    return pd.DataFrame( new_data_dict )