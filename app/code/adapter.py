import pandas as pd
import numpy as np
import json
from InOutput import InOutput

#需全改 IO 要回傳dataframe 再用adapter 轉 json回傳
class Adapter(InOutput):
    def __init__(self, io):
        self.__io = io
    def handle_instructions(self, instructions, id):
        result = self.__io.handle_instructions(instructions, id)
        if(isinstance(result, None)):
            return "{}"
        elif(isinstance(result, pd.DataFrame)):
            return result.to_json(orient='index')
        elif(isinstance(result,float)):
            float_dict = {}
            float_dict["instructions"] = result
            return json.dumps(float_dict)
            