from Patient import Patient

class DataStorage():
    def __init__(self):
        self._patient_list = []
        self._calculated_result = {}

    def add_patient(self, patinet):
        self._patient_list.append(patinet)

    def add_calculated_result(self, result_name, result):
        self._calculated_result[result_name] = result

    def iter_patient_list(self):
        return self._patient_list

    def calculate_result(self, select_result):
        return self._calculated_result[select_result]