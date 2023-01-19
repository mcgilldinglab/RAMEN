import ArraySaver as AS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
from scipy.stats import nbinom
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
import InitializeGraph as ig
import RandomWalk as RW
import PlotRandomDistribution as PRD
import tools as tools
import copy
from InitializeGraph import InitializeRandomWalkGraph

def FitAndExtractSignificantEdges( data_csv, rw_result, random_result, fdr = True, bonf = False ):
    g = MakeDistributionGraph( data_csv, rw_result )

    ( n, p ) = GetDistributionParametersDir( random_result )

    p_values = GetPValues( g, n, p )

    not_input = copy.deepcopy( p_values )
    
    SignificantEdgesToTxt( g, not_input, 0.20, "signif_edges/notcorrected020.txt" )
    SignificantEdgesToTxt( g, not_input, 0.05, "signif_edges/notcorrected005.txt" )
    SignificantEdgesToTxt( g, not_input, 0.01, "signif_edges/notcorrected001.txt" )
    
    if ( bonf ):
        bonf_input = copy.deepcopy( p_values )
        SignificantEdgesToTxt( g, bonf_input, 0.05/len(bonf_input), "signif_edges/bonf005.txt" )
        SignificantEdgesToTxt( g, bonf_input, 0.01/len(bonf_input), "signif_edges/bonf001.txt" )
    if ( fdr ):
        fdr_input = copy.deepcopy( p_values )
        fdr_p_values = FDRCorrection( fdr_input )
        SignificantEdgesToTxt( g, fdr_p_values, 0.05, "signif_edges/fdr005.txt" )
        SignificantEdgesToTxt( g, fdr_p_values, 0.01, "signif_edges/fdr001.txt" )

def GetDistributionParameters( filename ):
    data = AS.LoadArrayFromFile( filename )
    X = np.ones_like( data )
    res = sm.NegativeBinomial( data, X ).fit( start_params = [ 1,1 ])
    p = 1/( 1 + np.exp( res.params[0] )*res.params[1] )
    n = np.exp( res.params[0] )*p/( 1-p )
    return ( n, p )

def GetDistributionParametersDir( filename ):
    pre_data = AS.LoadArrayFromFile( filename )
    data = tools.TwoDArrayToOneDArray( pre_data )
    X = np.ones_like( data )
    res = sm.NegativeBinomial( data, X ).fit( start_params = [ 1,1 ])
    p = 1/( 1 + np.exp( res.params[0] )*res.params[1] )
    n = np.exp( res.params[0] )*p/( 1-p )
    return ( n, p )

def Make2DArrayInto1D( array ):
    new_array = []
    for i in range( len( array ) ):
        for j in range( len( array[ i ] ) ):
            new_array.append( array[i][j] )
    return np.array( new_array )

def PlotFil( filename ):
    data = Make2DArrayInto1D( AS.LoadArrayFromFile( filename ) )
    print( data )
    n, p = GetDistributionParametersDir( filename )
    x_plot = np.linspace( 0, 50 )
    sns.set_theme()
    ax = sns.distplot( data, kde = False, norm_hist = True, label = "Real Values")
    ax.plot( x_plot, nbinom.pmf( x_plot, n, p ), 'g-', lw=2, label = 'Fitted NB')
    plt.title( "Real vs Fitted NB Distributions" )
    plt.show()


def AddEdgeToSortedArray( edgeTup, edgeTupList ):
    for i in range( len( edgeTupList ) ):
        if ( edgeTup[1] < edgeTupList[i][1] ):
            edgeTupList.insert( i, edgeTup )
            return
    edgeTupList.append( edgeTup )

def WriteEdgeTuplistToTxt( edgeTupList, filename ):
    f = open( filename, "w" )
    for i in range( len( edgeTupList ) ):
        f.write( edgeTupList[i][0] )

    f.close()


def SignificantEdgesToTxt( g, p_values, threshold, out_filename ):
    edgeTups = []
    
    visited = set()
    for h in range( len( g.vs ) ):
        for i in range( len( g.vs ) ):
            ID = g.get_eid( h,i )

            if ( ( ID in visited ) or ( i == h ) ):
                continue
            visited.add( ID )

            if ( p_values[ID][0] < threshold ):
                string = ""
                string += g.vs[h]["clinic_vars"]
                string += "--- "
                string += g.vs[i]["clinic_vars"]
                string += ": "
                string += str( p_values[ID][0] )
                string += ";;;TimesVisited: "
                string += str(g.es[ID]["AB"])
                string += "\n"

                to_add = ( string, p_values[ID][0] )
                AddEdgeToSortedArray( to_add, edgeTups )

            if ( p_values[ID][1] < threshold ):
                string = ""
                string += g.vs[i]["clinic_vars"]
                string += "--- "
                string += g.vs[h]["clinic_vars"]
                string += ": "
                string += str( p_values[ID][1] )
                string += ";;;TimesVisited: "
                string += str(g.es[ID]["BA"])
                string += "\n"

                to_add = ( string, p_values[ID][1] )
                AddEdgeToSortedArray( to_add, edgeTups )
    WriteEdgeTuplistToTxt( edgeTups, out_filename )


def GetPValues( g, n, p ):
    p_values = []
    for m in range( len( g.es ) ):
        p_values.append( [ 0, 0 ] )

    visited = set()

    for h in range( len( g.vs ) ):
        for i in range( len( g.vs ) ):
            ID = g.get_eid( h,i )

            if ( ID in visited ):
                continue

            p_value1 = 1 - nbinom.cdf( g.es[ID]["AB"] , n, p )
            p_value2 = 1 - nbinom.cdf( g.es[ID]["BA"] , n, p )

            p_values[ID][0] = p_value1
            p_values[ID][1] = p_value2

    return np.array( p_values )


def FDRCorrection( array ):
    to_compute = np.reshape( array, array.shape[0]*array.shape[1] )
    corrected = multipletests( to_compute, method = "fdr_bh" )
    return np.reshape( corrected[1], ( array.shape[0], array.shape[1]))    


def MakeDistributionGraph( dataframe_csv, edge_visit_count_file ):
    g = InitializeRandomWalkGraph( dataframe_csv )
    visit_array = AS.LoadArrayFromFile( edge_visit_count_file )    
    for i in range( len( g.es ) ):
        try:
            g.es[ i ][ "AB" ] = visit_array[ i ][ 0 ]
            g.es[ i ][ "BA" ] = visit_array[ i ][ 1 ]
        except:
            print( str( i ) + " " + "failed" )
    return g

    