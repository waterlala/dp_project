import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor

class CalConfirm410MonthVisitor(PatientVisitor):
    def visit_patient(self, patient):
        calConfirm410DateVisitor = CalConfirm410DateVisitor()
        patient.accept_visitor(calConfirm410DateVisitor)
        confirm_date = calConfirm410DateVisitor.get_result()
        self.__result = confirm_date.month
    def get_result(self):
        return self.__result