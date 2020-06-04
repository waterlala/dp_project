import numpy as np
import pandas as pd
import datetime
from FP_growth import FPTree
from PatientVisitor import PatientVisitor
from GetAllPatientHistoryDiseaseSetVisitor import GetAllPatientHistoryDiseaseSetVisitor

class GetSamePatientByFPTreeVisitor(PatientVisitor):
    def __init__(self, data_storage):
        self.__data_storage = data_storage
        
    def visit_patient(self, patient):
        getAllPatientHistoryDiseaseSetVisitor = GetAllPatientHistoryDiseaseSetVisitor(self.__data_storage)
        patient.accept_visitor(getAllPatientHistoryDiseaseSetVisitor)
        desease_sets = getAllPatientHistoryDiseaseSetVisitor.get_result()
        
        tree = FPTree()
        tree.fit(desease_sets)
        pattern = pd.DataFrame(tree.mine(), columns=('Pattern', 'Count'))
        pattern['Length'] = pattern['Pattern'].apply(len)
        df = desease_sets.reset_index()
        df = df.rename(columns={'index':'ID',0:'ICD9CM'})
        desease_set = df[df['ID'] == patient.get_id()]['ICD9CM'].iloc[0]
        match = pattern[pattern['Pattern'].apply(desease_set.issuperset)]
        pattern = match.sort_values('Length', ascending=False).iloc[0]['Pattern']
        patients = desease_sets[desease_sets.apply(lambda x: x.issuperset(pattern))].index
        patients = list(patients)
        save_patients = list()
        for patient in self.__data_storage.iter_patient_list():
            if patient.get_id() in patients:
                save_patients.append(patient)
        self.__result = save_patients
    
    def get_result(self):
        return self.__result