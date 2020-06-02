import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor
from ThreeYearRecordFilter import ThreeYearRecordFilter

class HistoryMEPatientVisitor(PatientVisitor):
    
    def __init__(self):
        self.ICD = np.nan
        
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        confirmDatePatientVisitor.visitPatient(patient)
        confirm_date = confirmDatePatientVisitor.getResult()
        
        df = patient.get_inpatient()
        threeYearRecordFilter = ThreeYearRecordFilter(confirm_date)
        df = threeYearRecordFilter.execute(df)
        
        if len(df) != 0:
            col = list(set(list(eval(str(list(df['Drug'])).replace('[','').replace(']','')))))
            out = pd.DataFrame(columns = col)
            self.ICD = out
        else:
            self.ICD = np.nan
    def getResult(self):
        return self.ICD