from .variable_classification import GetVariableType
from .VarNameTranslator import MakeMapping, MakeReverseMapping
import pandas as pd
import networkx as nx
from pyitlib import discrete_random_variable as drv
import numpy as np
import pickle

def MakeCytoFiles( network_file, csv_filename, noa_filename, mapping_file = None ):
    if ( mapping_file is None ):
        mapping = MakeMapping()
    else:
        mapping_file = open( mapping_file, "rb" )
        mapping = pickle.load( mapping_file )
        mapping_file.close()
    #akeCytoScapeCSV( network_file, csv_filename, mapping )
    MakeCytoScapeSIF( network_file, csv_filename, mapping )
    MakeNodeClassification( network_file, noa_filename, mapping )

def SignificantEdgesToGraphPickle( filename, to_filename ):
    g = SignificantEdgesToGraph( filename )
    to_file = open( to_filename, "ab" )
    pickle.dump( g, to_file )
    to_file.close()

def GetSignificantEdgesScores( filename ):
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    scores = []
    for line in Lines:
        score = GetScoreFromString( line )
        scores.append( score )
    file1.close()
    return scores

def EdgesToEndVarEdgeList( filename, end_string ):
    file1 = open( filename, 'r' )
    Lines = file1.readlines()
    edges = []
    for line in Lines:
        bounds = GetVerticesFromString( line )
        if ( bounds[1][-1] == "\n"):
            bounds[1] = bounds[1][0:-1]
        if ( bounds[1] == end_string ):
            edges.append( bounds[ 0 ] )
    file1.close()
    return edges


def SignificantEdgesToGraph( filename ):
    g = nx.DiGraph()
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    edges = []
    for line in Lines:
        bounds = GetVerticesFromString( line )
        if ( bounds[1][-1] == "\n"):
            bounds[1] = bounds[1][0:-1]
        g.add_edge( bounds[0], bounds[1] )
        edges.append( (bounds[0], bounds[1]) )
    file1.close()
    return g

def GetScoreFromString( string ):
    pre_strings = string.split( ":;;;" )
    score = float( pre_strings[ 1 ] )
    return score

def GetVerticesFromString( string ):
    pre_strings = string.split( ":;;;" )
    strings = pre_strings[ 0 ].split( "--- " )
    return strings

def MakeCytoScapeCSV( network_file, out_filename, mapping = {} ):
    g = SignificantEdgesToGraph( network_file )
    leftVertices = []
    rightVertices = []
    for edge in list( g.edges ):
        leftVertices.append( GetMapString(mapping, edge[0]).replace( ",", "-" ) )
        rightVertices.append( GetMapString(mapping, edge[1]).replace( ",", "-" ) )
    data = { "Left": leftVertices, "Right": rightVertices }
    df = pd.DataFrame( data )
    df.to_csv( out_filename )

def MakeCytoScapeSIF( network_file, sif_filename, mapping ):
    sif = open( sif_filename, 'w' )
    g = SignificantEdgesToGraph( network_file )
    categ = [ "strongest", "strong", "okay", "weaker" ]
    counter = 0
    splitter = int( len( g.edges )/4 )
    
    for edge in list( g.edges ):
        bound1 = str( mapping[ edge[ 0 ] ] )
        bound2 = str( mapping[ edge[ 1 ] ] )
        string = bound1 + "\t" + categ[ min( int( counter/splitter ), 3 ) ] + "\t" + bound2 + "\n"
        counter += 1
        sif.write( string )
    sif.close()

def MakeNodeClassification( network_file, noa_filename, mapping ):
    noa = open( noa_filename, 'w' )
    g = SignificantEdgesToGraph( network_file )
    noa.write( "Role (class=variable category)\n" )
    for node in g.nodes:
        classification = GetVariableType( node )
        write_node = node
        write_node = GetMapString( mapping, node )
        write_string = write_node + " = " + classification + "\n"
        noa.write( write_string )
    noa.close()
    
def GetMapString( mapping, string ):
    result = mapping.get( string )
    if ( result is None ):
        result = string
    return result

def MakeMutualInformationRanking( result_filename, csv_file, to_filename, reverse = True ):
    g = SignificantEdgesToGraph( result_filename )
    df = pd.read_csv( csv_file )
    file = open( to_filename, "w" )
    sorted_list = []
    for edge in g.edges:
        v1 = edge[ 0 ]
        v2 = edge[ 1 ]
        vector1 = np.array( df[v1] )
        vector2 = np.array( df[v2] )
        mi = ComputeMutualInformation( vector1, vector2 )
        sorted_list.append( ( mi, ( v1, v2 ) ) )
    sorted_list = sorted( sorted_list, reverse = reverse )
    for element in sorted_list:
        edge = element[ 1 ]
        mi = element[ 0 ]
        file.write( edge[ 0 ] + "--- " + edge[ 1 ] + ":;;;" + str( mi )+ "\n" )
    file.close()

    
def MakeWeightedSif( filename, out_filename, df_csv ):
    file1 = open( filename, 'r' )
    out_file = open( out_filename, 'w' )
    df = pd.read_csv( df_csv )
    mapping = MakeMapping()
    reverse_mapping = MakeReverseMapping()
    Lines = file1.readlines()
    edges = []
    for line in Lines:
        bounds = GetVerticesSif( line )
        if ( bounds[1][-1] == "\n"):
            bounds[1] = bounds[1][0:-1]
        un_simp1 = reverse_mapping[ bounds[ 0 ] ]
        un_simp2 = reverse_mapping[ bounds[ 1 ] ]
        vector1 = df[ un_simp1 ]
        vector2 = df[ un_simp2 ]
        mi = ComputeMutualInformation( vector1, vector2 )
        write_string = mapping[ un_simp1 ] + "\t" + str( mi ) + "\t" + mapping[ un_simp2 ] + "\n"
        out_file.write( write_string )
    file1.close()
    out_file.close()

def ComputeMutualInformation( vector1, vector2 ):
    mask = ( vector1 != -999 ) * ( vector2 != -999 )
    x1 = vector1[ mask ]
    x2 = vector2[ mask ]
    if ( len( x1 ) == 0 ):
        return 0
    mi = drv.entropy( x1 ) - drv.entropy_conditional( x1, x2 )
    return mi

def GetVerticesSif( string ):
    bounds = string.split( "---" )
    for i in range(len(bounds)):
        bounds[i] = bounds[i].replace( "->", "???" )
        #bounds[i] = bounds[i].replace( "-", "," )
        bounds[ i ] = ReplaceToCommaSmart( bounds[ i ] )
        bounds[i] = bounds[i].replace( "???", "->" )
    return bounds

def ReplaceToCommaSmart( string ):
    new_string = ""
    for i in range( len( string ) ):
        if ( string[ i ] == "-" and string[ i + 1 ] == " " ):
            new_string += ","
        else:
            new_string += string[ i ]
    return new_string