
def drop_bad_vars(dataframe, threshhold = 500):
    to_remove = get_vars_with_insufficient_values(dataframe, threshhold)
    dataframe.drop(to_remove, inplace = True, axis = 1)

def count_non_missing_values(value_list):
    counter = 0
    for i in range(len(value_list)):
        if str(value_list[i]) != "-999" and str(value_list[i]) != "-999.0":
            counter += 1
    return counter

def get_vars_with_insufficient_values(dataframe, threshold):
    vars = []
    for var in dataframe.columns:
        values = dataframe[var]
        filled_values = count_non_missing_values(values)
        if filled_values < threshold:
            vars.append(var)
    return vars
