import numpy as np
import pandas as pd
import datetime
import pickle
from PatientVisitor import PatientVisitor
from CalAreaVisitor import CalAreaVisitor
from CalConfirm410MonthVisitor import CalConfirm410MonthVisitor
from CalConfirmedTypeVisitor import CalConfirmedTypeVisitor
from CalConfirmedAgeVisior import CalConfirmedAgeVisior
from CalHistoryTotalDotVisitor import CalHistoryTotalDotVisitor
from CalHistoryTypeVisitor import CalHistoryTypeVisitor
from CalHistoryICDVisitor import CalHistoryICDVisitor
from CalHistoryMEVisitor import CalHistoryMEVisitor

class CalShortTermMortalityRateVisitor(PatientVisitor):
    def visit_patient(self, patient):
        
        calAreaVisitor = CalAreaVisitor()
        patient.accept_visitor(calAreaVisitor)
        area = calAreaVisitor.get_result()
        
        calConfirm410MonthVisitor = CalConfirm410MonthVisitor()
        patient.accept_visitor(calConfirm410MonthVisitor)
        month = calConfirm410MonthVisitor.get_result()
        
        calConfirmedTypeVisitor = CalConfirmedTypeVisitor()
        patient.accept_visitor(calConfirmedTypeVisitor)
        type = calConfirmedTypeVisitor.get_result()
        
        calConfirmedAgeVisior = CalConfirmedAgeVisior()
        patient.accept_visitor(calConfirmedAgeVisior)
        age = calConfirmedAgeVisior.get_result()
        
        calHistoryTotalDotVisitor = CalHistoryTotalDotVisitor()
        patient.accept_visitor(calHistoryTotalDotVisitor)
        dot = calHistoryTotalDotVisitor.get_result()
        
        calHistoryTypeVisitor = CalHistoryTypeVisitor()
        patient.accept_visitor(calHistoryTypeVisitor)
        history_type = calHistoryTypeVisitor.get_result()
        
        calHistoryICDVisitor = CalHistoryICDVisitor()
        patient.accept_visitor(calHistoryICDVisitor)
        history_icd = calHistoryICDVisitor.get_result()
        
        calHistoryMEVisitor = CalHistoryMEVisitor()
        patient.accept_visitor(calHistoryMEVisitor)
        history_me = calHistoryMEVisitor.get_result()
        
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
        self.__result = pd.DataFrame(model.predict_proba(to_machine_dataframe[0:1]))[1].values[0]

    def get_result(self):
        return self.__result
        