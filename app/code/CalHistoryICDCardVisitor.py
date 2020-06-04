import numpy as np
import pandas as pd
import datetime
from PatientVisitor import PatientVisitor

class CalHistoryICDCardVisitor(PatientVisitor):
    def visit_patient(self, patient):
        df = patient.get_record()[['ID','InDate','ICD9CM']].reset_index(drop=True)
        df['Birth'] = patient.get_birth()
        df['InDate'] = df['InDate'].astype('datetime64')
        df['Birth'] = df['Birth'].astype('datetime64')
        df['date'] = df['InDate'] - df['Birth']
        df['date'] = df['date'].apply(lambda x: x.days)
        df = df.sort_values('date')
        save_list = list()
        out = list()
        for r in list(df['ICD9CM']):
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
        df['total_icd'] = pd.Series(out)
        df['total_icd_len'] = df['total_icd'].apply(lambda x: len(x))
        df['year'] = df['date'] / 365
        x_out = list()
        for i in range(0,df['date'].max(),365):
            x_out.append(i+1)
        out_data = pd.DataFrame()
        out_data['x'] = pd.Series(x_out)
        def get_y(x):
            s_df = df[df['date']<=x]
            return s_df['total_icd_len'].max()
        out_data['y'] = out_data['x'].apply(get_y)
        out_data = out_data.fillna(0)
        out_data_x = list(out_data['x'])
        out_data_y = list(out_data['y'])
        self.__result = pd.DataFrame(data = {'x':[out_data_x],'y':[out_data_y]})
    def get_result(self):
        return self.__result
        