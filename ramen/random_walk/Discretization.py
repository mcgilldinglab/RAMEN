import numpy as np

def discretize(variable_values):
    non_nan_indices = get_non_missing_value_indices(variable_values)
    possible_values = get_all_possible_values(variable_values, non_nan_indices)

    xmax = int(max(possible_values)) + 1
    xmin = int(min(possible_values))
    
    bins_mapping = {}
    bins = build_bins(xmin, xmax, 10)
    for i in range(len(bins) - 1):
        bins_mapping[(bins[i], bins[i + 1])] = i
    discretized = list(np.digitize(possible_values, bins))

    update_variable_values(variable_values, non_nan_indices, discretized)

    return variable_values, bins_mapping

###################### Private Function Section ######################

def build_bins(start, end, num_bins):
    increment = (end - start)/num_bins
    current = start
    bins = []
    for i in range(num_bins + 1):
        bins.append(current)
        current += increment
    return bins

def update_variable_values(variable_values, indices, complete_values):
    for i in range(len(complete_values)):
        variable_values[indices[i]] = complete_values[i]

def get_non_missing_value_indices(values):
    indices = []
    for i in range(len(values)):
        if (values[i] != -999):
            indices.append(i)
    return indices

def get_all_possible_values(variable_values, indices):
    values = []
    for i in range(len(indices)):
        values.append(variable_values[indices[i]])
    return values
