import pandas as pd
from RandomWalk.ProcessDataframe import ProcessDataframeNoSave
from RandomWalk.MutualInformation import MakeMutualInfoMatrixNoSave
from RandomWalk.InitializeGraph import InitializeRandomWalkGraph
from RandomWalk.RandomWalk import RunExperiments, RunExperiments, RunRandomExperiment
from RandomWalk.Distribution import FitAndExtractSignificantEdges
from GeneticAlgorithm.GeneticAlgorithmLauncher import StructuredLearningRun
from GeneticAlgorithm.PickleSaver import Pickle, UnPickle

class Ramen( object ):
    def __init__( self, csv_data = None, ref_save_name = "var_val_ref.pickle", end_string = "", bad_var_threshold = 500 ):
        assert( csv_data is not None )
        self.df = ProcessDataframeNoSave( csv_data, ref_save_name, bad_var_threshold )
        self.mutual_info_array = MakeMutualInfoMatrixNoSave( self.df )
        self.signif_edges = None
        self.network = None
        self.end_string = end_string
        
    def random_walk( self, num_exp = 10, num_walks = 50000, num_steps = 7, p_value = 0.05, mode = "default" ):
        assert( self.end_string in list( self.df.columns ) )
        g_rand = InitializeRandomWalkGraph( self.df )
        g = InitializeRandomWalkGraph( self.df )
        result_rand = RunRandomExperiment( g_rand, self.mutual_info_array, num_walks, num_steps, self.end_string )
        result = RunExperiments( g, self.mutual_info_array, num_exp, num_walks, num_steps, self.end_string )
        self.signif_edges = FitAndExtractSignificantEdges( self.df, result, result_rand, p_value, mode )
    
    def genetic_algorithm( self, num_candidates = 10, end_thresh = 0.01, mutate_num = 100, best_cand_num = 10, bad_reprod_accept = 10, reg_factor = 0.01, hard_stop = 100 ):
        assert ( self.signif_edges is not None )
        self.network = StructuredLearningRun( self.df, self.signif_edges, num_candidates, end_thresh, mutate_num, best_cand_num, bad_reprod_accept, reg_factor, hard_stop )
    
    def pickle_signif_edges( self, filename ):
        assert( self.signif_edges is not None )
        Pickle( self.signif_edges, filename )
    
    def load_signif_edges_pickle( self, filename ):
        self.signif_edges = UnPickle( filename )
    
    def pickle_final_network( self, filename ):
        assert( self.network is not None )
        Pickle( self.network, filename )
    
    def set_end_string( self, end_string ):
        self.end_string = end_string
        
        