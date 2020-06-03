import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor

class ConfirmMonthPatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        patient.accept_visitor(confirmDatePatientVisitor)
        confirm_date = confirmDatePatientVisitor.getResult()
        self.result = confirm_date.month