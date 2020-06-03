import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor

class AreaPatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        patient.accept_visitor(confirmDatePatientVisitor)
        confirm_date = confirmDatePatientVisitor.getResult()

        df = patient.get_record().reset_index(drop=True)
        df = df[['InDate','Area']]
        df['InDate'] = df['InDate'].astype('datetime64')
        df['confirm_date'] = confirm_date
        df['different'] = df['InDate'] - df['confirm_date']
        df['different'] = df['different'].apply(lambda x: x.days)
        df = df[(df['different']>=0)&(df['different']<=7)]
        
        self.result = df['Area'].value_counts().sort_values(ascending = False).index[0]
        

