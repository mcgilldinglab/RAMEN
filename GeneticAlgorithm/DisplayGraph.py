import matplotlib.pyplot as plt
import networkx as nx

def ShowGraphFromFile( filename, with_labels = False ):
    g = SignificantEdgesToGraph( filename )
    ShowGraphNX( g, with_labels )

def ShowGraph( graph ):
    G = graph.to_networkx()
    nx.draw( G, node_size = 50 )
    plt.show()

def ShowGraphNX( graph, with_labels ):
    nx.draw( graph, node_size = 50, with_labels = with_labels )
    plt.show()

def SignificantEdgesToGraph( filename ):
    g = nx.Graph()
    file1 = open( filename, 'r')
    Lines = file1.readlines()
    edges = []

    for line in Lines:
        bounds = GetVerticesFromString( line )
        edge = ( RemoveNewLineChar( bounds[ 0 ] ), RemoveNewLineChar( bounds[ 1 ] ) )
        edges.append( edge )
    for edge in edges:
        g.add_edge( edge[ 0 ], edge[ 1 ] )
    file1.close()
    return g

def RemoveNewLineChar( string ):
    new_string = ""
    for i in range( len( string ) ):
        if ( string[ i ] != "\n" ):
            new_string += string[ i ]
    return new_string

def GetVerticesFromString( string ):
    return string.split( "---")

if __name__ == "__main__":
    graph = nx.read_gpickle( "koinetwork.gpickle" )
    print( nx.is_directed_acyclic_graph( graph ) )
    #ShowGraphNX( graph )