import pandas as pd
import numpy as np
from .VectorizeDataframe import VectorizeDataframe
from .BadVariableEliminater import DropBadVars

def ProcessDataframeNoSave( data_file, ref_save_name, bad_var_threshold = 500 ):
    dataframe = pd.read_csv( data_file )
    dataframe = ConvertNanTo999( dataframe )
    print( "Starting removing vars with too few values, vectorizing dataframe, and initializing mutual information matrix, this might take a few minutes.")    
    start_col = len( dataframe.columns )
    DropBadVars( dataframe, bad_var_threshold )
    dataframe, mapping = VectorizeDataframe( dataframe, ref_save_name )
    end_col = len( dataframe.columns )
    print( "Removed " + str( start_col - end_col ) + " variables because of insufficient data. If deleted too many, please adjust the bad_var_threshold" )
    return dataframe, mapping
    

#TODO NEED to fix a bug where if we just do clean neg and drop bad vars it works but with all the stuff above it doesn't work. Key Error
def ProcessDataframe( data_file, to_name, ref_save_name, bad_var_threshold = 500 ):
    dataframe = pd.read_csv( data_file )
    dataframe = ConvertNanTo999( dataframe )
    #CompleteFirstVisit( dataframe )
    #dataframe = RemoveDuplicateVisits( dataframe )
    print( "starting patient cleaning ")
    #CleanNegativePatients( dataframe )
    
    start_col = len(dataframe.columns)
    print( "dropping bad vars" )
    DropBadVars( dataframe, bad_var_threshold )
    print( "vectorizing dataframe" )
    dataframe, mapping = VectorizeDataframe( dataframe, ref_save_name )
    end_col = len( dataframe.columns )
    print( "Removed " + str( start_col - end_col ) + "Variables because of insufficient data. If deleted too many, please adjust the bad_var_threshold" )
    dataframe.to_csv( to_name )
    print( "Processing Done :)")
    print( "Processed csv saved to " + to_name )

###################### Private Function Section ######################   

def IncompleteData( row ):
    for i in range( len( row ) ):
        if ( row[i] == -999 ):
            return True
    return False

def GetToRemoveRows( dataframe ):
    to_remove_rows = []
    for index, row in dataframe.iterrows():
        if ( dataframe["Final COVID status:"].iloc[index] != "Positive" ):
            to_remove_rows.append( index )

    return to_remove_rows

def CompleteData( dataframe, name ):
    CompleteFirstVisit( dataframe )
    dataframe.to_csv( name )

def CleanNegativePatients( dataframe ):
    to_remove = GetToRemoveRows( dataframe )
    dataframe.drop( to_remove, inplace=True )
    
def CleanNegativePatientsCsv( csv, to_name ):
    dataframe = pd.read_csv( csv )
    to_remove = GetToRemoveRows( dataframe )
    dataframe.drop( to_remove, inplace=True )
    dataframe.to_csv( to_name )
    
def ConvertNanTo999( dataframe ):
    new_data_dict = {}
    variables = dataframe.columns
    for i in range( len( variables ) ):
        liste = list( dataframe[ variables[i] ] )
        new_data_dict[ variables[i] ] = Convert( liste )
    new_dataframe = pd.DataFrame( new_data_dict )
    return new_dataframe

def Convert( liste ):
    for i in range( len( liste ) ):
        if ( type( liste[ i ] ) == str ):
            continue
        if ( np.isnan( liste[i] ) ):
            liste[i] = -999
    return liste

def CompleteFirstVisit( dataframe ):
    id_tracker = {}
    cols = dataframe.columns
    for index, row in dataframe.iterrows():
        id = dataframe.loc[ index, 'BQC ID']
        if ( id not in id_tracker ):
            id_tracker[ id ] = index
        else:
            original_index = id_tracker[id]
            for col in cols:
                if ( str(dataframe.loc[ original_index, col ]) == "-999" or str(dataframe.loc[ original_index, col ]) == "-999.0" ):
                    dataframe.loc[ original_index, col ] = dataframe.loc[ index, col ]

def RemoveDuplicateVisits( dataframe ):
    cols = dataframe.columns
    new_dataframe_dict = {}
    for col in cols:
        new_dataframe_dict[ col ] = []
    id_tracker = set()
    cols = dataframe.columns
    for index, row in dataframe.iterrows():
        print( index )
        id = dataframe.loc[ index, 'BQC ID']
        if ( id not in id_tracker ):
            id_tracker.add( id )
            for col in cols:
                new_dataframe_dict[ col ].append( dataframe.loc[ index, col ] )
    new_dataframe = pd.DataFrame( new_dataframe_dict )
    return new_dataframe

def GoodVariable( liste ):
    seen_values = set()
    for i in range( len( liste ) ):
        if ( liste[ i ] == -999 ):
            continue
        if ( liste[ i ] not in seen_values ):
            seen_values.add( liste[ i ] )
    return ( len( list( seen_values ) )  > 1 )

def CleanOneValueVariables( in_csv, filename ):
    to_drop = []
    dataframe = pd.read_csv( in_csv )
    print( len( dataframe.columns ) )
    for col in dataframe.columns:
        if ( not GoodVariable( list( dataframe[ col ] ) ) ):
            to_drop.append( col )
    dataframe.drop( columns = to_drop, inplace=True )
    print( len( dataframe.columns ) )
    dataframe.to_csv( filename )