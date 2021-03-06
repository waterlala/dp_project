import numpy as np
import pandas as pd
import json
import time
from PatientParser import PatientParser
from DataStorage import DataStorage
from CalInpatientCycleVisitor import CalInpatientCycleVisitor
from CalMeanAllInpatientCycle import CalMeanAllInpatientCycle
from CalShortTermMortalityRateVisitor import CalShortTermMortalityRateVisitor
from CalHistoryICDCardVisitor import CalHistoryICDCardVisitor
from CalSamePatientSurviveTimeMeanVisitor import CalSamePatientSurviveTimeMeanVisitor
from CalSamePatientAfterConfimeICDTimesVisitor import CalSamePatientAfterConfimeICDTimesVisitor

class InOutput():

    def __init__(self):
        self.__data_storage = DataStorage()
        self.__load_data()
        self.__calculate_group_data()
    def handle_instructions(self, instructions, id):
        patient = self.__get_patient_by_id(id)
        if(instructions == "get_personal_info"):
            if(type(patient) != type(None)):
                return self.__get_personal_info(patient)
            else:
                return None
        elif(instructions == "get_icd_category_growth_trend"):
            if(type(patient) != type(None)):
                return self.__get_icd_category_growth_trend(patient)
            else:
                return None
        elif(instructions == "get_personal_inpatient_cycle"):
            if(type(patient) != type(None)):
                return self.__get_personal_inpatient_cycle(patient)
            else:
                return None
        elif(instructions == "get_shortterm_mortality_rate"):
            if(type(patient) != type(None)):
                return self.__get_shortterm_mortality_rate(patient)
            else:
                return None
        elif(instructions == "same_patient_survive_time_mean"):
            if(type(patient) != type(None)):
                return self.__get_same_patient_survive_time_mean(patient)
            else:
                return None
        elif(instructions == "same_patient_after_confirm_disease_value_counts"):
            if(type(patient) != type(None)):
                return self.__get_same_patient_after_confirm_disease_value_counts(patient)
            else:
                return None

        elif(instructions == "get_average_of_all_the_patients_cycles"):
            return self.__data_storage.get_group_result('avg_of_all_inpatient_cycle')
        else:
            return None

    def __load_data(self):
        #讀json file
        with open('../data/patient.json','r') as patient_reader:
            patient_data = json.load(patient_reader)
        with open('../data/record.json','r') as record_reader:
            record_data = json.load(record_reader)
        with open('../data/inpatient.json','r') as inpatient_reader:
            inpatient_data = json.load(inpatient_reader)
        patient_df = pd.DataFrame.from_dict(patient_data , orient='index')
        record_df = pd.DataFrame.from_dict(record_data , orient='index')
        inpatient_df = pd.DataFrame.from_dict(inpatient_data , orient='index')
        self.__build_patient_data(patient_df, record_df, inpatient_df)

    def __build_patient_data(self,patient_data, record_data, inpatient_data):
        #建立patient資料 呼叫parser builder
        for id in patient_data['ID'].values:
            patient_parser = PatientParser()
            patient_parser.parse_patient(patient_data, record_data, inpatient_data, id)
            self.__data_storage.add_patient(patient_parser.get_result())

    def __calculate_group_data(self):
        self.__data_storage.add_calculated_result('avg_of_all_inpatient_cycle',self.__get_average_of_all_the_patients_cycles())

    #以下要用visitor做
    def __get_personal_info(self, patient):
        out = pd.DataFrame(columns = ['id','gender','birthdate'])
        out.loc[0] = [patient.get_id(),patient.get_gender(),patient.get_birth()]
        out['birthdate'] = out['birthdate'].astype('datetime64')
        out['birthdate'] = out['birthdate'].astype('str')
        return out
    
    def __get_icd_category_growth_trend(self, patient):
        cardPatientVisitor = CalHistoryICDCardVisitor()
        patient.accept_visitor(cardPatientVisitor)
        position = cardPatientVisitor.get_result()
        return position
    
    def __get_personal_inpatient_cycle(self, patient):
        cycle_visitor = CalInpatientCycleVisitor()
        patient.accept_visitor(cycle_visitor)
        return cycle_visitor.get_result()
    
    def __get_average_of_all_the_patients_cycles(self):
        patient_list = self.__data_storage.iter_patient_list()
        cycle_mean_visitor = CalMeanAllInpatientCycle()
        for patient in patient_list:
            patient.accept_visitor(cycle_mean_visitor)
        return cycle_mean_visitor.get_result()
    
    def __get_shortterm_mortality_rate(self, patient):
        quicklyDeathPatientVisitor = CalShortTermMortalityRateVisitor()
        patient.accept_visitor(quicklyDeathPatientVisitor)
        death_posible = quicklyDeathPatientVisitor.get_result()
        return death_posible
    
    def __get_same_patient_survive_time_mean(self, patient):
        calSamePatientDeathMeanTimePatientVisitor = CalSamePatientSurviveTimeMeanVisitor(self.__data_storage)
        patient.accept_visitor(calSamePatientDeathMeanTimePatientVisitor)
        mean = calSamePatientDeathMeanTimePatientVisitor.get_result()
        return mean
    
    def __get_same_patient_after_confirm_disease_value_counts(self, patient):
        calSamePatientAfterConfimeICDTimesVisitor = CalSamePatientAfterConfimeICDTimesVisitor(self.__data_storage)
        patient.accept_visitor(calSamePatientAfterConfimeICDTimesVisitor)
        a_d_set = calSamePatientAfterConfimeICDTimesVisitor.get_result()
        return a_d_set
        
    def __get_patient_by_id(self, id):
        search_patient = None
        for patient in self.__data_storage.iter_patient_list():
            if id == patient.get_id():
                search_patient = patient
                break
        return search_patient