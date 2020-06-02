#!/usr/bin/env python
# coding: utf-8

# In[34]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from patients_icd_card import patients_icd_card
from FP_growth import FPTree


# In[35]:


class io:
    """
    初始化
    
    1.呼叫load_data() -->time = 6.64s
    
    2.呼叫需要尋找的病患 set_patient_by_id(_id)  -->time = 1min35s
        輸入ID(type = String) 
        輸出: 無
        
    功能
    
    1.取得病患資料 get_patient_personal_data() -->time = 1.99ms
        輸入: 無
        輸出: columns = id,gender,birthdate 的dataframe
        
    2.取得病患疾病卡片 get_patients_icd_card() -->time = 87.8ms
        輸入: 無
        輸出: columns = x,y 的dataframe , x => x軸座標 y => y軸座標
        
    3.取得與自己相似的病患 get_patients_by_pattern(desease_set) -->time = 21s
        輸入: desease_set(Type = set{string}) example => {'410','465'}
        輸出: id 的 list example => ['dsfsgsdfa','dsfasdfsa']
        
    """
    def __init__(self):
        self._patients = np.nan
        self._records = np.nan
        self._main_patient = np.nan
        self._main_records= np.nan
        self._desease_sets = np.nan
    def load_data(self):
        self._patients = pd.read_pickle('patients.pkl.zip')
        self._records = pd.read_pickle('records_inpatients.pkl.zip')
        self._desease_sets = pd.read_pickle('disease_sets.pkl.zip')
    def set_patient_by_id(self, _id):
        self._main_patient = self._patients[self._patients['ID']==_id].reset_index(drop='True')
        self._main_records = self._records[self._records['PatientID']==_id].reset_index(drop='True')
    def get_patient_personal_data(self):
        return self._main_patient[['ID','Gender','Birth']].rename(columns={'ID':'id','Gender':'gender','Birth':'birthdate'})
    def get_patients_icd_card(self):
        return patients_icd_card(self._main_records,self._main_patient).get_result()
    def get_patients_by_pattern(self, desease_set):
        tree = FPTree()
        tree.fit(self._desease_sets)
        pattern = pd.DataFrame(tree.mine(), columns=('Pattern', 'Count'))
        pattern['Length'] = pattern['Pattern'].apply(len)
        match = pattern[pattern['Pattern'].apply(desease_set.issuperset)]
        pattern = match.sort_values('Length', ascending=False).iloc[0]['Pattern']
        return list(self._desease_sets[self._desease_sets.apply(lambda x: x.issuperset(pattern))].index)
       

