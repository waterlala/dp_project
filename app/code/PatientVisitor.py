import abc
from Patient import Patient

class PatientVisitor(abc.ABC):
   def __init__(self):
      self.result = None
   @abc.abstractclassmethod
   def visitPatient(self, patient):
      return NotImplemented
   @abc.abstractclassmethod
   def getResult(self):
      return NotImplemented
      
