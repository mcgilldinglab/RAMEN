import numpy as np
import MutualInformation as MInt
import InitializeGraph as ig

def ArrayToFile( array, name ):
    np.save( name, array )

def LoadArrayFromFile( file ):
    array = np.load( file )
    return array