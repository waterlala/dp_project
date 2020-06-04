import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from Patient import Patient
from PatientVisitor import PatientVisitor 
class CalculateInpatientCyalevisitor(PatientVisitor):
    def __init__(self):
        self.__result = None
    
    def visit_patient(self, patient):
        inpatient = patient.get_inpatient()
        cycle_data = self.__cal_intervel(inpatient)
        cycle_dict = self.__create_complete_data(cycle_data)
        cycle_dict = cycle_dict.reset_index()
        cycle_dict = cycle_dict.rename(columns = {'index':'age',0:'interval'})
        age = cycle_dict['age'].agg(lambda x: x.tolist())
        interval = cycle_dict['interval'].agg(lambda x: x.tolist())
        self.__result = pd.DataFrame(data = {'x' : [age], 'y' :[interval]})

    def __cal_intervel(self, inpatient_data):
        inpatient_data['sn'] = [x for x in range(0,len(inpatient_data))]
        cur_age = 0
        next_age = 0
        interval_list=[]
        avg_interval=[]
        age_list=[]
        if(len(inpatient_data) > 1):
            for i in range(0,len(inpatient_data)-1):
                cur_age = inpatient_data.loc[inpatient_data['sn'] == i ,'InAge'].values[0]
                next_age = inpatient_data.loc[inpatient_data['sn'] == i+1 ,'InAge'].values[0]
                next_indate= datetime.strptime(inpatient_data.loc[inpatient_data['sn'] == i+1, 'InDate'].values[0][0:10], "%Y-%m-%d") 
                cur_indate= datetime.strptime(inpatient_data.loc[inpatient_data['sn'] == i ,'InDate'].values[0][0:10], "%Y-%m-%d") 
                days = (next_indate - cur_indate).days
                #days = second.astype('timedelta64[D]') / np.timedelta64(1, 'D')
                interval_list.append(days)
                if(cur_age != next_age):
                    avg_interval.append(sum(interval_list)//len(interval_list))
                    age_list.append(cur_age)
                    interval_list=[]
                    interval_list.append(days)        
            if(len(interval_list)!=0):        
                avg_interval.append(sum(interval_list)//len(interval_list))
                age_list.append(next_age)    
            list_index = [x for x in range(0,len(age_list))]
            interval_data = pd.Series(data = avg_interval ,index = list_index)
            age_data = pd.Series(data = age_list ,index = list_index)
            return pd.DataFrame({ 'age':age_data, 'interval': interval_data})
    
    def __create_complete_data(self, cycle_data):
        default_value = 0
        interval_list = {0:default_value,5:default_value,10:default_value,15:default_value,20:default_value,25:default_value,
                        30:default_value,35:default_value,40:default_value,45:default_value,50:default_value,55:default_value,
                        60:default_value,65:default_value,70:default_value,75:default_value,80:default_value,85:default_value,
                        90:default_value,95: default_value,100:default_value}
        min = cycle_data['age'].min()
        max = cycle_data['age'].max()
        cur_age_index = -1
        for list_age in interval_list.keys():
            if list_age == min:
                interval_list[list_age] = cycle_data.loc[cycle_data['age'] == list_age,'interval'].values[0]
                cur_age_index = cycle_data.loc[cycle_data['age'] == list_age].index.values.astype(int)[0]
            elif list_age == max:
                interval_list[list_age] = cycle_data.loc[cycle_data['age'] == list_age,'interval'].values[0]
                break
            elif list_age > min and list_age < max and cur_age_index != -1:
                if list_age < cycle_data.loc[cycle_data.index == cur_age_index+1,'age'].values[0]:
                    interval_list[list_age] = cycle_data.loc[cycle_data.index == cur_age_index,'interval'].values[0]
                else:
                    interval_list[list_age] = cycle_data.loc[cycle_data.index == cur_age_index+1,'interval'].values[0]
                    cur_age_index+=1
        ans = pd.Series(data = list(interval_list.values()) ,index = (interval_list.keys()))
        return pd.DataFrame(ans)

    def get_result(self):
        return self.__result

    