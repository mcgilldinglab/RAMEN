import numpy as np
from sklearn.metrics import mutual_info_score
from .InitializeGraph import initialize_mutual_info_matrix_graph

def make_mutual_info_matrix_no_save(df):
    g = initialize_mutual_info_matrix_graph(df)
    matrix = np.array(initialize_mutual_info_matrix(g))
    print("done")
    return matrix

###################### Private Function Section ######################

def initialize_mutual_info_matrix(g):
    vector_matrix = generate_graph_vector_matrix(g)
    random_var1 = np.random.randint(0, 10, vector_matrix.shape[1])
    random_var2 = np.random.randint(0, 10, vector_matrix.shape[1])
    mi_tracker = []
    for i in range(100):
        mi_tracker.append(compute_pair_mi_for_vars(random_var1, random_var2))
    mi_tracker.sort()
    lower_bound = mi_tracker[-5]
    mi_matrix = compute_pair_mi_for_vars(vector_matrix, lower_bound)
    return mi_matrix

def generate_graph_vector_matrix(g):
    matrix = []
    for i in range(len(g.vs)):
        matrix.append(g.vs[i]["Vector"])
    return np.array(matrix)

def compute_pair_mi_for_vars(variables, lower_bound = 0):
    size = len(variables)
    mutual_info_matrix = np.zeros((size, size))

    for i in range(size):
        current_var = variables[i]
        for j in range(size):
            inner_var = variables[j]
            mutual_info_matrix[i][j] = max(compute_pair_mi(current_var, inner_var), lower_bound)
    return mutual_info_matrix

def compute_pair_mi(var1, var2):
    mask = (var1 != -999) * (var2 != -999)
    x1 = var1[mask]
    x2 = var2[mask]
    if len(x1) == 0:
        return 0
    else: 
        return mutual_info_score(x1, x2)
