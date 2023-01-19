from sklearn.impute import KNNImputer
import pandas as pd
import numpy as np

def ImputeCSV( csv_filename, csv_to_filename ):
    new_dataframe_dic = {}
    df = pd.read_csv( csv_filename )
    index_to_vertex = df.columns
    columns = []
    for vertex in index_to_vertex:
        columns.append( list( df[ vertex ] ) )
    for column in columns:
        for i in range( len( column ) ):
            if ( int( column[ i ] == -999 ) ):
                column[ i ] = np.nan
    patients = []
    for i in range( len( columns[0] ) ):
        patient = []
        for j in range( len( columns ) ):
            patient.append( columns[j][i] )
        patients.append( patient )
    imputer = KNNImputer( n_neighbors = 5 )
    patients = imputer.fit_transform( np.array( patients ) )
    for k in range( len( patients ) ):
        for l in range( len( patients[ k ] ) ):
            patients[ k ][ l ] = int( patients[ k ][ l ] )
    
    for i in range( len( index_to_vertex ) ):
        new_liste = []
        for j in range( len( patients ) ):
            new_liste.append( patients[ j ][ i ] )
        new_dataframe_dic[ index_to_vertex[ i ] ] = new_liste
    complete_df = pd.DataFrame( new_dataframe_dic )
    complete_df.to_csv( csv_to_filename )

def MergeCSVs( csv1, csv2 ):
    d1 = pd.read_csv( csv1 )
    d2 = pd.read_csv( csv2 )
    merged = pd.concat([d1, d2])
    merged.to_csv("Merged.csv")
    

        