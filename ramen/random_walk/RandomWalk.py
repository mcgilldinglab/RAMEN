import multiprocessing
import random

import numpy as np

from .ExpEdgeVisitTracker import EdgeVisitTracker
import copy

from collections import defaultdict


def run_experiments(g, mutual_info_matrix, times, numb_walks, numb_steps, end_string):
    mut_info = copy.deepcopy(mutual_info_matrix)
    nullify_out_probability(end_string, g, mut_info)
    prob_matrix = initialize_probability_matrix(mut_info)

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(times):
        p = multiprocessing.Process(target = the_walks, args = (i, return_dict, g, numb_walks, numb_steps, prob_matrix, end_string))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    end_var_arrival_counters = defaultdict(int)
    for key in return_dict:
        return_dict[key].pass_data_to_graph(g)
        for var, value in return_dict[key].end_var_arrival_tracker.items():
            end_var_arrival_counters[var] += value
    return get_directed_data_from_graph(g), dict(end_var_arrival_counters)

def run_random_experiments(g, mutual_info_matrix, numb_walks, numb_steps, end_string):
    mut_info = copy.deepcopy(mutual_info_matrix)
    shuffle_2d_matrix(mut_info)
    nullify_out_probability(end_string, g, mut_info)
    prob_matrix = initialize_probability_matrix(mut_info)
    tracker = random_the_walks(g, numb_walks, numb_steps, prob_matrix, end_string)
    tracker.pass_data_to_graph(g)
    return get_directed_data_from_graph(g)

###################### Private Function Section ######################   

def the_walks(procnum, return_dict, g, times, steps, prob_matrix, end_string):
    edge_tracker = EdgeVisitTracker(len(g.es), g.vs.indices)
    for i in range(times):
        start = random.randint(0, len(g.vs)-1)
        one_walk(g, start, steps, prob_matrix, edge_tracker, end_string)
    return_dict[procnum] = edge_tracker

def get_directed_data_from_graph(g):
    data = []
    for e in g.es:
        data.append([compute_mean_for_list(e["AB"]), compute_mean_for_list(e["BA"])])
    return data

def random_the_walks(g, times, steps, prob_matrix, end_string):
    ExpTracker = EdgeVisitTracker(len(g.es), g.vs.indices)
    for i in range(times):
        start = random.randint(0, len(g.vs)-1)
        one_walk(g, start, steps, prob_matrix, ExpTracker, end_string)
    return ExpTracker

def one_walk(graph, start, steps, prob_matrix, edge_tracker, end_string):
    current = start
    num_nodes = len(graph.vs)

    vector_length = len(graph.es)
    increment_vector = np.zeros(vector_length)
    ab_increment_vector = np.zeros(vector_length)
    ba_increment_vector = np.zeros(vector_length)

    for i in range(steps):
        prob_array = get_probability_array(current, num_nodes, prob_matrix)
        next_step = roll_random(prob_array)
        edge_ID = graph.get_eid(current, next_step)
        increment_vector[edge_ID] += 1
        if current < next_step:
            ab_increment_vector[edge_ID] += 1
        else:
            ba_increment_vector[edge_ID] += 1
        current = next_step

    if graph.vs[current]["clinic_vars"] == end_string:
        edge_tracker.increment_tracker_from_list(increment_vector)
        edge_tracker.increment_AB_visits_from_list(ab_increment_vector)
        edge_tracker.increment_BA_visits_from_list(ba_increment_vector)
        edge_tracker.register_end_var_arrival(start)


def get_probability_array(start, num_nodes, prob_matrix):
    probability = []
    summation = 0
    for i in range(num_nodes):
        prob = prob_matrix[start][i]
        summation += prob
        probability.append(summation)
    return probability

def initialize_probability_matrix(mutual_info_matrix):
    totals = mutual_info_matrix.sum(axis = 1)
    
    size = len(mutual_info_matrix)
    prob_matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if (totals[i] == 0):
                prob_matrix[i][j] = 0
            else:
                prob_matrix[i][j] = mutual_info_matrix[i][j]/totals[i]
    return prob_matrix

def compute_mean_for_list(value_list):
    return np.mean(np.array(value_list))

def nullify_out_probability(clinic_var, graph, prob_array):
    var_index = -1
    for i in range(len(graph.vs)):
        if graph.vs[i]["clinic_vars"] == clinic_var:
            var_index = i

    if (var_index == -1):
        raise Exception("Clinical var not found")

    for i in range(len(prob_array[var_index])):
        prob_array[var_index][i] = 0
    prob_array[var_index][var_index] = 1

def shuffle_2d_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            randomi = random.randint(0, len(matrix)-1)
            randomj = random.randint(0, len(matrix[i])-1)

            temp = matrix[i][j]
            matrix[i][j] = matrix[randomi][randomj]
            matrix[randomi][randomj] = temp


def roll_random(interval):
    randomRoll = random.uniform(0, interval[len(interval)-1])
    for i in range(len(interval)):
        if (randomRoll <= interval[i]):
            return i
    return -1
