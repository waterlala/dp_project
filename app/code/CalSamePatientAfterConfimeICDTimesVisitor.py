import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from GetAfterConfirmICDVisitor import GetAfterConfirmICDVisitor
from CalConfirm410DateVisitor import CalConfirm410DateVisitor
from GetSamePatientByFPTreeVisitor import GetSamePatientByFPTreeVisitor

class CalSamePatientAfterConfimeICDTimesVisitor(PatientVisitor):
    def __init__(self, data_storage):
        self.__data_storage = data_storage
        
    def visit_patient(self, patient):
        
        getSamePatientByFPTreeVisitor = GetSamePatientByFPTreeVisitor(self.__data_storage)
        patient.accept_visitor(getSamePatientByFPTreeVisitor)
        patients = getSamePatientByFPTreeVisitor.get_result()
        
        all_disease = []
        for patient in patients:
            getAfterConfirmICDVisitor = GetAfterConfirmICDVisitor()
            patient.accept_visitor(getAfterConfirmICDVisitor)
            d_set = getAfterConfirmICDVisitor.get_result()
            all_disease = all_disease + d_set
        df = pd.Series(all_disease).value_counts().reset_index().rename(columns = {'index':'disease',0:'times'}).sort_values('times',ascending = False)
        self.__result = df.iloc[:10]
    
    def get_result(self):
        return self.__result