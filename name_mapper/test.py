import pandas as pd
from collections import Iterable


class NameMapper:
    """ Map ICD-9-CM code to correspoding chinese name.
    
    Usage:
    >>> mapper = NameMapper()
    >>> code = '001'
    >>> mapper.to_name(code)
    '霍亂(虎烈拉)'333code 
    >>> code = pd.Series(['001', '001.0', '002.x'])
    >>>
    """
    def __init__(self, file_path='name_mapper.pkl.zip'):
        self._mapper = pd.read_pickle(file_path)
        '''
    def to_name(self, code):
        
        try:
            name = name_mapper[code]
        except KeyError:
            name = None
        
        return name
        
    def to_names(self, codes):
        
        return codes.apply(self.to_name)'''