from Patient import Patient

class DataStorage():
    def __init__(self):
        self.__patient_list = []
        self.__calculated_result = {}

    def add_patient(self, patinet):
        self.__patient_list.append(patinet)

    def add_calculated_result(self, result_name, result):
        self.__calculated_result[result_name] = result

    def iter_patient_list(self):
        return self.__patient_list

    def get_group_result(self, select_result):
        return self.__calculated_result[select_result]