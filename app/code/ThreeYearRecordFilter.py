from RecordFilter import RecordFilter

class ThreeYearRecordFilter(RecordFilter):
    def __init__(self, confirm_date):
        self._confirm_date = confirm_date
    def execute(self, record):
        df = record
        df['confirm_date'] = self._confirm_date
        df['InDate'] = df['InDate'].astype('datetime64')
        df['different'] = df['confirm_date'] - df['InDate']
        df['different'] = df['different'].apply(lambda x: x.days)
        df = df[(df['different']>=0)&(df['different']<=365*3)]
        df = df.drop(['confirm_date','different'],axis = 1)
        df = df.reset_index(drop = True)
        return df