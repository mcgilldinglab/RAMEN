from .random_walk.ProcessDataframe import ProcessDataframeNoSave
from .random_walk.MutualInformation import MakeMutualInfoMatrixNoSave
from .random_walk.InitializeGraph import InitializeRandomWalkGraph
from .random_walk.RandomWalk import RunExperiments, RunExperiments, RunRandomExperiment
from .random_walk.Distribution import FitAndExtractSignificantEdges
from .genetic_algorithm.GeneticAlgorithmLauncher import StructuredLearningRun
from .genetic_algorithm.PickleSaver import Pickle, UnPickle


class Ramen( object ):
    def __init__( self, csv_data = None, ref_save_name = "var_val_ref.pickle", end_string = "", min_values = 500 ):
        """
        Constructor of the Ramen Object, which will be used to run random walk and genetic algorithm.

        Args:
            csv_data (str): path to the data in csv form.
            ref_save_name (str): when the csv is discretized, this is the mapping of the discrete values to the actual values.
            end_string (str): the destination variable of absorbing random walk.

        Returns:
            type: Ramen object

        Raises:
            Exception: if csv_data is not provided, and when the end_string is not in the dataset.
        """

        if (csv_data is None):
            raise Exception("csv_data cannot be None.")
        df, var_ref = ProcessDataframeNoSave( csv_data, ref_save_name, min_values )
        self.df = df
        self.var_ref = var_ref
        self.mutual_info_array = MakeMutualInfoMatrixNoSave( self.df )
        self.signif_edges = None
        self.network = None
        self.end_string = end_string
        if (self.end_string not in list(self.df.columns)):
            raise Exception("couldn't find end_string in the csv columns.")
        
        
    def random_walk( self, num_exp = 10, num_walks = 50000, num_steps = 7, p_value = 0.05, correction = "no_correction" ):
        """
        Method to begin the absorbing random walk once the Ramen object is initialized. The significant edges will be stored in ramen_object.signif_edges.

        Args:
            num_exp (int): the number of random walk experiments. (default value is 10)
            num_walks (int): the number of random walks per experiment. (default value is 50000)
            num_steps (int): the number of steps per random walk. (default value is 7)
            p_value (float): the cutoff value to determine significance of edge visits. An edge is significant if it is below p_value. (default value is 0.05)
            correction (str): choose correction method on the significant edges p-values. (supported correction: ["fdr", "no_correction"])

        Returns:
            type: None
        """

        g_rand = InitializeRandomWalkGraph( self.df )
        g = InitializeRandomWalkGraph( self.df )
        result_rand = RunRandomExperiment( g_rand, self.mutual_info_array, num_walks, num_steps, self.end_string )
        result = RunExperiments( g, self.mutual_info_array, num_exp, num_walks, num_steps, self.end_string )
        self.signif_edges = FitAndExtractSignificantEdges( self.df, result, result_rand, p_value, correction )

    
    def genetic_algorithm( self, num_candidates = 10, end_thresh = 0.01, mutate_num = 100, best_cand_num = 10, bad_reprod_accept = 10, reg_factor = 0.01, hard_stop = 100 ):
        """
        Method to begin the genetic algorithm once random walk is complete. The result neetwork will be stored in ramen_object.network.

        Args:
            num_candidates (int): number of initial candidates. (default value is 10)
            end_thresh (int): if the score increase between generations are continuously below end_thresh, then it converges. (default value is 0.01)
            mutate_num (int): the number of mutations per intermediate candidate after cross breeding. (default value is 100)
            best_cand_num (int): the number of top candidates kept after a generation. (default value is 10)
            bad_reprod_accept (int): the number of generations with < end_thresh increase before convergeance. (default value is 10)
            reg_factor (float): score penalty per edge (default value is 0.01)
            hard_stop (int): maximum number of generations (default value is 100)
        Returns:
            type: None

        Raises:
            Exception: raised when the significant edges are empty.
        """

        if (self.signif_edges is None):
            raise Exception("Cannot start genetic algorithm before running random walk.")
        self.network = StructuredLearningRun( self.df, self.signif_edges, num_candidates, end_thresh, mutate_num, best_cand_num, bad_reprod_accept, reg_factor, hard_stop )
    

    def pickle_signif_edges( self, filename = "signif_edges.pickle"):
        """
        Method to save the significant edges to a pickle object.

        Args:
            filename (str): name of the save file (Default value is "signif_edges.pickle")
        Returns:
            type: None

        Raises:
            Exception: raised when genetic algorithm hasn't been ran yet.
        """
        if (self.signif_edges is None):
            raise Exception("significant edges is None.")
        Pickle( self.signif_edges, filename )
    

    def load_signif_edges_pickle( self, filename ):
        """
        Method to load the significant edges from a pickle object.

        Args:
            filename (str): name of the save file.
        Returns:
            type: None
        """
        self.signif_edges = UnPickle( filename )
    

    def pickle_final_network( self, filename = "final_net.pickle"):
        """
        Method to save the final network as a NetworkX DiGraph.

        Args:
            filename (str): name of the save file.
        Returns:
            type: None
        Raises:
            Exception: raised when the final network is None.
        """
        if (self.network is None):
            raise Exception("network is None.")
        Pickle( self.network, filename )
    

    def set_end_string( self, end_string ):
        """
        Method to modify the end_string of absorbing random walk.

        Args:
            end_string (str): name of end variable.
        Returns:
            type: None
        """
        self.end_string = end_string


    def get_signif_edges(self):
        """
        Return a copy of the significant edges, or None if there are None.

        Args:
            None.
        Returns:
            type: list<tup<str, str>>
        """
        if (self.get_signif_edges is None):
            return None
        return self.signif_edges.copy()
    

    def set_signif_edges(self, signif_edges):
        """
        Set the significant edges.

        Args:
            signif_edges (list<tup<str, str>>): significant edges to set.
        Returns:
            type: None
        """
        self.signif_edges = signif_edges
    

    def get_var_ref(self):
        """
        get the discrete to variable value reference.

        Args:
            None
        Returns:
            type: dict
        """
        return self.var_ref
    
    
    def get_mutual_info_array(self):
        """
        Get the mutual information matrix.

        Args:
            None
        Returns:
            type: numpy.array
        """
        return self.mutual_info_array
