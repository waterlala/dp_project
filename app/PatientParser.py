import numpy as np
import pandas as pd
from PatientBuilder import PatientBuilder

class PatientParser():
    def __init__(self):
        self._patient_builder = PatientBuilder()

    def parse_patient(self, patient_df, record_df, inpatient_df, id):
        personal_info = patient_df.loc[patient_df["ID"] == id,:].values
        personal_record = record_df.loc[record_df['ID'] == id,:]
        personal_inpatient = inpatient_df.loc[inpatient_df['ID'] == id,:]
        self._patient_builder.build_patient(personal_info[0][0], personal_info[0][1], personal_info[0][2], personal_info[0][3], personal_record, personal_inpatient)
    
    def get_result(self):
        return self._patient_builder.get_result()