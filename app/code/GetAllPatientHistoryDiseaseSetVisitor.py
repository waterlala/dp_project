import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from CalHistoryICDVisitor import CalHistoryICDVisitor

class GetAllPatientHistoryDiseaseSetVisitor(PatientVisitor):
    
    def __init__(self, data_storage):
        self.__data_storage = data_storage
        
    def visit_patient(self, patient):
        df = pd.DataFrame(columns = ['ID','disease'])
        for patient in self.__data_storage.iter_patient_list():
            calHistoryICDVisitor = CalHistoryICDVisitor()
            patient.accept_visitor(calHistoryICDVisitor)
            df.loc[len(df)] = [patient.get_id(),set(calHistoryICDVisitor.get_result().columns)]
        self.__result = pd.Series(list(df['disease']),index = list(df['ID']))
    
    def get_result(self):
        return self.__result