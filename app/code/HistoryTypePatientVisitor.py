import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor
from ThreeYearRecordFilter import ThreeYearRecordFilter

class HistoryTypePatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        patient.accept_visitor(confirmDatePatientVisitor)
        confirm_date = confirmDatePatientVisitor.getResult()
        
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
        
        self.result = out




