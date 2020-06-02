# InpatientCycle.py
import numpy as np
import pandas as pd
import math
import json
from datetime import date, datetime, timedelta

class InpatientCycle:
    """ Get patients' inpatinet cycle
    Usage:
        To initialize this class need the one dataframe, inpatient, 
        which you have load before.  

        When initilizing inpatient cycle class, it will call the function 
        calculate_inpatient_cycle automatically and stores the inpatient 
        cycle of everypatient with dataframe.

        If you want the single patient's inpatient cycle, just call the 
        function get_inpatient_cycle_of_single_patient with target patient's ID.
        It will return jsonString as following
        '{x:[20, 25, 30,....., 90], 
         y:[0, 0, 0, 40, 40, 30, 30,....., 0]}'
        (x is age, y is days or week or month of cycle) 

        To get the inpatient cycle about the everypatient, just call the function 
        get_average_of_inpatient_cycle_of_everypatient without any id.
        Its content of return is same as the function get_inpatient_cycle_of_single_patient.
        The different is that it is everypatient's average of inpatient cycle
    """
    def __init__(self, inpatient):
        """ Load inpatient dataframe data """
        #self._inpatient = inpatient
        #self._calculate_inpatient_cycle(inpatient) calulate time :5min
        #self._all_inpatient_cycle = pd.read_pickle('all_inpatient_cycle.pkl')
        self._all_inpatient_cycle = pd.read_pickle('./all_inpatient_cycle_avg.pkl')
        self._inpatient_cycle_of_single_male = pd.read_pickle("./inpatient_cycle_of_single_male.pkl")
        self._inpatient_cycle_of_single_female = pd.read_pickle("./inpatient_cycle_of_single_female.pkl")

    def _calculate_inpatient_cycle(self,inpatients_input):
        """ Calculate everypatient's inpatient cycle """

        #in_clean_data = inpatients_input.loc[:,['ID','InDate','OutDate','InAge']] if load inpatient
        inpatients_input = inpatients_input.dropna(subset=['InAge'])# record_inpatient
        in_clean_data = inpatients_input.loc[:,['PatientID','InDate','OutDate','InAge']]# record_inpatient
        in_clean_data.rename(columns={'PatientID':'ID'}, inplace=True)# record_inpatient
        in_clean_data['InAge'] = in_clean_data['InAge'] //5 *5
        #call function
        interval_data = in_clean_data.groupby('ID').apply(self._cal_intervel)
        interval_data = interval_data.reset_index()
        interval_data.rename(columns={'level_1':'sn'}, inplace=True)
        #call function
        all_inpatient_cycle = interval_data.groupby('ID').apply(self._create_complete_data)
        all_inpatient_cycle = all_inpatient_cycle.reset_index()
        all_inpatient_cycle.rename(columns={'level_1':'age', 0:'cycle'}, inplace=True)
        self._all_inpatient_cycle = all_inpatient_cycle


    def get_average_of_inpatient_cycle_of_everypatient(self):
        """ Get the jsonstring of average of inpatient cycle of each patient """
        """result = {}
        x=[]
        y=[]
        for i in range (0,101,5):
            avg = self._all_inpatient_cycle.loc[self._all_inpatient_cycle['age'] == i,'cycle'].mean()
            x.append(i)
            if math.isnan(avg):
                y.append(0)
            else:
                y.append(int(avg))
        result['x'] = x
        result['y'] = y"""
        result = {}
        x=[]
        y=[]
        for i in range (0,101,5):
            avg = self._all_inpatient_cycle.loc[self._all_inpatient_cycle['age'] == i,'avg_cycle'].values[0]
            x.append(i)
            if math.isnan(avg):
                y.append(0)
            else:
                y.append(int(avg))
        result['x'] = x
        result['y'] = y
        return json.dumps(result)

    def get_inpatient_cycle_of_single_patient(self, patient_id):
        """ Get the jsonstring of inpatient cycle of single patient """
        """result = {}
        x=[]
        y=[]
        if(len(all_inpatient_cycle.loc[all_inpatient_cycle['ID'] == id,:]) == 0):
            return "{}"
        the_patient = self._all_inpatient_cycle.loc[self._all_inpatient_cycle['ID'] == patient_id,:]
        for i in range (0,101,5):
            cycle = the_patient.loc[the_patient['age'] == i,'cycle'].values[0]
            x.append(i)
            if math.isnan(cycle):
                y.append(0)
            else:
                y.append(int(cycle))
        result['x'] = x
        result['y'] = y"""
        result = {}
        x=[]
        y=[]
        
        for i in range (0,101,5):
            if (patient_id == "015b8ac98a1019c00a3d16d2db53bb42"): #male
                cycle = self._inpatient_cycle_of_single_male.loc[self._inpatient_cycle_of_single_male['age'] == i,'avg_cycle'].values[0]
            elif(patient_id == "045e9bc49edc71780d8a280abe3bb985"): #female
                cycle = self._inpatient_cycle_of_single_female.loc[self._inpatient_cycle_of_single_female['age'] == i,'avg_cycle'].values[0]
            else:
                return "{}"
            x.append(i)
            if math.isnan(cycle):
                y.append(0)
            else:
                y.append(int(cycle))
        result['x'] = x
        result['y'] = y
        return json.dumps(result)


    def _cal_intervel(self, data):
        data['sn'] = [x for x in range(0,len(data))]
        cur_age = 0
        next_age = 0
        interval_list=[]
        avg_interval=[]
        age_list=[]
        if(len(data) > 1):
            for i in range(0,len(data)-1):
                cur_age = data.loc[data['sn'] == i ,'InAge'].values[0]
                next_age = data.loc[data['sn'] == i+1 ,'InAge'].values[0]
                second = data.loc[data['sn'] == i+1, 'InDate'].values[0] - data.loc[data['sn'] == i ,'InDate'].values[0]
                days = second.astype('timedelta64[D]') / np.timedelta64(1, 'D')
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

    def _create_complete_data(self, data):
        interval_list = {0:np.nan,5:np.nan,10:np.nan,15:np.nan,20:np.nan,25:np.nan,
                        30:np.nan,35:np.nan,40:np.nan,45:np.nan,50:np.nan,55:np.nan,
                        60:np.nan,65:np.nan,70:np.nan,75:np.nan,80:np.nan,85:np.nan,
                        90:np.nan,95: np.nan,100:np.nan}
        min = data['age'].min()
        max = data['age'].max()
        cur_age_index = -1
        for list_age in interval_list.keys():
            if list_age == min:
                interval_list[list_age] = data.loc[data['age'] == list_age,'interval'].values[0]
                cur_age_index = data.loc[data['age'] == list_age,'sn'].values[0]
            elif list_age == max:
                interval_list[list_age] = data.loc[data['age'] == list_age,'interval'].values[0]
                break
            elif list_age > min and list_age < max and cur_age_index != -1:
                if list_age < data.loc[data['sn'] == cur_age_index+1,'age'].values[0]:
                    interval_list[list_age] = data.loc[data['sn'] == cur_age_index,'interval'].values[0]
                else:
                    interval_list[list_age] = data.loc[data['sn'] == cur_age_index+1,'interval'].values[0]
                    cur_age_index+=1
        ans = pd.Series(data = list(interval_list.values()) ,index = (interval_list.keys()))
        return pd.DataFrame(ans)








