from .CandidateMaker import MakeCandidates
from .GeneticAlgorithm import GeneticRun
from .Scorer import Scorer
import timeit
from .GraphConverter import MatrixToNetwork

def StructuredLearningRun( ScoringDataframe, significant_edges, num_candidates, end_thresh, mutate_num, best_cand_num, bad_reprod_accept, regular_factor, hard_stop_counter = 50 ):
    index_to_vertex = SignificantEdgesToVertices( significant_edges )
    print( len( index_to_vertex ) )
    var_to_index_dict = InitializeVarToIndexDictionary( index_to_vertex )
    print("initializing scorer")
    scorer = Scorer( index_to_vertex, ScoringDataframe, regular_factor, var_to_index_dict )
    print("done initializing scorer")
    print("making candidates" )
    startime = timeit.default_timer()  
    candidates = MakeCandidates( significant_edges, scorer, index_to_vertex, var_to_index_dict, num_candidates )
    endtime = timeit.default_timer()
    print( "Finished making candidates in", end = ": ")
    print( endtime-startime )
    children = GeneticRun( candidates, end_thresh, mutate_num, best_cand_num, bad_reprod_accept, scorer, hard_stop_counter )
    return MatrixToNetwork( children[ 0 ].matrix, index_to_vertex )

######## private functions #############

def InitializeVarToIndexDictionary( IndexToVarListe ):
    var_to_index = {}
    for i in range( len( IndexToVarListe ) ):
        var_to_index[ IndexToVarListe[i] ] = i
    return var_to_index

def WriteEdgesToTxt( matrix, index_to_vertex, to_file_name ):
    f = open( to_file_name, "w" )
    for i in range( len( matrix ) ):
        for j in range( len( matrix[i] ) ):
            if ( matrix[i][j] == 1 ):
                v1 = index_to_vertex[i]
                v2 = index_to_vertex[j]
                f.write( v1 + "--- " + v2 )
                f.write( ":;;;")
                f.write( "\n" )
    f.close()

def SignificantEdgesToVertices( Lines ):
    vertices = set()
    for line in Lines:
        bounds = GetVerticesFromString( line )
        vertices.add( bounds[0] )
        vertices.add( bounds[1] )
    return sorted(list( vertices ))

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

def SimplifyNetworkNames( network_file, to_file_name, mapping ):
    file1 = open( network_file, 'r')
    f = open( to_file_name, 'w' )
    Lines = file1.readlines()
    not_mapped = set()
    for line in Lines:
        bounds = GetVerticesFromString( line )
        bound1_mapped = mapping.get( bounds[ 0 ] )
        bound2_mapped = mapping.get( bounds[ 1 ] )
        if ( bound1_mapped is None ):
            bound1_mapped = bounds[ 0 ]
            not_mapped.add( bound1_mapped )
        if ( bound2_mapped is None ):
            bound2_mapped = bounds[ 1 ]
            not_mapped.add( bound2_mapped )
        f.write( bound1_mapped + "--- " + bound2_mapped )
        f.write( "\n" )
    file1.close()
    f.close()
    return list( not_mapped )