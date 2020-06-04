import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor

class CalConfirmedTypeVisitor(PatientVisitor):
    def visit_patient(self, patient):
        calConfirm410DateVisitor = CalConfirm410DateVisitor()
        patient.accept_visitor(calConfirm410DateVisitor)
        confirm_date = calConfirm410DateVisitor.get_result()
        
        df = patient.get_record().reset_index(drop = True)
        df['InDate'] = df['InDate'].astype('datetime64')
        df = df[df['InDate'] == confirm_date]
        save = -1
        for type in list(df['Type']):
            if int(type)>save:
                save = int(type)
        self.__result = save
    def get_result(self):
        return self.__result
