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
        patient.accept_visitor(areaPatientVisitor)
        area = areaPatientVisitor.getResult()
        
        confirmMonthPatientVisitor = ConfirmMonthPatientVisitor()
        patient.accept_visitor(confirmMonthPatientVisitor)
        month = confirmMonthPatientVisitor.getResult()
        
        confirmTypePatientVisitor = ConfirmTypePatientVisitor()
        patient.accept_visitor(confirmTypePatientVisitor)
        type = confirmTypePatientVisitor.getResult()
        
        confirmAgePatientVisitor = ConfirmAgePatientVisitor()
        patient.accept_visitor(confirmAgePatientVisitor)
        age = confirmAgePatientVisitor.getResult()
        
        historyTotalDotPatientVisitor = HistoryTotalDotPatientVisitor()
        patient.accept_visitor(historyTotalDotPatientVisitor)
        dot = historyTotalDotPatientVisitor.getResult()
        
        historyTypePatientVisitor = HistoryTypePatientVisitor()
        patient.accept_visitor(historyTypePatientVisitor)
        history_type = historyTypePatientVisitor.getResult()
        
        historyICDPatientVisitor = HistoryICDPatientVisitor()
        patient.accept_visitor(historyICDPatientVisitor)
        history_icd = historyICDPatientVisitor.getResult()
        
        historyMEPatientVisitor = HistoryMEPatientVisitor()
        patient.accept_visitor(historyMEPatientVisitor)
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
        