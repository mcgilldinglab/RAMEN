from igraph import*
from ProcessDataframe import ProcessDataframe
import numpy as np
import tools as tools
import pandas as pd

def InitializeMutualInfoMatrixGraph( dataframe ):
    g = Graph()

    clinic_vars = list( dataframe.columns )
    slicing_index = GetStartVarIndex( clinic_vars )
    g.add_vertices( len( clinic_vars[ slicing_index: ] ) )
    g.vs[ "clinic_vars" ] = clinic_vars[ slicing_index: ]

    AttachVectors( clinic_vars[ slicing_index: ], dataframe, g )

    CreateEdges( g )

    return g

#assumption here is that the csv_file has already been processed using ProcessDataframe
def InitializeRandomWalkGraph( csv_file ):
    g = Graph()
    dataframe = pd.read_csv( csv_file )

    clinic_vars = list( dataframe.columns )
    slicing_index = GetStartVarIndex( clinic_vars )
    g.add_vertices( len( clinic_vars[ slicing_index: ] ) )
    g.vs[ "clinic_vars" ] = clinic_vars[ slicing_index: ]

    CreateEdges(g)

    return g


###################### Private Function Section ######################   

def AttachVectors( variables, dataframe, g ):
    liste = []
    for var in variables:
        liste.append( CreateVector( var, dataframe ) )
    g.vs["Vector"] = liste

def CreateVector( variable, dataframe ):
    return list( dataframe[variable] )

def CreateEdges( g ):
    added = set()
    for h in range(len(g.vs)):
        for i in range(len(g.vs)):
            if (not((h,i) in added or (i,h) in added)):
                g.add_edges([(h, i)])
                ID = g.get_eid(h,i)
                g.es[ID]["Time_Visited"] = []
                g.es[ID]["AB"] = []
                g.es[ID]["BA"] = []
                added.add((h,i))

def GetStartVarIndex( liste ):
    for i in range( len( liste ) ):
        if ( "Unnamed" not in str( liste[ i ] ) ):
            return i
    return -1