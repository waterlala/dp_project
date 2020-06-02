import numpy as np
import pandas as pd

class Patient():
    def __init__(self, id, gender, birth, death, record, inpatient):
        self._id = id
        self._gender = gender
        self._birth = birth
        self._death = death
        self._record = record #dataframe
        self._inpatient = inpatient #dataframe
    
    def get_id(self):
        return self._id
    def get_gender(self):
        return self._gender
    def get_birth(self):
        return self._birth
    def get_death(self):
        return self._death
    def get_record(self):
        return self._record
    def get_inpatinet(self):
        return self._inpatient
    def accept_vistor(self, vistor):
        vistor.visit_patient(self)
    