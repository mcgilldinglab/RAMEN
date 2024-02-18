import networkx as nx
import random

from .GraphConverter import NetworkTo2dMatrix, MatrixToNetwork
import numpy as np
from .AdjMatrixStructure import AdjMatrix
import timeit
import sknetwork


def MakeCandidates( significant_edges, scorer, index_to_vertex, var_to_index_dict, num_candidates ):
    graphs = []
    for i in range( num_candidates ):
        graph = SignificantEdgesToGraph( significant_edges )
        graphs.append( graph )
    
    candidates = []

    for j in range( len( graphs ) ):
        matrix = np.array( NetworkTo2dMatrix( graphs[ j ], var_to_index_dict ) )
        if ( sknetwork.topology.is_connected( matrix ) and sknetwork.topology.is_acyclic( matrix ) ):
            matrixObj = AdjMatrix( matrix, scorer )
            candidates.append( matrixObj )
            continue
        RemoveCyclesMatrix( matrix )
        MakeConnected( matrix )
        matrixObj = AdjMatrix( matrix, scorer )        
        candidates.append( matrixObj )
        print( matrixObj.score )
    return candidates

########### private functions ############
def SignificantEdgesToGraph( signif_edges ):
    g = nx.DiGraph()
    Lines = signif_edges
    edges = []

    for line in Lines:
        bounds = GetVerticesFromString( line )
        edge = ( bounds[ 0 ], bounds[ 1 ] )
        reverse_edge = ( bounds[ 1 ], bounds[ 0] )
        if ( bounds[ 0 ] == bounds[ 1 ] ):
            continue
        elif ( reverse_edge in edges ):
            coin = random.randint( 0, 1 )
            if ( coin == 1 ):
                edges.remove( reverse_edge )
                edges.append( edge )
        else:
            edges.append( edge )
    for edge in edges:
        g.add_edge( edge[ 0 ], edge[ 1 ] )
    return g

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

def DetectTwoCycles( matrix ):
    for i in range( len( matrix ) ):
        for j in range( len( matrix ) ):
            if ( matrix[ i ][ j ] == 1 and matrix[ j ][ i ] == 1 ):
                return True
    return False

def IsEmpty( matrix ):
    for i in range( len( matrix ) ):
        for j in range( len( matrix ) ):
            if ( matrix[ i ][ j ] == 1 ):
                return False
    return True

def CheckTwoMatrixEqual( matrix1, matrix2 ):
    for i in range( len( matrix1 ) ):
        for j in range( len( matrix1[ i ] ) ):
            if ( matrix1[ i ][ j ] != matrix2[ i ][ j ] ):
                return False
    return True

def CheckMatrixOnlyOneAndZero( matrix ):
    for i in range( len( matrix ) ):
        for j in range( len( matrix[ i ] ) ):
            if ( matrix[ i ][ j ] != 1 and matrix[ i ][ j ] != 0 ):
                return False
    return True

def GetNeightbours( matrix, current ):
    neighbours = []
    neighbourhood = matrix[ current ]
    return np.where( neighbourhood == 1 )[ 0 ] 

def FindEdgesToRemoveFromStart( matrix, start ):
    visited = set()
    stack = set()

    def dfs( node ):
        visited.add( node )
        stack.add( node )
        to_remove = []
        for neighbor in GetNeightbours( matrix, node ):
            if neighbor not in visited:
                to_remove += dfs( neighbor )
            elif neighbor in stack:
                to_remove += [ ( node, neighbor ) ]
        stack.remove(node)
        return to_remove
    
    return dfs( start )
    
def RemoveCyclesMatrix( matrix ):
    for i in range( matrix.shape[ 0 ] ):
        edges_to_remove = FindEdgesToRemoveFromStart( matrix, i )
        for edge in edges_to_remove:
            x, y = edge
            matrix[ x ][ y ] = 0

def FindAllReachableEdges( matrix, start ):
    stack = []
    stack.insert( 0, start )
    visited = [ 0 ] * matrix.shape[ 0 ]
    reachables = []
    while( len( stack ) != 0 ):
        popped = stack.pop( 0 )
        neighbours = GetNeightbours( matrix, popped )
        for neighbour in neighbours:
            if ( visited[ neighbour ] == 0 ):
                visited[ neighbour ] = 1
                stack.insert( 0, neighbour )
                reachables.append( neighbour )
    return reachables

def MakeConnected( matrix ):
    chunks = FindIslands( matrix )
    if ( len( chunks ) == 1):
        return
    else:
        for i in range( len( chunks ) - 1 ):
            random_pos1 = random.randint( 0, len( chunks[i] ) - 1 )
            random_pos2 = random.randint( 0, len( chunks[i + 1] ) - 1 )
            starter = chunks[ i ][ random_pos1 ]
            receiver = chunks[ i + 1 ][ random_pos2 ]
            matrix[ starter ][ receiver ] = 1

def FindIslands( matrix ):
    size = matrix.shape[ 0 ]
    reachableDict = {}
    for i in range( size ):
        reachableDict[ i ] = FindAllReachableEdges( matrix, i )
    
    subgraphs = []
    chunks = []
    for key in reachableDict:
        subgraph = reachableDict[ key ]
        subgraph.append( key )
        subgraphs.append( subgraph )
    for subgraph in subgraphs:
        chunks = UpdateChunks( chunks, subgraph )
    return chunks

def UpdateChunks( chunks, element ):
    new_chunks = []
    to_merge = []
    for i in range( len( chunks ) ):
        if ( not Intersection( chunks[ i ], element ) ):
            new_chunks.append( chunks[ i ] )
        else:
            to_merge.append( i )
    if ( to_merge == [] ):
        new_chunks.append( element )
    else:
        new_subgraph = []
        new_subgraph += element
        for j in range( len( to_merge ) ):
            new_subgraph += chunks[ to_merge[ j ] ]
        new_chunks.append( new_subgraph )
    return new_chunks

def Intersection( subgraph1, subgraph2 ):
    for i in range( len( subgraph1 ) ):
        if ( subgraph1[ i ] in subgraph2 ):
            return True
    return False

def MakeNodeSetFromStartNode( node, reachableDict, mergedTracker ):
    new_liste = []
    queue = []
    queue.append( node )
    while( queue != [] ):
        top_node = queue.pop( 0 )
        mergedTracker[ top_node ] = 1
        new_liste.append( top_node )
        queue += reachableDict[ top_node ]
    return list( set( new_liste ) )

def CountEdges( matrix ):
    counter = 0
    for i in range( len( matrix ) ):
        for j in range( len( matrix ) ):
            if ( matrix[ i ][ j ] == 1):
                counter += 1
    return counter

def GetPredecessors( matrix, index ):
    predecessors = []
    for i in range( len( matrix ) ):
        if ( matrix[ i ][ index ] == 1 ):
            predecessors.append( i )
    return predecessors
                    
