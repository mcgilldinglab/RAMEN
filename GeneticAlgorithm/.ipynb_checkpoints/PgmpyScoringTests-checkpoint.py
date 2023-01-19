import pgmpy
import pandas as pd

def PgmpyScoringTest1():
    dataframe = pd.read_csv( "ScoringDataframeT1.csv" )
    grader = pgmpy.estimators.K2Score( dataframe, complete_samples_only = False )
    child = "LDH:"
    parents = ['Repeat Instance', 'Height in m:', 'Asthma ?', 'Dementia ? ', 'Immunosupressed state?', 'Coronary artery disease ?', 'COPD (emphysema, chronic bronchitis) ?', 'Obesity ?', 'Psychiatric disease?', 'Chronic kidney disease ?', 'HGO or insulin?', 'Diarrhea ?', 'Shortness of breath (Dyspnea) ?', 'Fatigue ?', 'Fever (?38.0 Celcius) ?', 'Muscle aches (Myalgia) ?', 'Nausea / vomiting ?', 'Loss of taste / lost of smell ?', 'Skin rash ?', 'Runny nose (Rhinorrhea) ?', 'Neutrophil (x 10^9/L):', 'Eosinophil (relative value)', 'Gastrointestinal haemorrhage?', 'Hyperglycemia?', 'Acute kidney injury?', 'Treatments administered: (choice=Hydroxychloroquine (Plaquenil))', 'Treatments administered: (choice=Other COVID-19 treatments (specify))', 'Lymphocyte (relative value) (LOWEST value)', 'Potassium K+ (HIGHEST value)', 'Has the participant had any new disease and/or worsening and/or deterioration of a pre-existing disease?', 'Joint pain (Arthralgia) ?.1', 'Diarrhea ?.1', 'Abdominal pain ?.1', 'Chest pain ?.1', 'Shortness of breath (Dyspnea) ?.1', 'Extremity weakness or numbness ?.1', 'Loss of appetite ?.1', 'Headache ?.1', 'Muscle aches (Myalgia) ?.1', 'Nausea / vomiting ?.1', 'Loss of taste / lost of smell ?.1', 'Skin rash ?.1', 'Cough ?.1', 'Trouble speaking (Aphasia / Dysphasia) ?.1', 'Usual activities, including work, study, housework, family or leisure activities:', 'How much difficulty do you have walking across a room?', 'How many times have you fallen in the past year?']
    edgescore = grader.local_score( child, parents)
    return edgescore
    