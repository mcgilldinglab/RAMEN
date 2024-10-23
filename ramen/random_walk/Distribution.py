from .InitializeGraph import initialize_random_walk_graph
from igraph import*
import numpy as np
from scipy.stats import nbinom
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
import copy

def fit_and_extract_significant_edges(dataframe, rw_result, random_result, p_value = 0.05, mode = "default"):
    g = make_distribution_graph(dataframe, rw_result)
    edge_visit_dict = make_edge_visit_dictionary(g)

    (n, p) = get_distribution_parameters_dir(random_result)

    p_values = get_p_values(g, n, p)
    
    if (mode == "fdr"):
        fdr_input = copy.deepcopy(p_values)
        fdr_p_values = fdr_correction(fdr_input)
        return significant_edges_to_list(g, fdr_p_values, p_value), edge_visit_dict
    else:
        not_input = copy.deepcopy(p_values)
        return significant_edges_to_list(g, not_input, p_value), edge_visit_dict

def get_distribution_parameters_dir(pre_data):
    data = np.array(pre_data).flatten()
    X = np.ones_like(data)
    res = sm.NegativeBinomial(data, X).fit(start_params = [1,1])
    p = 1/(1 + np.exp(res.params[0])*res.params[1])
    n = np.exp(res.params[0])*p/(1-p)
    return (n, p)

def add_edge_to_sorted_array(edge, edge_list):
    for i in range(len(edge_list)):
        if (edge[1] < edge_list[i][1]):
            edge_list.insert(i, edge)
            return
    edge_list.append(edge)

def significant_edges_to_list(g, p_values, threshold):
    edge_tups = []
    
    visited = set()
    for h in range(len(g.vs)):
        for i in range(len(g.vs)):
            ID = g.get_eid(h,i)

            if ((ID in visited) or (i == h)):
                continue
            visited.add(ID)

            if (p_values[ID][0] < threshold):
                string = ""
                string += g.vs[h]["clinic_vars"]
                string += "--- "
                string += g.vs[i]["clinic_vars"]
                string += ": "
                string += str(p_values[ID][0])
                string += ";;;TimesVisited: "
                string += str(g.es[ID]["AB"])
                string += "\n"

                to_add = (string, p_values[ID][0])
                add_edge_to_sorted_array(to_add, edge_tups)

            if (p_values[ID][1] < threshold):
                string = ""
                string += g.vs[i]["clinic_vars"]
                string += "--- "
                string += g.vs[h]["clinic_vars"]
                string += ": "
                string += str(p_values[ID][1])
                string += ";;;TimesVisited: "
                string += str(g.es[ID]["BA"])
                string += "\n"

                to_add = (string, p_values[ID][1])
                add_edge_to_sorted_array(to_add, edge_tups)
    signif_edges = []
    for edge in edge_tups:
        signif_edges.append(edge[0])
    return signif_edges

def get_p_values(g, n, p):
    p_values = []
    for m in range(len(g.es)):
        p_values.append([0, 0])

    visited = set()

    for h in range(len(g.vs)):
        for i in range(len(g.vs)):
            ID = g.get_eid(h,i)

            if (ID in visited):
                continue

            p_value1 = 1 - nbinom.cdf(g.es[ID]["AB"] , n, p)
            p_value2 = 1 - nbinom.cdf(g.es[ID]["BA"] , n, p)

            p_values[ID][0] = p_value1
            p_values[ID][1] = p_value2

    return np.array(p_values)


def fdr_correction(array):
    to_compute = np.reshape(array, array.shape[0]*array.shape[1])
    corrected = multipletests(to_compute, method = "fdr_bh")
    return np.reshape(corrected[1], (array.shape[0], array.shape[1]))    


def make_distribution_graph(dataframe, visit_array):
    g = initialize_random_walk_graph(dataframe)
    for i in range(len(g.es)):
        try:
            g.es[i]["AB"] = visit_array[i][0]
            g.es[i]["BA"] = visit_array[i][1]
        except:
            print(str(i) + " " + "failed")
    return g

def make_edge_visit_dictionary(graph):
    edge_dict = {}
    for edge in graph.es:
        node1 = graph.vs[edge.source]["clinic_vars"]
        node2 = graph.vs[edge.target]["clinic_vars"]

        edge_dict[(node1, node2)] = edge['AB']
        edge_dict[(node2, node1)] = edge['BA']
    return edge_dict

