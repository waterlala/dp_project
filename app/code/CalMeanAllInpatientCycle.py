import pandas as pd
import numpy as np
import math
from datetime import date, datetime, timedelta
from Patient import Patient
from PatientVisitor import PatientVisitor 

class CalMeanAllInpatientCycle(PatientVisitor):
    def __init__(self):
        self.__result = None
    def visit_patient(self, patient):
        inpatient = patient.get_inpatient()
        if(type(inpatient) != type(None)):
            inpatient['InAge'] = inpatient['InAge'] //5 *5
            cycle_data = self.__cal_intervel(inpatient)
            if(type(cycle_data) != type(None)):
                cycle_data['ID'] = patient.get_id()
                if (type(self.__result) == type(None)):
                    self.__result = cycle_data
                else:
                    self.__result = pd.concat([self.__result, cycle_data])

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
            return pd.DataFrame({ 'age':age_data, 'cycle': interval_data})
    
    def get_result(self):
        cycle_list = []
        age_list = []
        for age in range (0,101,5):
            age_list.append(age)
            avg = self.__result.loc[self.__result['age'] == age,'cycle'].mean()
            if(math.isnan(avg)):
                cycle_list.append(0)
            else:
                cycle_list.append(avg)
        return pd.DataFrame(data = {'x' : [age_list], 'y' :[cycle_list]})