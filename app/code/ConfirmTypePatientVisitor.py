import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor
from ConfirmDatePatientVisitor import ConfirmDatePatientVisitor

class ConfirmTypePatientVisitor(PatientVisitor):
    def __init__(self):
        self.type = np.nan
        
    def visitPatient(self, patient):
        confirmDatePatientVisitor = ConfirmDatePatientVisitor()
        confirmDatePatientVisitor.visitPatient(patient)
        confirm_date = confirmDatePatientVisitor.getResult()
        
        df = patient.get_record().reset_index(drop = True)
        df['InDate'] = df['InDate'].astype('datetime64')
        df = df[df['InDate'] == confirm_date]
        save = -1
        for type in list(df['Type']):
            if int(type)>save:
                save = int(type)
        type_list = []
        data_list = [] 
        for i in range(0,3,1):
            type_list.append('type_'+str(i))
            if i==save:
                data_list.append(1)
            else:
                data_list.append(0)
        out = pd.DataFrame(columns = type_list)
        out.loc[0]=data_list
        self.type = out
        
    def getResult(self):
        return self.type
