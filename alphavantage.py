################################################################################################################################ 
# https://github.com/RomelTorres/alpha_vantage
################################################################################################################################ 

import os
import sys
import time
from urllib2 import urlopen
import urllib2
import pandas as pd
import random
import json
from alpha_vantage.timeseries import TimeSeries
import config

class AlphaVantage:

    def __init__(self, last_date = None):
        self.key = config.get_alphavantage_key()
        self.last_date = last_date
        self.ts = TimeSeries(key=self.key, retries=5, output_format='pandas', indexing_type='date')

    def compact_quotes(self, sym):
        try: 
            df, m = self.ts.get_daily(sym, outputsize='compact')   
        except:
            print 'Compact quote get caused exception'
            return None

        if df is not None:
            df = df.rename(columns = {'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
            df = df[['open', 'high', 'low', 'close', 'volume']] 
        return df

    def full_quotes(self, sym):
        try: 
            df, m = self.ts.get_daily(sym, outputsize='full')   
        except:
            print 'Full quote get caused exception'
            return None

        if df is not None:
            df = df.rename(columns = {'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
            df = df[['open', 'high', 'low', 'close', 'volume']] 
        return df

    def compact_quotes_intraday(self, sym):
        try: 
            df, m = self.ts.get_intraday(sym, interval='30min', outputsize='compact')
        except:
            print 'Compact quote intraday get caused exception'
            return None

        if df is not None:
            df = df.rename(columns = {'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
            df = df[['open', 'high', 'low', 'close', 'volume']]
        return df

    def full_quotes_intraday(self, sym):
        try: 
            df, m = self.ts.get_intraday(sym, interval='30min', outputsize='full')
        except:
            print 'Full quote intraday get caused exception'
            return None

        if df is not None:
            df = df.rename(columns = {'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
            df = df[['open', 'high', 'low', 'close', 'volume']]
        return df

    def quotes_weekly(self, sym):
        try: 
            df, m = self.ts.get_weekly(sym)
        except:
            print 'Weekly quote get caused exception'
            return None

        if df is not None:
            df = df.rename(columns = {'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
            df = df[['open', 'high', 'low', 'close', 'volume']]
        return df

    def quotes_monthly(self, sym):
        try: 
            df, m = self.ts.get_monthly(sym)
        except:
            print 'Weekly quote get caused exception'
            return None

        if df is not None:
            df = df.rename(columns = {'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
            df = df[['open', 'high', 'low', 'close', 'volume']]
        return df
