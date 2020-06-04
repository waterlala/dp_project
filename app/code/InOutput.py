import numpy as np
import pandas as pd
import json
import time
from PatientParser import PatientParser
from DataStorage import DataStorage
from CalInpatientCyalevisitor import CalInpatientCyalevisitor
from CalMeanAllInpatientCycle import CalMeanAllInpatientCycle
from CalShortTermMortalityRateVisitor import CalShortTermMortalityRateVisitor
from CalHistoryICDCardVisitor import CalHistoryICDCardVisitor
from CalSamePatientSurviveTimeMeanVisitor import CalSamePatientSurviveTimeMeanVisitor
from CalSamePatientAfterConfimeICDTimesVisitor import CalSamePatientAfterConfimeICDTimesVisitor

class InOutput():
    """
    使用整個IO之前必須呼叫兩個Funtion - 
        1.load_data() 不須輸入參數
        2.set_patient_by_id(_id) 設定好要選擇的病患，需要輸入病人的ID，輸入格式為String
    主要功能 -
        1.get_patient_personal_data()
            取得病患的id,gender,birthdate，不需要輸入資料，輸出資料為columns = id,gender,birthdate 的dataframe轉json 格式為index
            輸出example => {"0":{"id":"fff2ecdf8a0234c105986a3b4a45ae5b","gender":"F","birthdate":"11-01-1932"}}
        2.get_patients_icd_card()
            取得病患卡片收集圖表，不需要輸入資料，輸出為x軸，與y軸座標點，輸出資料為columns = x, y 的dataframe轉json 格式為index
            輸出example => '{"0":{"x":1,"y":0.0},"1":{"x":366,"y":0.0}, ... "81":{"x":29566,"y":90.0}}'
        3.get_patients_by_pattern(desease_set)
            取得與自己相似的病患ID，輸入為疾病的集合example: {'410','465'}，輸出資料為id的list
            輸出example =>['0007613eee440aa3145f09e1dfd0865b','001561666d3f7af58205c452df1006a7', ... '002119087b222fd6ac966d38b8c53f44']
        4.get_quickly_death_model_point()
            取得快速死亡機率，不用輸入，輸出為float
            輸出example => 0.17911194
    """
    def __init__(self):
        self._data_storage = DataStorage()
        self._load_data()
    def handle_instructions(self, instructions, id):
        if(instructions == "get_personal_info"):
            patient = self._get_patient_by_id(id)
            return self.get_personal_info(patient)
        elif(instructions == "get_icd_category_growth_trend"):
            patient = self._get_patient_by_id(id)
            return self.get_icd_category_growth_trend(patient)
        elif(instructions == "get_personal_inpatient_cycle"):
            patient = self._get_patient_by_id(id)
            return self.get_personal_inpatient_cycle(patient)
        elif(instructions == "get_average_of_all_the_patients_cycles"):
            return self.get_average_of_all_the_patients_cycles()
        else:
            return self._data_storage
        #elif(instructions == "get_icd_of_the_same_pattern_patient"):

    def _load_data(self):
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
        self._build_patient_data(patient_df, record_df, inpatient_df)

    def _build_patient_data(self,patient_data, record_data, inpatient_data):
        #建立patient資料 呼叫parser builder
        for id in patient_data['ID'].values:
            patient_parser = PatientParser()
            patient_parser.parse_patient(patient_data, record_data, inpatient_data, id)
            self._data_storage.add_patient(patient_parser.get_result())
        
    
    #以下要用visitor做
    def get_personal_info(self, patient):
        out = pd.DataFrame(columns = ['id','gender','birthdate'])
        out.loc[0] = [patient.get_id(),patient.get_gender(),patient.get_birth()]
        out['birthdate'] = out['birthdate'].astype('datetime64')
        return out
    
    def get_icd_category_growth_trend(self, patient):
        cardPatientVisitor = CalHistoryICDCardVisitor()
        patient.accept_visitor(cardPatientVisitor)
        position = cardPatientVisitor.get_result()
        return position
    
    def get_personal_inpatient_cycle(self, patient):
        cycle_visitor = CalInpatientCyalevisitor()
        patient.accept_visitor(cycle_visitor)
        return cycle_visitor.get_result()
    
    def get_average_of_all_the_patients_cycles(self):
        patient_list = self._data_storage.iter_patient_list()
        cycle_mean_visitor = CalMeanAllInpatientCycle()
        for patient in patient_list:
            patient.accept_visitor(cycle_mean_visitor)
        return cycle_mean_visitor.get_result()
    
    def get_quickly_death_possible(self, patient):
        quicklyDeathPatientVisitor = CalShortTermMortalityRateVisitor()
        patient.accept_visitor(quicklyDeathPatientVisitor)
        death_posible = quicklyDeathPatientVisitor.get_result()
        return death_posible
    
    def get_same_patient_survive_time_mean(self, patient):
        calSamePatientDeathMeanTimePatientVisitor = CalSamePatientSurviveTimeMeanVisitor(self._data_storage)
        patient.accept_visitor(calSamePatientDeathMeanTimePatientVisitor)
        mean = calSamePatientDeathMeanTimePatientVisitor.get_result()
        return mean
    
    def get_same_patient_after_confirm_disease_value_counts(self, patient):
        getAllPatientAfterConfirmDiseaseSetValueCountPatientVisitor = CalSamePatientAfterConfimeICDTimesVisitor(self._data_storage)
        patient.accept_visitor(getAllPatientAfterConfirmDiseaseSetValueCountPatientVisitor)
        a_d_set = getAllPatientAfterConfirmDiseaseSetValueCountPatientVisitor.get_result()
        return a_d_set
        
    def _get_patient_by_id(self, id):
        for patient in self._data_storage.iter_patient_list():
            if id == patient.get_id():
                search_patient = patient
                break
        return search_patient
    """
    def set_patient_by_id(self, _id):
        self._main_patient = self._patients[self._patients['ID'] == _id].reset_index(
            drop='True')
        self._main_records = self._records[self._records['PatientID'] == _id].reset_index(
            drop='True')

    def get_patient_personal_data(self):
        df = self._main_patient[['ID', 'Gender', 'Birth']].rename(
            columns={'ID': 'id', 'Gender': 'gender', 'Birth': 'birthdate'})
        df['birthdate'] = df['birthdate'].apply(
            lambda x: x.strftime("%m-%d-%Y"))
        return df.to_json(orient='index')

    def get_patients_icd_card(self):
        return patients_icd_card(self._main_records, self._main_patient).get_result().to_json(orient='index')
        #return self._main_records.to_json(orient='index')

    def get_patients_by_pattern(self):
        tree = FPTree()
        tree.fit(self._desease_sets)
        pattern = pd.DataFrame(tree.mine(), columns=('Pattern', 'Count'))
        pattern['Length'] = pattern['Pattern'].apply(len)
        desease_set = self._desease_sets[self._main_patient['ID'].iloc[0]]
        match = pattern[pattern['Pattern'].apply(desease_set.issuperset)]
        pattern = match.sort_values(
            'Length', ascending=False).iloc[0]['Pattern']
        return list(self._desease_sets[self._desease_sets.apply(lambda x: x.issuperset(pattern))].index)

    def get_quickly_death_model_point(self):
        _model_quickly_death = joblib.load('model_quickly_death.pkl')
        _model_quickly_death_data = pd.read_pickle(
            'model_death_quickly_data_single_patients.pickle')
        _model_death_quickly_data_list = pd.read_pickle(
            'model_death_quickly_data_list.pickle')
        _model_quickly_death_data = _model_quickly_death_data[
            _model_quickly_death_data['ID'] == self._main_patient.ID.iloc[0]]
        _model_quickly_death_data = _model_quickly_death_data.drop(
            ['ID', 'is_quickly'], axis=1)
        _model_quickly_death_data = _model_quickly_death_data.loc[:, list(
            _model_death_quickly_data_list[0])]
        return _model_quickly_death.predict_proba(_model_quickly_death_data)[0][1]
    """