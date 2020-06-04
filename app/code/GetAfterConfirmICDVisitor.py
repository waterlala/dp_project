import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor
from AfterConfirmRecordFilter import AfterConfirmRecordFilter

class GetAfterConfirmICDVisitor(PatientVisitor):
    def visit_patient(self, patient):
        
        calConfirm410DateVisitor = CalConfirm410DateVisitor()
        patient.accept_visitor(calConfirm410DateVisitor)
        confirm_date = calConfirm410DateVisitor.get_result()

        afterConfirmRecordFilter = AfterConfirmRecordFilter(confirm_date)
        df = afterConfirmRecordFilter.execute(patient.get_record())

        if len(df) != 0:
            col = list(set(list(eval(str(list(df['ICD9CM'])).replace('[','').replace(']','')))))
        self.__result = col

    def get_result(self):
        return self.__result