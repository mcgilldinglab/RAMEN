class SortedList( object ):
    def __init__ ( self, size ):
        self.list = []
        self.max_size = size
        self.current_size = 0

    def insert( self, object ):
        inserted = False
        score = object.score
        for i in range( len( self.list ) ):
            local_score = self.list[ i ].score
            if ( score > local_score ):
                self.list.insert( i, object )
                inserted = True
                break
        if ( inserted ):
            if ( self.current_size >= self.max_size ):
                del self.list[ -1 ]
            else:
                self.current_size += 1
        else:
            if ( self.current_size < self.max_size ):
                self.list.append( object )
                self.current_size += 1
    
    def GetScoreAverage( self ):
        sum = 0
        for i in range( len( self.list ) ):
            sum += self.list[ i ].score
        return sum/self.current_size
    
    def GetBest( self ):
        if ( self.list == [] ):
            return -6969696969
        else:
            return self.list[ 0 ].score


class MutationList( object ):
    def __init__ ( self, size ):
        self.list = []
        self.size = 0
        self.max_size = size
    
    def insert( self, mutation ):
        inserted = False
        score = mutation.scoreDiff
        for i in range( len( self.list ) ):
            local_score = self.list[ i ].scoreDiff
            if ( score > local_score ):
                self.list.insert( i, mutation )
                inserted = True
                break
        if ( inserted ):
            if ( self.size >= self.max_size ):
                del self.list[ -1 ]
            else:
                self.size += 1
        else:
            if ( self.size < self.max_size ):
                self.list.append( mutation )
                self.size += 1
    
    def insertListe( self, mutationListe ):
        for i in range( len( mutationListe ) ):
            self.insert( mutationListe[ i ] )

    def ConvertListToMatrixObj( self ):
        MatrixObjListe = []
        for i in range( len( self.list ) ):
            converted = self.list[ i ].GenerateNewMatrix()
            MatrixObjListe.append( converted )
        return MatrixObjListe