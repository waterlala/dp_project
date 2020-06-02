import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor

class ConfirmMonthPatientVisitor(PatientVisitor):
    def __init__(self):
        self.month = np.nan
        
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        confirmDatePatientVisitor.visitPatient(patient)
        confirm_date = confirmDatePatientVisitor.getResult()
        month_list = []
        data_list = [] 
        for i in range(1,13,1):
            month_list.append('month_'+str(i))
            if i==confirm_date.month:
                data_list.append(1)
            else:
                data_list.append(0)
        out = pd.DataFrame(columns = month_list)
        out.loc[1]=data_list
        self.month = out
        
    def getResult(self):
        return self.month
