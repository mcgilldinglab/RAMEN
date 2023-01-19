def CalculateMean( data ): 
    sum = 0
    n = len ( data )
    for i in range( n ):
        sum += data[i]
    
    return sum/n


def CalculateVariance( data ):
    sum = 0
    mean = CalculateMean( data )
    n = len( data )

    for i in range( n ):
        top = ( data[i] - mean )**2
        sum += top
    
    return sum/( n-1 )