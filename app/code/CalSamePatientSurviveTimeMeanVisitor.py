import numpy as np
import pandas as pd
from datetime import datetime
from FP_growth import FPTree
from PatientVisitor import PatientVisitor
from GetSamePatientByFPTreeVisitor import GetSamePatientByFPTreeVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor

class CalSamePatientSurviveTimeMeanVisitor(PatientVisitor):
    def __init__(self, data_storage):
        self.__data_storage = data_storage
        
    def visit_patient(self, patient):
        
        getSamePatientByFPTreeVisitor = GetSamePatientByFPTreeVisitor(self.__data_storage)
        patient.accept_visitor(getSamePatientByFPTreeVisitor)
        patients = getSamePatientByFPTreeVisitor.get_result()
        
        survive_days_list = list()
        for s_patient in patients:
            if not str(s_patient.get_death())=='NaT':
                death_date = datetime.strptime(s_patient.get_death(),"%Y-%m-%d %H:%M:%S")
                calConfirm410DateVisitor = CalConfirm410DateVisitor()
                s_patient.accept_visitor(calConfirm410DateVisitor)
                confirm_date = calConfirm410DateVisitor.get_result()
                survive_days_list.append((death_date - confirm_date).days)
        self.__result = pd.Series(survive_days_list).mean()
    def get_result(self):
        return self.__result