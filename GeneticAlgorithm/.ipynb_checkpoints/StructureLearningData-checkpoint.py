import pandas as pd
import tools as tools
import numpy as np

def Convert( liste ):
    converted = tools.ConvertToVector( liste, "bobS" )
    for i in range( len( converted ) ):
        if ( int(converted[i]) == -999 ):
            converted[i] = np.nan
    return converted

def GetStructureLearningDF( dataframe, variables ):
    new_data_dict = {}

    for i in range( len( variables ) ):
        liste = list( dataframe[ variables[i] ] )
        new_data_dict[ variables[i] ] = Convert( liste )
    new_data_frame = pd.DataFrame( new_data_dict )
    new_data_frame.to_csv( "ScoringDataframe.csv" )        