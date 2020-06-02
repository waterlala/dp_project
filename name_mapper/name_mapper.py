import pandas as pd
from collections import Iterable


class NameMapper:
    """ Map ICD-9-CM code to correspoding chinese name.
    
    Usage:
    # before create a NameMapper object, please check the
    # 'name_mapper.pkl.zip' file is exist.
    >>> mapper = NameMapper()
    # you can also specify the path
    >>> mapper = NameMapper(file_path='name_mapper.pkl.zip')
    >>> code = '001'
    >>> mapper.to_name(code)
    '霍亂(虎烈拉)'
    >>> code = pd.Series(['001', '001.0', '002.x'])
    >>> mapper.to_names(codes)
    001        霍亂(虎烈拉)
    001.0    霍亂弧菌所致的霍亂
    002.x          NaN
    Name: Name, dtype: object
    """
    def __init__(self, file_path='name_mapper.pkl.zip'):
        self._mapper = pd.read_pickle(file_path)
        
    def to_name(self, code):
        """Return chinese name of code, return None if code is not exist."""
        try:
            name = self._mapper[code]
        except KeyError:
            name = None
        
        return name
        
    def to_names(self, codes):
        """Allow input list of code and return Series object of names."""
        return pd.Series(codes).apply(self.to_name)