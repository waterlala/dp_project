import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor

class ConfirmAgePatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        patient.accept_visitor(confirmDatePatientVisitor)
        confirm_date = confirmDatePatientVisitor.getResult()
        df = pd.DataFrame(columns = ['birth','confirm_date'])
        df.loc[0] = [patient.get_birth(),confirm_date]
        df['different'] = df['confirm_date'] - df['birth']
        df['different'] = df['different'].apply(lambda x: x.days)
        df['different'] = df['different'].apply(lambda x: x/365)
        df = df.rename(columns = {'different':'age'})
        self.result = df[['age']].iloc[0].values[0]