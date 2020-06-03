import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor

class ConfirmTypePatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        patient.accept_visitor(confirmDatePatientVisitor)
        confirm_date = confirmDatePatientVisitor.getResult()
        
        df = patient.get_record().reset_index(drop = True)
        df['InDate'] = df['InDate'].astype('datetime64')
        df = df[df['InDate'] == confirm_date]
        save = -1
        for type in list(df['Type']):
            if int(type)>save:
                save = int(type)
        self.result = save
