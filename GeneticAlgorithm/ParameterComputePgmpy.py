import networkx as nx
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
import pickle

class ParameterComputer( object ):
    def __init__( self, translate_dic_pickle, dataframe, g ):
        file = open( translate_dic_pickle, "rb" )
        self.translate_dic = pickle.load( file )
        self.graph = g
        self.dataframe = dataframe
    def ComputeProbability( self, source, source_value, target, target_value ):
        prob = None
        try:
            prob = self.CalculateProbability( source, source_value, target, target_value )
        except:
            print( "Something went wrong when computing probability" )
        return prob
    
    def CalculateProbability( self, source, source_value, target, target_value ):
        prob_cpd = ComputeProbTable( self.dataframe, self.graph, source, target )
        if ( source not in self.translate_dic ):
            val_source = int( source_value )
        else:
            val_source = self.translate_dic[ source ][ source_value ]
        val_target = self.translate_dic[ target ][ target_value ]
        return prob_cpd.get_values()[ val_target ][ val_source ]

################################ Private Section #################################

def ComputeProbTable( dataframe, g, source, target ):
    model = GenerateSubBayesianNetwork( g, source, target )
    #model = nx.relabel_nodes( model, mapping )
    cpd_A = MaximumLikelihoodEstimator( model, dataframe ).estimate_cpd( target )
    marginalize_list = []
    for i in range( len( cpd_A.variables ) ):
        if ( ( cpd_A.variables[ i ] != source ) and ( cpd_A.variables[ i ] != target ) ):
            marginalize_list.append( cpd_A.variables[ i ] )
    cpd_A.marginalize( marginalize_list )
    print( cpd_A.get_values() )
    return cpd_A

def GenerateSubBayesianNetwork( g, source, target ):
    edges = set()
    all_paths = nx.all_simple_paths( g, source, target )
    for path in all_paths:
        for i in range( len( path ) - 1 ):
            edges.add( ( path[i], path[i+1] ) )
    return BayesianNetwork( list( edges ) )
            