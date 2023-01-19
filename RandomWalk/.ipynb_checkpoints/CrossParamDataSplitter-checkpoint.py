import pandas as pd

def MakeSplitCSVs( filename ):
    dataframe = pd.read_csv( filename )
    new_data_dict1 = {}
    new_data_dict2 = {}
    new_data_dict3 = {}
    new_data_dict4 = {}
    new_data_dict5 = {}

    size = len( dataframe[ dataframe.columns[ 0 ] ] )
    split_size = int(size/5)

    for i in range( len( dataframe.columns ) ):
        liste = list( dataframe[ dataframe.columns[i] ] )
        new_data_dict1[ dataframe.columns[i] ] = liste[ 0: split_size ]
        new_data_dict2[ dataframe.columns[i] ] = liste[ split_size:2*split_size ]
        new_data_dict3[ dataframe.columns[i] ] = liste[ 2*split_size:3*split_size ]
        new_data_dict4[ dataframe.columns[i] ] = liste[ 3*split_size:4*split_size ]
        new_data_dict5[ dataframe.columns[i] ] = liste[ 4*split_size:size ]

    pd.DataFrame( new_data_dict1 ).to_csv( "Data1.csv" )
    pd.DataFrame( new_data_dict2 ).to_csv( "Data2.csv" )
    pd.DataFrame( new_data_dict3 ).to_csv( "Data3.csv" )
    pd.DataFrame( new_data_dict4 ).to_csv( "Data4.csv" )
    pd.DataFrame( new_data_dict5 ).to_csv( "ParameterLearning.csv" )

if __name__ == "__main__":
    MakeSplitCSVs( "ThinnedDataCleaned1.csv" )