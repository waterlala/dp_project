import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor
from AfterConfirmRecordFilter import AfterConfirmRecordFilter

class AfterConfirmRecordDiseaseSetPatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        patient.accept_visitor(confirmDatePatientVisitor)
        confirm_date = confirmDatePatientVisitor.getResult()

        afterConfirmRecordFilter = AfterConfirmRecordFilter(confirm_date)
        df = afterConfirmRecordFilter.execute(patient.get_record())

        if len(df) != 0:
            col = list(set(list(eval(str(list(df['ICD9CM'])).replace('[','').replace(']','')))))
        self.result = col