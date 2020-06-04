import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor
from ThreeYearRecordFilter import ThreeYearRecordFilter

class CalHistoryMEVisitor(PatientVisitor):
    def visit_patient(self, patient):
        calConfirm410DateVisitor = CalConfirm410DateVisitor()
        patient.accept_visitor(calConfirm410DateVisitor)
        confirm_date = calConfirm410DateVisitor.get_result()
        
        df = patient.get_inpatient()
        threeYearRecordFilter = ThreeYearRecordFilter(confirm_date)
        df = threeYearRecordFilter.execute(df)
        
        df = df.dropna()
        
        if len(df) != 0:
            col = list(set(list(eval(str(list(df['Drug'])).replace('[','').replace(']','')))))
            out = pd.DataFrame(columns = col)
            self.__result = out
        else:
            self.__result = pd.DataFrame()
        
    def get_result(self):
        return self.__result