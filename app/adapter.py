from IO import IO
from inpatient_cycle import InpatientCycle



#需全改 IO 要回傳dataframe 再用adapter 轉 json回傳
class Adapter:
    def __init__(self):
        pass
    def dataframe_to_json(self, dataframe):
        return self.result
        