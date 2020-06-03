import numpy as np
import pandas as pd
from datetime import datetime
from FP_growth import FPTree
from PatientVisitor import PatientVisitor
from FindPatientByFPTreePatientVisitor import FindPatientByFPTreePatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor

class CalSamePatientDeathMeanTimePatientVisitor(PatientVisitor):
    def __init__(self, data_storage):
        self._data_storage = data_storage
        
    def visitPatient(self, patient):
        
        findPatientByFPTreePatientVisitor = FindPatientByFPTreePatientVisitor(self._data_storage)
        patient.accept_visitor(findPatientByFPTreePatientVisitor)
        patients = findPatientByFPTreePatientVisitor.getResult()
        
        survive_days_list = list()
        for s_patient in patients:
            if not str(s_patient.get_death())=='NaT':
                death_date = datetime.strptime(s_patient.get_death(),"%Y-%m-%d %H:%M:%S")
                confirmDatePatientVisitor = ConfirmDatePatientVisitor()
                s_patient.accept_visitor(confirmDatePatientVisitor)
                confirm_date = confirmDatePatientVisitor.getResult()
                survive_days_list.append((death_date - confirm_date).days)
        self.result = pd.Series(survive_days_list).mean()