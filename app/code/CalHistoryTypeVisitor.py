import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor
from ThreeYearRecordFilter import ThreeYearRecordFilter

class CalHistoryTypeVisitor(PatientVisitor):
    def visit_patient(self, patient):
        calConfirm410DateVisitor = CalConfirm410DateVisitor()
        patient.accept_visitor(calConfirm410DateVisitor)
        confirm_date = calConfirm410DateVisitor.get_result()
        
        df = patient.get_record()
        threeYearRecordFilter = ThreeYearRecordFilter(confirm_date)
        df = threeYearRecordFilter.execute(df)

        df = df['Type'].value_counts()
        out = pd.DataFrame(columns = ['ou_times','em_times','in_times'])
        key_list = list(df.reset_index()['index'])
        out_list = list()
        for i in range(0,3,1):
            if str(i) in key_list:
                out_list.append(df[str(i)])
            else:
                out_list.append(0)
        out.loc[0] = out_list
        
        self.__result = out
    def get_result(self):
        return self.__result



