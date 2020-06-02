#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor
from ThreeYearRecordFilter import ThreeYearRecordFilter

class HistoryTotalDotPatientVisitor(PatientVisitor):
    
    def __init__(self):
        self.TotalDot = np.nan
        
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        confirmDatePatientVisitor.visitPatient(patient)
        confirm_date = confirmDatePatientVisitor.getResult()
        
        df = patient.get_record()
        threeYearRecordFilter = ThreeYearRecordFilter(confirm_date)
        df = threeYearRecordFilter.execute(df)
        
        out = pd.DataFrame(columns = ['TotalDot'])
        out.loc[0] = df['TotalDot'].sum()
        
        self.TotalDot = out
        
    def getResult(self):
        return self.TotalDot


# In[ ]:




