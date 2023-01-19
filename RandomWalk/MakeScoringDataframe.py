import tools
import numpy as np
import pandas as pd

def Convert( liste ):
    for i in range( len( liste ) ):
        if ( int(liste[i]) == -999 ):
            liste[i] = np.nan
    return liste


def GetStructureLearningDF( dataframe, variables, to_name ):
    new_data_dict = {}

    for i in range( len( variables ) ):
        liste = list( dataframe[ variables[i] ] )
        new_data_dict[ variables[i] ] = Convert( liste )
    new_data_frame = pd.DataFrame( new_data_dict )
    new_data_frame.to_csv( to_name )
    
#Use Cases

# if __name__ == "__main__":
#     dataframe  = pd.read_csv( "ThinnedDataCleaned1.csv" )
#     vars = list( dataframe.columns )
#     variables = vars[ 3: ]
#     GetStructureLearningDF( dataframe, variables, "ScoringDataframeT1.csv" )