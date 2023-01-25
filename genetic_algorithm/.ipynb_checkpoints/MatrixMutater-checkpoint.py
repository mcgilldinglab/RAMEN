import random
from Mutation import MutationMake

def MutateMatrix( matrix, scorer ):
    dice = random.randint( 0, 1 )
    if ( dice == 0 ):
        return MutateMatrixOneEdge( matrix, scorer )
    else:
        return MutateMatrixTwoEdges( matrix, scorer )
    
################ Private Functions Section ###################

def MutateMatrixOneEdge( matrixObj, scorer ):
    dice = random.randint( 0, 2 )
    affected_nodes = []
    changeList = []
    
    edges = matrixObj.edges
    ( i, j ) = edges[ random.randint( 0, len( edges ) - 1 ) ]
    size = len( matrixObj.matrix )
    
    #remove
    if ( dice == 0 ):
        changeList = [ ( i, j, 0 ) ]
        affected_nodes.append( i )
        affected_nodes.append( j )
    #add
    elif ( dice == 1 ):
        v1 = random.randint( 0, size - 1 )
        v2 = random.randint( 0, size - 1 )
        changeList = [ ( v1, v2, 1 ) ]
        affected_nodes.append( v1 )
        affected_nodes.append( v2 ) 
    #flip
    else:
        changeList = [ ( i, j, 0 ), ( j, i, 1 ) ]
        affected_nodes.append( i )
        affected_nodes.append( j )

    mutation = MutationMake( matrixObj, changeList, affected_nodes, scorer )

    return mutation

def RemoveTwoEdges( matrixObj, scorer ):
    matrix = matrixObj.matrix
    matrix_length = len( matrix )
    edges = matrixObj.edges
    ( i, j ) = edges[ random.randint( 0, len( edges ) - 1 ) ]
    
    for index in range( len( edges ) ):
        if ( ( edges[ index ][ 0 ] == j ) or ( edges[ index ][ 1 ] == i ) ):
            n1, n2 = edges[ index ]
            changeList = [ ( i, j, 0 ), ( n1, n2, 0 ) ]
            affected_nodes = list( set( [ i, j, n1, n2 ] ) )
            mutation = MutationMake( matrixObj, changeList, affected_nodes, scorer )
            return mutation
        
    changeList = [ ( i, j, 0 ) ]
    affected_nodes = [ i, j ]
    mutation = MutationMake( matrixObj, changeList, affected_nodes, scorer )

    return mutation

def AddTwoEdges( matrixObj, scorer ):
    matrix = matrixObj.matrix
    matrix_length = len( matrix )
    j = random.randint( 0, matrix_length - 1 )
    k = random.randint( 0, matrix_length - 1 )
    l = random.randint( 0, matrix_length - 1 )
    changeList = [ ( j, k, 1 ), ( k, l, 1 ) ]
    affected_nodes = [ j, k, l ]
    mutation = MutationMake( matrixObj, changeList, affected_nodes, scorer )

    return mutation

def FlipTwoEdges( matrixObj, scorer ):
    matrix = matrixObj.matrix
    matrix_length = len( matrix )
    
    edges = matrixObj.edges
    ( i, j ) = edges[ random.randint( 0, len( edges ) - 1 ) ]
    
    for index in range( len( edges ) ):
        if ( ( edges[ index ][ 0 ] == j ) or ( edges[ index ][ 1 ] == i ) ):
            n1, n2 = edges[ index ]
            changeList = [ ( i, j, 0 ), ( n1, n2, 0 ), ( j, i, 1 ), ( n2, n1, 1 ) ]
            affected_nodes = list( set( [ i, j, n1, n2 ] ) )
            mutation = MutationMake( matrixObj, changeList, affected_nodes, scorer )
            return mutation
        
    changeList = [ ( i, j, 0 ), ( j, i, 1 ) ]
    affected_nodes = [ i, j ]
    mutation = MutationMake( matrixObj, changeList, affected_nodes, scorer )

    return mutation

def MutateMatrixTwoEdges( matrixObj, scorer ):
    dice = random.randint( 0, 2 )
    mutation = []

    if ( dice == 0 ):
        mutation = RemoveTwoEdges( matrixObj, scorer )
    elif ( dice == 1 ):
        mutation = AddTwoEdges( matrixObj, scorer )
    else:
        mutation = FlipTwoEdges( matrixObj, scorer )
    
    return mutation