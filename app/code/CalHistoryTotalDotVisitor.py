import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor
from ThreeYearRecordFilter import ThreeYearRecordFilter

class CalHistoryTotalDotVisitor(PatientVisitor):
    def visit_patient(self, patient):
        calConfirm410DateVisitor = CalConfirm410DateVisitor()
        patient.accept_visitor(calConfirm410DateVisitor)
        confirm_date = calConfirm410DateVisitor.get_result()
        
        df = patient.get_record()
        threeYearRecordFilter = ThreeYearRecordFilter(confirm_date)
        df = threeYearRecordFilter.execute(df)
        
        self.__result =  df['TotalDot'].sum()

    def get_result(self):
        return self.__result