from torch import long
from LongCovidDataId import long_covid_ids
import pandas as pd

def MakeLongCovidCsv( in_csv, filename ):
    dataframe = pd.read_csv( in_csv )
    AddLongCovidCol( dataframe )
    dataframe.to_csv( filename )

def AddLongCovidCol( dataframe ):
    new_col = []
    ids = list( dataframe["BQC ID"] )
    for id in ids:
        if ( id in long_covid_ids ):
            new_col.append( 1 )
        else:
            new_col.append( 0 )
    dataframe[ "Long Covid" ] = new_col


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

def GoodVariable( liste ):
    seen_values = set()
    for i in range( len( liste ) ):
        if ( liste[ i ] == -999 ):
            continue
        if ( liste[ i ] not in seen_values ):
            seen_values.add( liste[ i ] )
    return ( len( list( seen_values ) )  > 1 )