import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor
from ThreeYearRecordFilter import ThreeYearRecordFilter

class HistoryTotalDotPatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        confirmDatePatientVisitor.visitPatient(patient)
        confirm_date = confirmDatePatientVisitor.getResult()
        
        df = patient.get_record()
        threeYearRecordFilter = ThreeYearRecordFilter(confirm_date)
        df = threeYearRecordFilter.execute(df)
        
        self.result =  df['TotalDot'].sum()