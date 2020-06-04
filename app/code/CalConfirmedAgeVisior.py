import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor

class CalConfirmedAgeVisior(PatientVisitor):
    def visit_patient(self, patient):
        calConfirm410DateVisitor = CalConfirm410DateVisitor()
        patient.accept_visitor(calConfirm410DateVisitor)
        confirm_date = calConfirm410DateVisitor.get_result()
        df = pd.DataFrame(columns = ['birth','confirm_date'])
        df.loc[0] = [patient.get_birth(),confirm_date]
        df['different'] = df['confirm_date'] - df['birth']
        df['different'] = df['different'].apply(lambda x: x.days)
        df['different'] = df['different'].apply(lambda x: x/365)
        df = df.rename(columns = {'different':'age'})
        self.__result = df[['age']].iloc[0].values[0]
    def get_result(self):
        return self.__result