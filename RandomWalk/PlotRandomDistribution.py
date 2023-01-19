import matplotlib.pyplot as plt
import RandomWalk as RW
import InitializeGraph as ig
import numpy as np
import ArraySaver as AS
import tools as tools

def GetPlotDataFromGraph( g ):
    data = []
    for e in g.es:
        data.append( tools.AverageListValue( e["Time_Visited"] ) )
    AS.ArrayToFile( np.array( data ), "RandomExpData" )
    return data


def GetDirectedDataFromGraph( g, to_filename ):
    data = []
    for e in g.es:
        data.append( [ tools.AverageListValue( e["AB"] ), tools.AverageListValue( e["BA"] ) ] )
    AS.ArrayToFile( np.array( data ), to_filename )
    return data


def PlotEdgeVisits( g , max_val ):
    data = GetPlotDataFromGraph( g )
    plt.hist( data, bins = 100, range = [0, max_val] )
    plt.show()


def PlotEdgeVisitsFromFile( data_file, max_val ):
    data = AS.LoadArrayFromFile( "RandomExpData.npy" )
    plt.hist( data, bins = 100, range = [0, max_val] )
    plt.show()


def CombineNumpySaveFiles( saveFileListe ):
    if ( len( saveFileListe ) == 0 ):
        return
    accumulation = AS.LoadArrayFromFile( saveFileListe[0] )
    print( len(accumulation) )
    i = 1
    tries = len( saveFileListe )
    while( i < tries ):
        current = AS.LoadArrayFromFile( saveFileListe[i] )
        for k in range( len( accumulation ) ):
            for j in range( len( accumulation[k] ) ):
                accumulation[k][j] = accumulation[k][j] + current[k][j]
        i += 1
    
    for m in range( len( accumulation ) ):
        for n in range( len( accumulation[m] ) ):
            accumulation[m][n] = accumulation[m][n]/10
    AS.ArrayToFile( accumulation, "RandomDirectedDataT1" )