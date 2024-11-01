from .Discretization import discretize
import pandas as pd

def vectorize_dataframe(dataframe):
    new_data_dict = {}
    discr_var_dic = {}
    variables = dataframe.columns
    for i in range(len(variables)):
        variable_values = list(dataframe[variables[i]])
        new_data_dict[variables[i]] = convert_variable_to_discrete(variable_values, variables[i], discr_var_dic)
    new_data_frame = pd.DataFrame(new_data_dict)
    
    return new_data_frame, discr_var_dic

###################### Private Function Section ######################

def convert_variable_to_discrete(variable_values, var_name, discr_var_dic):
    if is_variable_continuous(variable_values):
        values, mapping = discretize(variable_values)
        discr_var_dic[var_name] = mapping
        return values
    else:
        value = 0
        tracker = { "-999" : -999, "-999.0" : -999 }
        newlist = []
        for i in range(len(variable_values)):
            stringBuffer = str(variable_values[i])
            if (stringBuffer not in tracker):
                tracker[stringBuffer] = value
                newlist.append(tracker[stringBuffer])
                value += 1
            else:
                newlist.append(tracker[stringBuffer])
        tracker.pop("-999")
        tracker.pop("-999.0")
        discr_var_dic[var_name] = tracker
        return newlist

def is_variable_continuous(variable_values):
    valueSet = set()
    for i in range(len(variable_values)):
        if (type(variable_values[i]) == float) and (variable_values[i] != -999):
            return True
        valueSet.add(variable_values[i])
    numberBool = False
    valueList = list(valueSet)
    for j in range(len(valueList)):
        if (type(valueList[j]) != str and valueList[j] != -999):
            numberBool = True
            break
    if (len(valueSet) > 10 and numberBool):
        return True
    return False