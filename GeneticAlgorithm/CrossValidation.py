from .Scorer import Scorer
from .GeneticAlgorithmLauncher import SignificantEdgesToVertices, InitializeVarToIndexDictionary
import pandas as pd
import .BinaryStringToBayesianN as BSTB
import numpy as np
from .ParameterLearning import EdgesToGraph, SignificantEdgesToVertices

def ScoreNetwork( scoring_dataframe_file, significant_edges_file ):
    ScoringDataframe = pd.read_csv( scoring_dataframe_file )
    index_to_vertex = SignificantEdgesToVertices( significant_edges_file )
    var_to_index_dict = InitializeVarToIndexDictionary( index_to_vertex )
    scorer = Scorer( index_to_vertex, ScoringDataframe, 0 )
    candidate = np.array( BSTB.NetworkTo2dMatrix( EdgesToGraph( significant_edges_file ), var_to_index_dict ) )
    return scorer.Score( candidate )

def InitializeVarToIndexDictionary( IndexToVarListe ):
    var_to_index = {}
    for i in range( len( IndexToVarListe ) ):
        var_to_index[ IndexToVarListe[i] ] = i
    return var_to_index