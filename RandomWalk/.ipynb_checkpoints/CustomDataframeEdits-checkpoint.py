import pandas as pd

def GetCommorbidityCols( dataframe ):
    commorbidities = []
    to_remove = []
    for col in dataframe:
        if ( ("Other comorbidity") in col or ( "Other comorbodity") in col ):
            to_remove.append( col )
            commorbidities.append( list( dataframe[col] ) )
    dataframe.drop( to_remove, inplace = True, axis = 1 )

    return commorbidities

def MergeCommorbidities( commorbidities ):
    combined = []
    for i in range( len( commorbidities[0] ) ):
        total = 0
        for j in range( len( commorbidities ) ):
            if ( str(commorbidities[j][i]) != "-999" and str(commorbidities[j][i]) != "-999.0" ):
                total += 1
        combined.append( total )
    return combined

def CombineCommorbidities( dataframe ):
    to_merge = GetCommorbidityCols( dataframe )
    merged = MergeCommorbidities( to_merge )
    dataframe[ "Number of comorbidities: " ] = merged


def MergeInCSV( file , end_file_name ):
    dataframe = pd.read_csv( file )
    CombineCommorbidities( dataframe )
    dataframe.to_csv( end_file_name )

def GetComplicationCols( dataframe ):
    complications = []
    to_remove = []
    for col in dataframe:
        if ( "complication" in col ):
            to_remove.append( col )
            complications.append( list( dataframe[col] ) )
    dataframe.drop( to_remove, inplace = True, axis = 1 )
    return complications

def MergeComplications( complications ):
    combined = []
    for i in range( len( complications[0] ) ):
        total = 0
        for j in range( len( complications ) ):
            if ( str(complications[j][i]) != "-999" and str(complications[j][i]) != "-999.0" ):
                total += 1
        combined.append( total )
    return combined


def CombineComplications( dataframe ):
    to_merge = GetComplicationCols( dataframe )
    merged = MergeComplications( to_merge )
    dataframe[ "Number of Complications: " ] = merged

def MergeComplicationsCSV( file , end_file_name ):
    dataframe = pd.read_csv( file )
    CombineComplications( dataframe )
    dataframe.to_csv( end_file_name )

def RemoveNonHospitalizedPatient( datafile ):
    dataframe = pd.read_csv( datafile )
    to_remove_rows = []
    for index, row in dataframe.iterrows():
        if ( dataframe["Has the participant been hospitalized or is the participant seen on an outpatient?"].iloc[index] != "Hospitalized" ):
            to_remove_rows.append( index )
    dataframe.drop( to_remove_rows, inplace=True )
    dataframe.to_csv( datafile )

def EditSmokingStatus( datafile ):
    dataframe = pd.read_csv( datafile )
    for index, row in dataframe.iterrows():
        if ( dataframe[ "Smoking status:" ].iloc[ index ] == "Not specified" ):
            dataframe[ "Smoking status:"].iloc[ index ] = -999
    dataframe.to_csv( datafile )


def ConvertFIO2ToPercentage( datafile ):
    dataframe = pd.read_csv( datafile )
    for index, row in dataframe.iterrows():
        if ( dataframe[ "FiO2 unit:" ].iloc[ index ] == "L/min" ):
            dataframe [ "On arrival, FiO2:" ].iloc[ index ] = 20 + float( dataframe [ "On arrival, FiO2:" ].iloc[ index ] )*4
            dataframe[ "FiO2 unit:" ].iloc[ index ] = "%"
    dataframe.to_csv( datafile )

def ConvertFIO2dot1ToPercentage( datafile ):
    dataframe = pd.read_csv( datafile )
    for index, row in dataframe.iterrows():
        if ( dataframe[ "FiO2 unit:.1" ].iloc[ index ] == "L/min" ):
            dataframe [ "At the time of collection, FiO2:" ].iloc[ index ] = 20 + float( dataframe [ "At the time of collection, FiO2:" ].iloc[ index ] )*4
            dataframe[ "FiO2 unit:.1" ].iloc[ index ] = "%"
    dataframe.to_csv( datafile )


def ConvertFIO2dot2ToPercentage( datafile ):
    dataframe = pd.read_csv( datafile )
    for index, row in dataframe.iterrows():
        if ( dataframe[ "FiO2 unit:.2" ].iloc[ index ] == "L/min" ):
            dataframe [ "FiO2 (associated with the previous SpO2):" ].iloc[ index ] = 20 + float( dataframe [ "FiO2 (associated with the previous SpO2):" ].iloc[ index ] )*4
            dataframe[ "FiO2 unit:.2" ].iloc[ index ] = "%"
    dataframe.to_csv( datafile )

def ConvertFIO2dot3ToPercentage( datafile ):
    dataframe = pd.read_csv( datafile )
    for index, row in dataframe.iterrows():
        if ( dataframe[ "FiO2 unit:.3" ].iloc[ index ] == "L/min" ):
            dataframe [ "FiO2 (related to SPO2)" ].iloc[ index ] = 20 + float( dataframe [ "FiO2 (related to SPO2)" ].iloc[ index ] )*4
            dataframe[ "FiO2 unit:.3" ].iloc[ index ] = "%"
    dataframe.to_csv( datafile )


def ConvertTemperatureToOral( datafile ):
    dataframe = pd.read_csv( datafile )
    for index, row in dataframe.iterrows():
        if ( dataframe[ "Temperature route:" ].iloc[ index ] == "Tympanic" ):
            dataframe[ "Temperature route:" ].iloc[ index ] = "Oral"
            dataframe[ "Temperature:" ].iloc[ index ] = float( dataframe[ "Temperature:" ].iloc[ index ] ) - 0.4
        elif ( dataframe[ "Temperature route:" ].iloc[ index ] == "Axillary" ):
            dataframe[ "Temperature route:" ].iloc[ index ] = "Oral"
            dataframe[ "Temperature:" ].iloc[ index ] = float( dataframe[ "Temperature:" ].iloc[ index ] ) + 0.4
        elif ( dataframe[ "Temperature route:" ].iloc[ index ] == "Rectal" ):
            dataframe[ "Temperature route:" ].iloc[ index ] = "Oral"
            dataframe[ "Temperature:" ].iloc[ index ] = float( dataframe[ "Temperature:" ].iloc[ index ] ) - 0.4
        elif ( dataframe[ "Temperature route:" ].iloc[ index ] == "Not available" ):
            dataframe[ "Temperature route:" ].iloc[ index ] = "Oral"
        
        if ( dataframe[ "Temperature route:.1" ].iloc[ index ] == "Tympanic" ):
            dataframe[ "Temperature route:.1" ].iloc[ index ] = "Oral"
            dataframe[ "Temperature:.1" ].iloc[ index ] = float( dataframe[ "Temperature:.1" ].iloc[ index ] ) - 0.4
        elif ( dataframe[ "Temperature route:.1" ].iloc[ index ] == "Axillary" ):
            dataframe[ "Temperature route:.1" ].iloc[ index ] = "Oral"
            dataframe[ "Temperature:.1" ].iloc[ index ] = float( dataframe[ "Temperature:.1" ].iloc[ index ] ) + 0.4
        elif ( dataframe[ "Temperature route:.1" ].iloc[ index ] == "Rectal" ):
            dataframe[ "Temperature route:.1" ].iloc[ index ] = "Oral"
            dataframe[ "Temperature:.1" ].iloc[ index ] = float( dataframe[ "Temperature:.1" ].iloc[ index ] ) - 0.4
        elif ( dataframe[ "Temperature route:.1" ].iloc[ index ] == "Not available" ):
            dataframe[ "Temperature route:.1" ].iloc[ index ] = "Oral"
        
    dataframe.to_csv( datafile )


def ConvertSeverityToBinary( datafile ):
    dataframe = pd.read_csv( datafile )
    string = "If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?"
    for index, row in dataframe.iterrows():
        if ( str(dataframe[ string ].iloc[ index ]) == "-999" or str(dataframe[ string ].iloc[ index ]) == "-999.0" ):
            continue
        if ( dataframe[ string ].iloc[ index ] == "Severe" or dataframe[ string ].iloc[ index ] == "Dead" ):
            dataframe[ string ].iloc[ index ] = "Severe"
        else:
            dataframe[ string ].iloc[ index ] = "Mild"
    dataframe.to_csv( datafile )
        

if __name__ == "__main__":
    #MergeInCSV( "ThinnedData.csv", "ThinnedData.csv")
    #MergeComplicationsCSV( "ThinnedData.csv", "ThinnedData.csv" )
    #RemoveNonHospitalizedPatient( "ThinnedData.csv" )
    #EditSmokingStatus( "ThinnedData.csv" )
    #ConvertFIO2ToPercentage( "ThinnedData.csv" )
    #ConvertTemperatureToOral( "ThinnedData.csv" )
    #ConvertFIO2dot1ToPercentage( "ThinnedData.csv" )
    #ConvertFIO2dot2ToPercentage( "ThinnedData.csv" )
    #ConvertFIO2dot3ToPercentage( "ThinnedData.csv" )
    ConvertSeverityToBinary( "ThinnedDataCleaned2.csv" )