import networkx as nx
from .tools import CreateAdjMatrix

def DictionaryToList( dictionary ):
    edges = []
    for index in dictionary:
        edges = edges + dictionary[ index ]
    return edges

def RemoveRedundantEdges( liste, dictionary ):
    dictionary_list = DictionaryToList( dictionary )
    non_redundant_list = []
    for i in range( len( liste ) ):
        if ( liste[i] not in dictionary_list ):
            non_redundant_list.append( liste[i] )
    return non_redundant_list


def BuildGraphFromBinaryString( edgeList, candidate_dictionary, bin_string ):
    edges = []
    for i in range( len( edgeList ) ):
        edges.append( edgeList[i] )
    for j in range( len( bin_string ) ):
        edge_to_add = candidate_dictionary[j][ bin_string[j] ]
        edges.append( edge_to_add )
    return edges

def IncrementBinaryString( bin_string ):
    current = 0
    while( current < len( bin_string ) ):
        if ( ( bin_string[ current ] + 1 ) == 1 ):
            bin_string[ current ] += 1
            return
        else:
            bin_string[ current ] = 0
            current += 1
    if( bin_string == [0]*len( bin_string ) ):
        for i in range( len( bin_string ) ):
            bin_string[i] = 2


def NetworkTo2dMatrix( network, vertex_to_index ):
    size = len( vertex_to_index )
    network_as_edges = list( network.edges )
    matrix = CreateAdjMatrix( size, size )
    for i in range( len( network_as_edges ) ):
        index1 = vertex_to_index[ network_as_edges[i][0] ]
        index2 = vertex_to_index[ network_as_edges[i][1] ]
        matrix[index1][index2] = 1
    return matrix

def RemoveSelfEdges( edges ):
    new_set = []
    for i in range( len( edges ) ):
        if ( edges[i][0] != edges[i][1] ):
            new_set.append( edges[i] )
    return new_set

def MatrixToNetwork( matrix, index_to_vertex ):
    graph = nx.DiGraph()

    for i in range( len( matrix ) ):
        for j in range( len( matrix[i] ) ):
            if ( matrix[i][j] == 1):
                vertex1 = index_to_vertex[i]
                vertex2 = index_to_vertex[j]
                graph.add_edge( vertex1, vertex2 )
    return graph