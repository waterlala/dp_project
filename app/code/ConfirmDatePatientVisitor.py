from PatientVisitor import PatientVisitor
import numpy as np
import pandas as pd
import datetime

class ConfirmDatePatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        df_record = patient.get_record()
        df_inpatient = patient.get_inpatient()
        df = pd.concat([df_record[['InDate','ICD9CM']],df_inpatient[['InDate','ICD9CM']]]).reset_index(drop = True)
        df['InDate'] = df['InDate'].astype('datetime64')
        df['is410'] = df['ICD9CM'].apply(lambda x: True if 410 in x else False)
        df = df[df['is410']]
        self.result = df.sort_values('InDate').reset_index(drop = True).iloc[0]['InDate']

