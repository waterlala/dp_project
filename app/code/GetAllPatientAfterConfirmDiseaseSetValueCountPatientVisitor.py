import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from AfterConfirmRecordDiseaseSetPatientVisitor import AfterConfirmRecordDiseaseSetPatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor
from FindPatientByFPTreePatientVisitor import FindPatientByFPTreePatientVisitor

class GetAllPatientAfterConfirmDiseaseSetValueCountPatientVisitor(PatientVisitor):
    def __init__(self, data_storage):
        self._data_storage = data_storage
        
    def visitPatient(self, patient):
        
        findPatientByFPTreePatientVisitor = FindPatientByFPTreePatientVisitor(self._data_storage)
        patient.accept_visitor(findPatientByFPTreePatientVisitor)
        patients = findPatientByFPTreePatientVisitor.getResult()
        
        all_disease = []
        for patient in patients:
            afterConfirmRecordDiseaseSetPatientVisitor = AfterConfirmRecordDiseaseSetPatientVisitor()
            patient.accept_visitor(afterConfirmRecordDiseaseSetPatientVisitor)
            d_set = afterConfirmRecordDiseaseSetPatientVisitor.getResult()
            all_disease = all_disease + d_set
        self.result = pd.Series(all_disease).value_counts().reset_index().rename(columns = {'index':'disease',0:'times'}).sort_values('times',ascending = False)