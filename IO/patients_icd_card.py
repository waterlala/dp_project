#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


class patients_icd_card:
    def __init__(self, main_records, main_patient):
        self._main_records = main_records
        self._main_patient = main_patient
    def get_result(self):
        record = pd.merge(self._main_records[['PatientID','InDate','ICD9CM']].rename(columns={'PatientID':'ID'}),self._main_patient[['ID','Birth']],on='ID',how='left')
        record['date'] = record['InDate'] - record['Birth']
        record['date'] = record['date'].apply(lambda x: x.days)
        record = record.sort_values('date')
        save_list = list()
        out = list()
        for r in list(record['ICD9CM']):
            save = list()
            save = save_list.copy()
            for single in r:
                single = str(single)
                if single.isdigit():
                    single = int(single)
                    if single not in save_list:
                        save_list.append(single)
                        save.append(single)
            out.append(save)
        record['total_icd'] = pd.Series(out)
        record['total_icd_len'] = record['total_icd'].apply(lambda x: len(x))
        record['year'] = record['date'] / 365
        x_out = list()
        for i in range(0,record['date'].max(),365):
            x_out.append(i+1)
        out_data = pd.DataFrame()
        out_data['x'] = pd.Series(x_out)
        def get_y(x):
            df = record[record['date']<=x]
            return df['total_icd_len'].max()
        out_data['y'] = out_data['x'].apply(get_y)
        out_data = out_data.fillna(0)
        return out_data

