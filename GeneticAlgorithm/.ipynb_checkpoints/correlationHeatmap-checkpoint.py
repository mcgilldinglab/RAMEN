import pandas as pd
import seaborn as sns
from CandidateMaker import SignificantEdgesToGraph
from scipy.stats import pearsonr
import numpy as np

def DrawHeatmap( data_file, network_file ):
    g = SignificantEdgesToGraph( network_file )
    dataframe = pd.read_csv( data_file )
    variables = g.nodes
    dim = len( variables )
    heatmap = np.zeros([dim, dim])
    for i in range( dim ):
        for j in range( dim ):
            heatmap[ i ][ j ] = pearsonr( dataframe[ variables[ i ] ], dataframe[ variables[ j ] ] )
    map_data = pd.Dataframe( heatmap_array )
    map_data.columns = variables
    map_data.index = variables
    sns.heatmap( dataframe )