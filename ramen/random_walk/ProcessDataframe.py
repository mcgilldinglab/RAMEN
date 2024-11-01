import pandas as pd
import numpy as np
from .VectorizeDataframe import vectorize_dataframe
from .BadVariableEliminater import drop_bad_vars

def process_data_frame(data_file, bad_var_threshold = 500):
    dataframe = pd.read_csv(data_file)
    dataframe = convert_nan_to_999_for_df(dataframe)
    print("Starting removing vars with too few values, vectorizing dataframe, and initializing mutual information matrix, this might take a few minutes.")    
    start_col = len(dataframe.columns)
    drop_bad_vars(dataframe, bad_var_threshold)
    dataframe, mapping = vectorize_dataframe(dataframe)
    end_col = len(dataframe.columns)
    print("Removed " + str(start_col - end_col) + " variables because of insufficient data. If deleted too many, please adjust the bad_var_threshold")
    return dataframe, mapping

###################### Private Function Section ######################   
    
def convert_nan_to_999_for_df(dataframe):
    new_data_dict = {}
    variables = dataframe.columns
    for i in range(len(variables)):
        liste = list(dataframe[ variables[i] ])
        new_data_dict[ variables[i] ] = convert_nan_to_999_for_array(liste)
    new_dataframe = pd.DataFrame(new_data_dict)
    return new_dataframe

def convert_nan_to_999_for_array(liste):
    for i in range(len(liste)):
        if (type(liste[ i ]) == str):
            continue
        if (np.isnan(liste[i])):
            liste[i] = -999
    return liste
