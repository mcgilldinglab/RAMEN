import numpy as np
import pandas as pd

def Discretize( dataEntries ):
    discretized = []

    NonNanIndices = NonMissingValuesIndices( dataEntries )
    CompleteValues = GetCompleteValuesFromIndices( dataEntries, NonNanIndices )

    xmax = int( max( CompleteValues ) ) + 1
    xmin = int( min( CompleteValues ) )
    
    bins_mapping = {}
    bins = BuildBins( xmin, xmax, 10 )
    for i in range( len( bins ) - 1 ):
        bins_mapping[ ( bins[ i ], bins[ i + 1 ] ) ] = i
    discretized = list( np.digitize( CompleteValues, bins ) )

    UpdateDataEntries( dataEntries, NonNanIndices, discretized )

    return dataEntries, bins_mapping

###################### Private Function Section ######################

# this creates the bins necessary for discretizing

def BuildBins( start, end, num_bins ):
    increment = (end - start)/num_bins
    current = start
    bins = []
    for i in range( num_bins + 1 ):
        bins.append( current )
        current += increment
    return bins

def UpdateDataEntries( liste, indices, completeValues ):
    for i in range( len( completeValues ) ):
        liste[indices[i]] = completeValues[i]

def NonMissingValuesIndices( liste ):
    indices = []
    for i in range( len( liste ) ):
        if ( liste[i] != -999 ):
            indices.append( i )
    return indices

def GetCompleteValuesFromIndices( liste, indices ):
    values = []
    for i in range( len( indices ) ):
        values.append( liste[ indices[i] ] )
    return values

# Not really necessary
def FixAge():
    dataframe = pd.read_csv("ScoringDataframeT1.csv")
    
    age_string = ""
    for col in dataframe.columns:
        if ("ge au recrutement" in col):
            age_string = col
    age_column = list(dataframe[age_string])
    for i in range(len(age_column)):
        value = float(age_column[i])
        value = value*10+5
        age_column[i] = value
    dataframe["Age au recrutement"] = age_column
    dataframe.drop(age_string, inplace = True, axis = 1)
    dataframe.to_csv("ScoringDataframeT11.csv")