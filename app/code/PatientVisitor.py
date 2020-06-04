import abc
from Patient import Patient

class PatientVisitor(abc.ABC):
   def __init__(self):
      self.__result = None
   @abc.abstractclassmethod
   def visit_patient(self, patient):
      return NotImplemented
   @abc.abstractclassmethod
   def get_result(self):
      return NotImplemented
      
