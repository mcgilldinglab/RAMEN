from .MatrixMutater import MutateMatrix
from .Scorer import IsAcyclic, IsConnected
from .SortedList import SortedList, MutationList
from .CrossBreeder import Mate
import multiprocessing
import random
import sknetwork

#start_parents are the start candidates
#end_thresh represents the minimum difference % from gen to gen for the algorithm to continue running
#mutate_numb is the number of children that we will mutate every gen
#best_cand_num is the number of best children that we will keep every generation
#bad_reprod_accept generations of worse children that we are willing to accept before terminating
#scoring_dataframe is the dataframe we are going to use to score our graphs
def GeneticRun( start_parents, end_thresh, mutate_numb, best_cand_num, bad_reprod_accept, scorer, hard_stop_counter ):
    print("starting Genetic Algorithm")
    difference = 1
    previous_gen_best = -9999999
    current_bad_reprod = 0
    lastGen = GetBestChildren( start_parents, 10 )
    print( lastGen[ 0 ].score )
    counter = 0
    while(  counter < hard_stop_counter ):
        next_Gen = MakeNextGen( lastGen, mutate_numb, best_cand_num, scorer )
        best = next_Gen[ 0 ].score
        difference = abs( best - previous_gen_best )
        print( "generation: " + str( counter ), end = " " )
        print( "best: " + str( best ) )
        lastGen = next_Gen
        previous_gen_best = best

        bad_reprod = False
        if ( difference <= end_thresh or best < previous_gen_best ):
            bad_reprod = True
        
        if ( bad_reprod ):
            if ( current_bad_reprod > bad_reprod_accept ):
                scoreLog.close()
                return next_Gen
            else:
                current_bad_reprod += 1
        else:
            current_bad_reprod = 0
        counter += 1
    return lastGen

################ Private Function Section #####################

def GetBestChildren( matrixListe, numb_to_keep ):
    lList = SortedList( numb_to_keep )
    for i in range( len( matrixListe ) ):
        lList.insert( matrixListe[i] )
    return lList.list

#this is a test function, can remove after
def CheckIfAllChildrenConnected( liste ):
    for i in range( len( liste ) ):
        if ( not IsConnected(liste[i].matrix) ):
            return False
    return True

#test function, can remove after
def CheckNumberOfSeverityEdges( liste ):
    number_liste = []
    for i in range( len( liste ) ):
        sum = 0
        matrix = liste[i].matrix
        for j in range( len( matrix ) ):
            if ( matrix[ j ][ 13 ] == 1 ):
                sum += 1
        number_liste.append( sum )
    print( number_liste )

def IsConnected( input_matrix ):
    return sknetwork.topology.is_connected( input_matrix )

def MakeNextGen( matrixListe, mutate_numb, numb_to_keep, scorer ):
    i = 0
    allChildren = []
    allChildren += matrixListe
    AddCrossOverChildren( allChildren, scorer )
   
    mutationList = GetMutateChildren( allChildren, mutate_numb, numb_to_keep, scorer )
    allChildren += mutationList.ConvertListToMatrixObj()
    return GetBestChildren( allChildren, numb_to_keep )

def GetMutateChildren( allChildren, mutate_numb, numb_to_keep, scorer ):
    mutationList = MutationList( numb_to_keep )
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    
    for i in range( len(allChildren) ):
        p = multiprocessing.Process(target=MutateWorker, args=(i, return_dict, allChildren[i].selfClone(), mutate_numb, numb_to_keep, scorer ) )
        jobs.append( p )
        p.start()
        
    for proc in jobs:
        proc.join()
    for key in return_dict:
        mutationList.insertListe( return_dict[ key ] )
    return mutationList

def AddCrossOverChildren( matrixListe, scorer ):
    size = len( matrixListe )

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range( 5 ):
        parent1 = matrixListe[random.randint( 0, size - 1 )]
        parent2 = matrixListe[random.randint( 0, size - 1 )]
        p = multiprocessing.Process( target=CrossBreedingWorker, args=(i, return_dict, parent1, parent2, scorer ) )
        jobs.append( p )
        p.start()
    for proc in jobs:
        proc.join()
    for key in return_dict:
        matrixListe += return_dict[key]
    return

def CrossBreedingWorker( procnum, return_dict, parent1, parent2, scorer ):
    children = Mate( parent1, parent2, scorer )
    return_dict[ procnum ] = children

def MutateWorker( procnum, return_dict, child, mutate_numb, numb_to_keep, scorer ):
    if ( not ( IsConnected( child.matrix ) and IsAcyclic( child.matrix ) ) ):
        return_dict[ procnum ] = []
        return
    mutationList = MutationList( numb_to_keep )
    for i in range( mutate_numb ):
        mutation = MutateMatrix( child, scorer )
        mutationList.insertListe( mutation )
    
    return_dict[ procnum ] = mutationList.list

def LogScoreAndEdges( file_pointer, matrix, score ):
    counter = 0
    for i in range( len( matrix ) ):
        for j in range( len( matrix[ i ] ) ):
            if ( matrix[ i ][ j ] == 1 ):
                counter += 1
    to_write = str( score ) + " " + "edges: " + str( counter )
    file_pointer.write( to_write )
    file_pointer.write( "\n" )