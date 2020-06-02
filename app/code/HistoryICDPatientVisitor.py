#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor
from ThreeYearRecordFilter import ThreeYearRecordFilter

class HistoryICDPatientVisitor(PatientVisitor):
    
    def __init__(self):
        self.ICD = np.nan
        
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        confirmDatePatientVisitor.visitPatient(patient)
        confirm_date = confirmDatePatientVisitor.getResult()
        
        df = patient.get_record()
        threeYearRecordFilter = ThreeYearRecordFilter(confirm_date)
        df = threeYearRecordFilter.execute(df)

        col = list(set(list(eval(str(list(df['ICD9CM'])).replace('[','').replace(']','')))))
        out = pd.DataFrame(columns = col)
        
        self.ICD = out
        
    def getResult(self):
        return self.ICD


# In[ ]:




