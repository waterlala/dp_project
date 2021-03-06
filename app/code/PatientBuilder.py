import numpy as np
import pandas as pd
from Patient import Patient

class PatientBuilder():
    def __init__(self):
        self._result = None

    def build_patient(self, id, gender, birth, death, record, inpatient):
        self._result =  Patient(id, gender, birth, death, record, inpatient)

    def get_result(self):
        return self._result