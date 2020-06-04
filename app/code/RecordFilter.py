import abc
import pandas as pd
class RecordFilter(abc.ABC):
   def __init__(self):
      pass
   @abc.abstractclassmethod
   def execute(self, record):
      return NotImplemented