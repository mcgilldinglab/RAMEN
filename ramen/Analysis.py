# Code for analysis and cytoscape

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from networkx import nodes

class HeatmapAction:
    def __init__(self, csv_file, var1, var2, destination_folder=None, var_name_mapping=None):
        self.csv = csv_file
        self.var1 = var1
        self.var2 = var2
        self.destination_folder = destination_folder
        self.var_name_mapping = var_name_mapping or {}

    def enact(self, ignore_values=None):
        print(f"Working on ({self.var1}, {self.var2}).")
        if ignore_values is None:
            ignore_values = []
        plot_heatmap(
            self.csv,
            self.var1,
            self.var2,
            self.var_name_mapping,
            ignore_values,
            destination_folder=self.destination_folder
        )

    def __str__(self):
        return f"Heatmap between: <{self.var1}> and <{self.var2}> saved to {self.destination_folder}"


def reverse_dictionary(dictionary):
    """Reverse inner dictionaries: {var: {discrete: real}} -> {var: {real: discrete}}"""
    new_dictionary = {}
    for var, mappings in dictionary.items():
        new_dictionary[var] = {v: k for k, v in mappings.items()}
    return new_dictionary


def plot_heatmap(csv_file, var1, var2, var_name_mapping, ignore_values, destination_folder=None):
    df = pd.read_csv(csv_file)

    # Use pandas for safe NaN handling (works for strings & numbers)
    variable_1_array = df[var1].replace(ignore_values, np.nan)
    variable_2_array = df[var2].replace(ignore_values, np.nan)

    # Drop rows where either variable is NaN
    valid_df = df.loc[variable_1_array.notna() & variable_2_array.notna(), [var1, var2]].copy()
    valid_df[var1] = try_floating(valid_df[var1])
    valid_df[var2] = try_floating(valid_df[var2])

    # Bin numeric values if necessary
    if should_bin(valid_df[var1]):
        valid_df[var1] = pd.cut(valid_df[var1].astype(float), bins=10, precision=1)
    if should_bin(valid_df[var2]):
        valid_df[var2] = pd.cut(valid_df[var2].astype(float), bins=10, precision=1)

    # Calculate frequency table and percentages
    cross_tab = pd.crosstab(valid_df[var1], valid_df[var2], normalize='index')
    percentage_table = (cross_tab * 100).round(2)

    # Plot heatmap
    plt.figure(figsize=(10, 8))
    sns.set(font_scale=2)
    sns.heatmap(
        percentage_table,
        annot=False,
        cmap='YlGnBu',
        fmt=".2f",
        linewidths=0.5,
        xticklabels=percentage_table.columns,
        yticklabels=percentage_table.index
    )

    plt.xlabel(get_from_mapping(var2, var_name_mapping), fontsize=30)
    plt.ylabel(get_from_mapping(var1, var_name_mapping), fontsize=30)
    plt.title(f"{var1} vs. {var2}", fontsize=30)
    plt.tight_layout()

    # Show plot instead of saving
    plt.show()


def get_from_mapping(key, mapping):
    return mapping.get(key, key)


def should_bin(array):
    """Decide whether numeric array should be binned into categories."""
    if not pd.api.types.is_numeric_dtype(array):
        return False
    return array.nunique() > 10


def try_floating(array):
    """Convert array to numeric if possible; leave strings intact."""
    return pd.to_numeric(array, errors="ignore")


def draw_heatmaps(variables_against_target, additional_pairs, target_node, csv, ignore_values=None):
    if ignore_values is None:
        ignore_values = []

    pairs = [(var, target_node) for var in variables_against_target] + additional_pairs
    for var1, var2 in pairs:
        heatmap_action = HeatmapAction(csv, var1, var2, destination_folder=None)
        heatmap_action.enact(ignore_values)

def get_edge_visits_to_node(visit_list, to_node_str):
    return [
        (entry["node_1"], entry["visits"])
        for entry in visit_list
        if entry["node_2"] == to_node_str
    ]


strength_categories = ["strongest", "strong", "okay", "weaker"]

def make_cytoscape_files(nx_graph, sif_name, noa_name, end_var, classifications, visit_dict = None, keep_factor=1):
    make_sif_file(nx_graph, sif_name, visit_dict, keep_factor)
    make_noa_file(nx_graph, noa_name, visit_dict, end_var, classifications)

def make_sif_file(nx_graph, sif_name, visit_dict, keep_factor):
    sif_file = open(sif_name, "w")
    edges = get_sort_edges_with_visit_dict(nx_graph, visit_dict)
    kept_edges = [edge[0] for edge in edges[0:int(len(edges)*keep_factor)]]

    counter = 0
    splitter = int(len(kept_edges)/4)
    for edge in kept_edges:
        x, y = edge
        string = x + "\t" + strength_categories[min(int(counter / splitter), 3)] + "\t" + y + "\n"
        counter += 1
        sif_file.write(string)
    sif_file.close()

def make_noa_file(nx_graph, noa_name, visit_dict, end_var, classifications, var_name_mapping = {}):
    noa = open(noa_name, 'w')
    noa.write("name = CATEGORY = WEIGHT\n")
    node_tuples = get_sort_nodes_with_visit_dict(nx_graph, visit_dict, end_var)

    for node_tup in node_tuples:
        classification = "other"
        node_str = node_tup[0]
        if node_str in classifications:
            classification = classifications[node_str]
        write_string = get_or_return_key(var_name_mapping, node_str) + " = " + classification + " = " + str(node_tup[1]) + "\n"
        noa.write(write_string)
    noa.close()
    return

def get_sort_edges_with_visit_dict(nx_graph, visit_dict):
    edges_with_visit = []
    for edge in list(nx_graph.edges):
        try:
            edges_with_visit.append((edge, visit_dict[edge]))
        except KeyError:
            print(f"Caught KeyError for edge: {edge}")
            edges_with_visit.append((edge, 0))
    edges_with_visit.sort(key=lambda x: x[1], reverse=True)
    return edges_with_visit

def get_sort_nodes_with_visit_dict(nx_graph, visit_dict, end_var):
    nodes_with_visit = [(node, visit_dict[(node, end_var)]) for node in list(nx_graph.nodes)]
    nodes_with_visit.sort(key=lambda x: x[1], reverse=True)
    return nodes_with_visit

def get_or_return_key(mapping, key):
    try:
        return mapping[key]
    except KeyError:
        return key



if __name__ == "__main__":
    from Ramen import Ramen
    import  networkx as nx

    ramen_bowl = Ramen("long_500.csv", "Long Covid", 0)

    ramen_bowl.random_walk(
        num_walks=50000,
        num_steps=3,
        p_value=0.05,
        correction="no_correction"
    )

    ramen_bowl.genetic_algorithm(
        num_candidates=10,
        end_thresh=0.01,
        mutate_num=100,
        best_cand_num=10,
        bad_reprod_accept=10,
        reg_factor=0.01,
        hard_stop=100,
    )

    # Save for Subsequenet Analysis
    # {
    #     "DATASET_PATH": self.csv_data_name,
    #     "END_VARIABLE": self.end_string,
    #     "RW_NETWORK": self.signif_edges,
    #     "FINAL_NETWORK": list(self.network.edges()),
    #     "RW_EDGE_VISIT": make_edge_visit_payload(self.edge_visit_dict),
    #     "END_VAR_ARRIVALS": self.var_arrival_count_tracker,
    # }
    ramen_results = ramen_bowl.export_ramen_as_dict()

    draw_heatmaps(
        ["Sex at birth:"],
        [],
        "Long Covid",
        "long_500.csv",
        ["ERROR", "nan", "no data", "<4", ">150*", "LESS THAN 5", "LESS THAN 0.4", -999],
    )

    draw_heatmaps(
        ["BMI:"],
        [],
        "Long Covid",
        "long_500.csv",
        ["ERROR", "nan", "no data", "<4", ">150*", "LESS THAN 5", "LESS THAN 0.4", -999],
    )

    long_ramen_graph = nx.DiGraph(ramen_results["FINAL_NETWORK"])
    long_rw_visits = ramen_results["RW_EDGE_VISIT"]

    make_sif_file(long_ramen_graph,
                  "long.sif",
                  long_rw_visits,
                  1)
    make_noa_file(long_ramen_graph,
                  "long.noa",
                  long_rw_visits,
                  "Long Covid",
                  {})  # If you want to categorize variable a dictionary e.g. {'Long Covid' : 'disease'}