from .Discretization import Discretize
import pandas as pd
import pickle

def VectorizeDataframe( dataframe, variable_ref_file ):
    new_data_dict = {}
    discr_var_dic = {}
    variables = dataframe.columns
    for i in range( len( variables ) ):
        liste = list( dataframe[ variables[i] ] )
        new_data_dict[ variables[i] ] = ConvertToVector( liste, variables[ i ], discr_var_dic )
    new_data_frame = pd.DataFrame( new_data_dict )
    
    return new_data_frame, discr_var_dic

###################### Private Function Section ######################

def ConvertToVector( liste, var, discr_var_dic ):
    if ( IsRealVar( liste ) ):
        values, mapping = Discretize( liste )
        discr_var_dic[ var ] = mapping
        return values
    else:
        value = 0
        tracker = { "-999" : -999, "-999.0" : -999 }
        newlist = []
        for i in range( len( liste ) ):
            stringBuffer = str(liste[i])
            if ( stringBuffer not in tracker ):
                tracker[ stringBuffer ] = value
                newlist.append( tracker[ stringBuffer ] )
                value += 1
            else:
                newlist.append( tracker[ stringBuffer ] )
        tracker.pop( "-999" )
        tracker.pop( "-999.0" )
        discr_var_dic[ var ] = tracker
        return newlist

def IsRealVar( array ):
    valueSet = set()
    for i in range( len( array ) ):
        if ( type( array[i] ) == float ) and ( array[i] != -999 ):
            return True
        valueSet.add( array[ i ] )
    numberBool = False
    valueList = list( valueSet )
    for j in range( len( valueList ) ):
        if ( type( valueList[ j ] ) != str and valueList[ j ] != -999 ):
            numberBool = True
            break
    if ( len( valueSet ) > 10 and numberBool ):
        return True
    return False