from .random_walk.ProcessDataframe import process_data_frame
from .random_walk.MutualInformation import make_mutual_info_matrix_no_save
from .random_walk.InitializeGraph import initialize_random_walk_graph
from .random_walk.RandomWalk import run_experiments, run_random_experiments
from .random_walk.Distribution import fit_and_extract_significant_edges
from .genetic_algorithm.GeneticAlgorithmLauncher import StructuredLearningRun
import networkx as nx


class Ramen(object):
    def __init__(self, csv_data = "", end_string = "", min_values = 0):
        if csv_data == "":
            raise Exception("csv_data cannot be Empty.")
        df, var_ref = process_data_frame(csv_data, min_values)
        self.csv_data_name = csv_data
        self.df = df
        self.var_ref = var_ref
        self.mutual_info_array = make_mutual_info_matrix_no_save(self.df)
        self.signif_edges = []
        self.network = nx.DiGraph()
        self.edge_visit_dict = {}
        self.end_string = end_string
        self.var_arrival_count_tracker = {}
        if self.end_string not in list(self.df.columns):
            raise Exception("couldn't find end_string in the csv columns.")
        
        
    def random_walk(self, num_exp = 10, num_walks = 50000, num_steps = 7, p_value = 0.05, correction = "no_correction"):
        g_rand = initialize_random_walk_graph(self.df)
        g = initialize_random_walk_graph(self.df)
        result_rand = run_random_experiments(g_rand, self.mutual_info_array, num_walks, num_steps, self.end_string)
        result, end_var_arrivals = run_experiments(g, self.mutual_info_array, num_exp, num_walks, num_steps, self.end_string)
        signif_edges, edge_visits_dic = fit_and_extract_significant_edges(self.df, result, result_rand, p_value, correction)

        self.var_arrival_count_tracker = construct_end_arrival_dict(g, end_var_arrivals)
        self.signif_edges = signif_edges
        self.edge_visit_dict = edge_visits_dic

    
    def genetic_algorithm(self, num_candidates = 10, end_thresh = 0.01, mutate_num = 100, best_cand_num = 10, bad_reprod_accept = 10, reg_factor = 0.01, hard_stop = 100):
        if len(self.signif_edges) == 0:
            raise Exception("Cannot start genetic algorithm before running random walk.")
        self.network = StructuredLearningRun(self.df, self.signif_edges, num_candidates, end_thresh, mutate_num, best_cand_num, bad_reprod_accept, reg_factor, hard_stop)


    def export_ramen_as_dict(self):
        return {
            "DATASET_PATH": self.csv_data_name,
            "END_VARIABLE": self.end_string,
            "VAR_REF": self.var_ref,
            "RW_NETWORK": self.signif_edges,
            "FINAL_NETWORK": list(self.network.edges()),
            "RW_EDGE_VISIT": self.edge_visit_dict,
            "END_VAR_ARRIVALS" : self.var_arrival_count_tracker,
        }


    def set_end_string(self, end_string):
        self.end_string = end_string


    def get_signif_edges(self):
        return self.signif_edges.copy()


    def get_edge_visit_dict(self):
        return self.edge_visit_dict


    def set_signif_edges(self, signif_edges):
        self.signif_edges = signif_edges
    

    def get_var_ref(self):
        return self.var_ref
    
    
    def get_mutual_info_array(self):
        return self.mutual_info_array


def construct_end_arrival_dict(g, end_var_arrival_tracker):
    var_name_to_arrival_count = {}
    for var_index in end_var_arrival_tracker:
        var_name_to_arrival_count[g.vs[var_index]["clinic_vars"]] = end_var_arrival_tracker[var_index]
    return var_name_to_arrival_count
