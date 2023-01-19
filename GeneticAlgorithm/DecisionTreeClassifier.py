from sklearn.tree import DecisionTreeClassifier
import pandas as pd


def RunDTExperiment( X_train, y_train, X_test, y_test ):
    
    




def MakeLearningMatrix( datafile, cols = None, end_var ):
    df = pd.read_csv( datafile )
    learning_cols = []
    if ( cols is None ):
        cols = df.columns
    for i in range( len( cols ) ):
        if ( "unnamed" not in cols[ i ].lower() and cols[ i ] != end_var ):
            learning_cols.append( cols[ i ] )
    
    df_learn = df[ learning_cols ]
    X = df_learn.to_numpy()
    y = df[ end_var ]
    return X, y     