import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor
from ThreeYearRecordFilter import ThreeYearRecordFilter

class HistoryMEPatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        patient.accept_visitor(confirmDatePatientVisitor)
        confirm_date = confirmDatePatientVisitor.getResult()
        
        df = patient.get_inpatient()
        threeYearRecordFilter = ThreeYearRecordFilter(confirm_date)
        df = threeYearRecordFilter.execute(df)
        
        df = df.dropna()
        
        if len(df) != 0:
            col = list(set(list(eval(str(list(df['Drug'])).replace('[','').replace(']','')))))
            out = pd.DataFrame(columns = col)
            self.result = out
        else:
            self.result = pd.DataFrame()