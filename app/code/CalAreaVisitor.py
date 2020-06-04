import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor

class CalAreaVisitor(PatientVisitor):
    def visit_patient(self, patient):
        
        calConfirm410DateVisitor = CalConfirm410DateVisitor()
        patient.accept_visitor(calConfirm410DateVisitor)
        confirm_date = calConfirm410DateVisitor.get_result()

        df = patient.get_record().reset_index(drop=True)
        df = df[['InDate','Area']]
        df['InDate'] = df['InDate'].astype('datetime64')
        df['confirm_date'] = confirm_date
        df['different'] = df['InDate'] - df['confirm_date']
        df['different'] = df['different'].apply(lambda x: x.days)
        df = df[(df['different']>=0)&(df['different']<=7)]
        
        self.__result = df['Area'].value_counts().sort_values(ascending = False).index[0]
    
    def get_result(self):
        return self.__result