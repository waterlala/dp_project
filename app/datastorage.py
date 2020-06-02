from patient import Patient


class DataStorage():
    def __init__(self):
        self.patient_list = []

    def add_patient(self, patinet):

        self.patient_list.append(patinet)
    def accept_visitor(self, visitor):
        visitor.visit_storage(self)