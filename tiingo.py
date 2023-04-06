"""
Light tiingo market data wrapper
kai.nb.mcpheeters
July 31st 2020
"""

import requests
from pandas import DataFrame 
from datetime import date, datetime, timedelta
TOKEN = 'd2119c6f723335d438c95a85c3f4e4e76fd4f7b9' # Please change to your own token, get for free at https://api.tiingo.com/

def formatDate(isodate_string):
    return datetime.fromisoformat(isodate_string[:-1]).date()

class Market (object):
    def __init__(self, ticker):
        self.ticker = ticker
        self.headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token ' + TOKEN
        }
    def __repr__(self):
        return self.ticker + '()'

    def getPrices(self, startDate=date.today()-timedelta(365),endDate=date.today()):
        '''Get End of Day Market Data, returns pandas dataframe'''
        requestResponse = requests.get(f"https://api.tiingo.com/tiingo/daily/{self.ticker}/prices?startDate={startDate}&endDate={endDate}", headers=self.headers)
        df = DataFrame(requestResponse.json())
        df['ticker'] = self.ticker
        df['date'] = df['date'].apply(formatDate)
        return df