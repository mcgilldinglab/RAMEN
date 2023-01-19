import multiprocessing
import random
import tools as tools
import ArraySaver as As
import ExpEdgeVisitTracker as ET
import numpy as np

#end_string = "If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?"
end_string = "Long Covid"

def RunExperiments( g, npy_filename, times, numb_walks, numb_steps, result_filename ):
    mutual_Info_Matrix = As.LoadArrayFromFile( npy_filename )
    tools.SetNextToItself(end_string, g, mutual_Info_Matrix)

    prob_matrix = InitializeProbabilityMatrix( mutual_Info_Matrix )

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range( times ):
        p = multiprocessing.Process( target = TheWalks, args = ( i, return_dict, g, numb_walks, numb_steps, prob_matrix )  )
        jobs.append( p )
        p.start()
    for proc in jobs:
        proc.join()
    for key in return_dict:
        return_dict[ key ].PassDataToGraph( g )
    GetDirectedDataFromGraph( g, result_filename )

def RunRandomExperiment( g, npy_filename, numb_walks, numb_steps, result_filename ):    
    mutual_Info_Matrix = As.LoadArrayFromFile( npy_filename )
    tools.Shuffle2DMatrix( mutual_Info_Matrix )
    tools.SetNextToItself(end_string, g, mutual_Info_Matrix )
    prob_matrix = InitializeProbabilityMatrix( mutual_Info_Matrix )
    tracker = RandomTheWalks( g, numb_walks, numb_steps, prob_matrix )
    tracker.PassDataToGraph( g )
    GetDirectedDataFromGraph( g, result_filename )

###################### Private Function Section ######################   

def GetProbabilityArray(start, num_nodes, prob_matrix):
    probability = []
    summation = 0
    for i in range(num_nodes):
        prob = prob_matrix[start][i]
        summation += prob
        probability.append(summation)
    return probability

#If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?
#for all random walks

def OneWalk(graph, start, steps, prob_matrix, edgeTracker):
    current = start
    num_nodes = len(graph.vs)
    path = []
    path.append(current)

    increment_vector = tools.CreateArrayOfZeros( len( graph.es ) )
    AB_increment_vector = tools.CreateArrayOfZeros( len( graph.es ) )
    BA_increment_vector = tools.CreateArrayOfZeros( len( graph.es ) )

    for i in range(steps):
        prob_array = GetProbabilityArray(current, num_nodes, prob_matrix)
        next_step = tools.RollRandom(prob_array)
        edge_ID = graph.get_eid(current, next_step)
        increment_vector[edge_ID] += 1
        if ( current < next_step ):
            AB_increment_vector[ edge_ID ] += 1
        else:
            BA_increment_vector[ edge_ID ] += 1
        current = next_step
        path.append(current)

    if (graph.vs[current]["clinic_vars"] == end_string):
        edgeTracker.IncrementTrackerFromList( increment_vector )
        edgeTracker.IncrementABVisitsFromList( AB_increment_vector )
        edgeTracker.IncrementBAVisitsFromList( BA_increment_vector )

    return path

       
def TheWalks( procnum, return_dict, g, times, steps, prob_matrix):
    ExpTracker = ET.EdgeVisitTracker( len( g.es ) )
    for i in range( times ):
        start = random.randint( 0, len(g.vs)-1 )
        OneWalk( g, start, steps, prob_matrix, ExpTracker )
    return_dict[ procnum ] = ExpTracker

def ShowEdges( g , times ):
    for h in range(len(g.vs)):
        for i in range(len(g.vs)):
            ID = g.get_eid(h,i)
            if ( g.es[ID]["Time_Visited"] != ([0]*times)):
                print( g.vs[h]["clinic_vars"], end = "--- " )
                print( g.vs[i]["clinic_vars"], end = ": ")
                print( g.es[ID]["Time_Visited"] )

def GetDirectedDataFromGraph( g, to_filename ):
    data = []
    for e in g.es:
        data.append( [ tools.AverageListValue( e["AB"] ), tools.AverageListValue( e["BA"] ) ] )
    As.ArrayToFile( np.array( data ), to_filename )
    return data


def RandomTheWalks( g, times, steps, prob_matrix ):
    ExpTracker = ET.EdgeVisitTracker( len( g.es ) )
    for i in range( times ):
        start = random.randint( 0, len(g.vs)-1 )
        OneWalk( g, start, steps, prob_matrix, ExpTracker )
    return ExpTracker

def InitializeProbabilityMatrix( mutual_info_matrix ):
    totals = mutual_info_matrix.sum(axis = 1)
    
    size = len( mutual_info_matrix )
    prob_matrix = tools.CreateAdjMatrix(size, size)
    for i in range(size):
        for j in range(size):
            if ( totals[i] == 0 ):
                prob_matrix[i][j] = 0
            else:
                prob_matrix[i][j] = mutual_info_matrix[i][j]/totals[i]
    return prob_matrix