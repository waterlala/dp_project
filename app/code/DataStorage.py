from Patient import Patient

class DataStorage():
    def __init__(self):
        self._patient_list = []

    def add_patient(self, patinet):
        self._patient_list.append(patinet)
    def accept_visitor(self, visitor):
        visitor.visit_storage(self)