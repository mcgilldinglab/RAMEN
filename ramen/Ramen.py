from .random_walk.ProcessDataframe import process_data_frame
from .random_walk.MutualInformation import make_mutual_info_matrix_no_save
from .random_walk.InitializeGraph import initialize_random_walk_graph
from .random_walk.RandomWalk import run_experiments, run_random_experiments
from .random_walk.Distribution import fit_and_extract_significant_edges
from .genetic_algorithm.GeneticAlgorithmLauncher import StructuredLearningRun
from .genetic_algorithm.PickleSaver import Pickle, UnPickle


class Ramen(object):
    def __init__(self, csv_data = None, end_string = "", min_values = 0):
        if (csv_data is None):
            raise Exception("csv_data cannot be None.")
        df, var_ref = process_data_frame(csv_data, min_values)
        self.df = df
        self.var_ref = var_ref
        self.mutual_info_array = make_mutual_info_matrix_no_save(self.df)
        self.signif_edges = None
        self.network = None
        self.edge_visit_dict = None
        self.end_string = end_string
        if self.end_string not in list(self.df.columns):
            raise Exception("couldn't find end_string in the csv columns.")
        
        
    def random_walk(self, num_exp = 10, num_walks = 50000, num_steps = 7, p_value = 0.05, correction = "no_correction"):
        g_rand = initialize_random_walk_graph(self.df)
        g = initialize_random_walk_graph(self.df)
        result_rand = run_random_experiments(g_rand, self.mutual_info_array, num_walks, num_steps, self.end_string)
        result = run_experiments(g, self.mutual_info_array, num_exp, num_walks, num_steps, self.end_string)
        signif_edges, edge_visits_dic = fit_and_extract_significant_edges(self.df, result, result_rand, p_value, correction)
        self.signif_edges = signif_edges
        self.edge_visit_dict = edge_visits_dic

    
    def genetic_algorithm(self, num_candidates = 10, end_thresh = 0.01, mutate_num = 100, best_cand_num = 10, bad_reprod_accept = 10, reg_factor = 0.01, hard_stop = 100):
        if self.signif_edges is None:
            raise Exception("Cannot start genetic algorithm before running random walk.")
        self.network = StructuredLearningRun(self.df, self.signif_edges, num_candidates, end_thresh, mutate_num, best_cand_num, bad_reprod_accept, reg_factor, hard_stop)
    

    def pickle_signif_edges(self, filename = "signif_edges.pickle"):
        if self.signif_edges is None:
            raise Exception("significant edges is None.")
        Pickle(self.signif_edges, filename)
    

    def load_signif_edges_pickle(self, filename):
        self.signif_edges = UnPickle(filename)
    

    def pickle_final_network(self, filename = "final_net.pickle"):
        if self.network is None:
            raise Exception("network is None.")
        Pickle(self.network, filename)


    def pickle_var_ref(self, filename = "var_ref.pickle"):
        if self.var_ref is None:
            raise Exception("no variable reference.")
        Pickle(self.var_ref, filename)


    def pickle_edge_visits(self, filename = "edge_visits.pickle"):
        if self.edge_visit_dict is None:
            raise Exception("no variable reference.")
        Pickle(self.edge_visit_dict, filename)


    def set_end_string(self, end_string):
        self.end_string = end_string


    def get_signif_edges(self):
        if self.get_signif_edges is None:
            return None
        return self.signif_edges.copy()


    def get_edge_visit_dict(self):
        if self.edge_visit_dict is None:
            return None
        return self.edge_visit_dict


    def set_signif_edges(self, signif_edges):
        self.signif_edges = signif_edges
    

    def get_var_ref(self):
        return self.var_ref
    
    
    def get_mutual_info_array(self):
        return self.mutual_info_array
        