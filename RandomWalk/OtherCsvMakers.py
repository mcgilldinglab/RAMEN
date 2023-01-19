from VectorizeDataframe import VectorizeDataframeSherry
import pandas as pd
import numpy as np

def MakeUIDataCSV( data_file, to_file_name ):
    dataframe = pd.read_csv( data_file )
    dataframe = VectorizeDataframeSherry( dataframe )
    dataframe = Change999ToNaN( dataframe )
    dataframe.to_csv( to_file_name )

def Convert( liste ):
    for i in range( len( liste ) ):
        if ( ( str( liste[i] ) == "-999" ) or ( str( liste[i] ) == "-999.0" ) ):
            liste[i] = np.nan
    return liste

def Change999ToNaN( dataframe ):
    new_data_dict = {}
    for i in range( len( dataframe.columns ) ):
        liste = list( dataframe[ dataframe.columns[i] ] )
        new_data_dict[ dataframe.columns[i] ] = Convert( liste )
    new_data_frame = pd.DataFrame( new_data_dict )
    return new_data_frame

#MakeUIDataCSV( "ThinnedDataCleaned1.csv", "SherryCsv.csv" )