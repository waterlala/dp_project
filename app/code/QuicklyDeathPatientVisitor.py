import numpy as np
import pandas as pd
import datetime
import pickle
from PatientVisitor import PatientVisitor
from AreaPatientVisitor import AreaPatientVisitor
from ConfirmMonthPatientVisitor import ConfirmMonthPatientVisitor
from ConfirmTypePatientVisitor import ConfirmTypePatientVisitor
from ConfirmAgePatientVisitor import ConfirmAgePatientVisitor
from HistoryTotalDotPatientVisitor import HistoryTotalDotPatientVisitor
from HistoryTypePatientVisitor import HistoryTypePatientVisitor
from HistoryICDPatientVisitor import HistoryICDPatientVisitor
from HistoryMEPatientVisitor import HistoryMEPatientVisitor

class QuicklyDeathPatientVisitor(PatientVisitor):
    def visitPatient(self, patient):
        
        areaPatientVisitor = AreaPatientVisitor()
        areaPatientVisitor.visitPatient(patient)
        area = areaPatientVisitor.getResult()
        
        confirmMonthPatientVisitor = ConfirmMonthPatientVisitor()
        confirmMonthPatientVisitor.visitPatient(patient)
        month = confirmMonthPatientVisitor.getResult()
        
        confirmTypePatientVisitor = ConfirmTypePatientVisitor()
        confirmTypePatientVisitor.visitPatient(patient)
        type = confirmTypePatientVisitor.getResult()
        
        confirmAgePatientVisitor = ConfirmAgePatientVisitor()
        confirmAgePatientVisitor.visitPatient(patient)
        age = confirmAgePatientVisitor.getResult()
        
        historyTotalDotPatientVisitor = HistoryTotalDotPatientVisitor()
        historyTotalDotPatientVisitor.visitPatient(patient)
        dot = historyTotalDotPatientVisitor.getResult()
        
        historyTypePatientVisitor = HistoryTypePatientVisitor()
        historyTypePatientVisitor.visitPatient(patient)
        history_type = historyTypePatientVisitor.getResult()
        
        historyICDPatientVisitor = HistoryICDPatientVisitor()
        historyICDPatientVisitor.visitPatient(patient)
        history_icd = historyICDPatientVisitor.getResult()
        
        historyMEPatientVisitor = HistoryMEPatientVisitor()
        historyMEPatientVisitor.visitPatient(patient)
        history_me = historyMEPatientVisitor.getResult()
        
        model_columns_list = list(pd.read_pickle('../data/model_columns_list.pkl')['key'])
        model_columns_list

        patient_columns_list = pd.DataFrame(columns = ['key','values'])
        patient_columns_list.loc[len(patient_columns_list) + 1 ] = ['dot',dot]
        patient_columns_list.loc[len(patient_columns_list) + 1 ] = ['get_age',age]
        patient_columns_list.loc[len(patient_columns_list) + 1 ] = ['ou',history_type['ou_times'].values[0]]
        patient_columns_list.loc[len(patient_columns_list) + 1 ] = ['em',history_type['em_times'].values[0]]
        patient_columns_list.loc[len(patient_columns_list) + 1 ] = ['in',history_type['in_times'].values[0]]
        patient_columns_list.loc[len(patient_columns_list) + 1 ] = ['type_' + str(type),1]
        patient_columns_list.loc[len(patient_columns_list) + 1 ] = ['area_' + str(area),1]
        patient_columns_list.loc[len(patient_columns_list) + 1 ] = ['month_' + str(month),1]
        for col in list(history_icd.columns):
            patient_columns_list.loc[len(patient_columns_list) + 1 ] = [str(col),1]
        if len(history_me.columns) != 0:
            for col in list(history_me.columns):
                patient_columns_list.loc[len(patient_columns_list) + 1 ] = [str(col),1]

        to_machine_dataframe = pd.DataFrame(columns = model_columns_list)
        to_machine_dataframe.loc[0] = 0
        for col in model_columns_list:
            if col in list(patient_columns_list['key']):
                df = patient_columns_list[patient_columns_list['key']==col]
                to_machine_dataframe.loc[0][str(col)] = df['values'].values[0]

        to_machine_dataframe = to_machine_dataframe.astype('int64')
        with open('../data/model.pickle', 'rb') as f:
            model = pickle.load(f)
        self.result = pd.DataFrame(model.predict_proba(to_machine_dataframe[0:1]))[1].values[0]
        