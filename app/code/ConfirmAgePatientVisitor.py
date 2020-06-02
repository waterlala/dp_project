import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor

class ConfirmAgePatientVisitor(PatientVisitor):
    def __init__(self):
        self.age = np.nan
        
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        confirmDatePatientVisitor.visitPatient(patient)
        confirm_date = confirmDatePatientVisitor.getResult()
        df = pd.DataFrame(columns = ['birth','confirm_date'])
        df.loc[0] = [patient.get_birth(),confirm_date]
        df['different'] = df['confirm_date'] - df['birth']
        df['different'] = df['different'].apply(lambda x: x.days)
        df['different'] = df['different'].apply(lambda x: x/365)
        df = df.rename(columns = {'different':'age'})
        self.age = df[['age']]
        
    def getResult(self):
        return self.age
