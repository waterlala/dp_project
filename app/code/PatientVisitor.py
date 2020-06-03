from Patient import Patient

class PatientVisitor:
   def __init__(self):
      self.result = None
   def visitPatient(self, patient):
      pass
   def getResult(self):
      return self.result
      
