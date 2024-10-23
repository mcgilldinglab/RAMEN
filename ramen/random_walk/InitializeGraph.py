from igraph import*

def initialize_mutual_info_matrix_graph(dataframe):
    g = Graph()

    clinic_vars = list(dataframe.columns)
    slicing_index = get_start_var_index(clinic_vars)
    g.add_vertices(len(clinic_vars[slicing_index:]))
    g.vs["clinic_vars"] = clinic_vars[slicing_index:]

    attach_vectors(clinic_vars[slicing_index:], dataframe, g)

    create_edges(g)

    return g

def initialize_random_walk_graph(dataframe):
    g = Graph()
    clinic_vars = list(dataframe.columns)
    slicing_index = get_start_var_index(clinic_vars)
    g.add_vertices(len(clinic_vars[slicing_index:]))
    g.vs["clinic_vars"] = clinic_vars[slicing_index:]

    create_edges(g)

    return g

###################### Private Function Section ######################   

def attach_vectors(variables, dataframe, g):
    liste = []
    for var in variables:
        liste.append(list(dataframe[var]))
    g.vs["Vector"] = liste

def create_vector(variable, dataframe):
    return list(dataframe[variable])

def create_edges(g):
    added = set()
    for h in range(len(g.vs)):
        for i in range(len(g.vs)):
            if (not((h,i) in added or (i,h) in added)):
                g.add_edges([(h, i)])
                ID = g.get_eid(h,i)
                g.es[ID]["Time_Visited"] = []
                g.es[ID]["AB"] = []
                g.es[ID]["BA"] = []
                added.add((h,i))

def get_start_var_index(var_name_list):
    for i in range(len(var_name_list)):
        if "Unnamed" not in str(var_name_list[i]):
            return i
    return -1