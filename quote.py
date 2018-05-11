import os
import sys
import time
import pandas as pd
import json
import config
from alphavantage import AlphaVantage

DATA_DIR = config.DATA_DIR
CONFIG_DIR = config.CONFIG_DIR

DEFAULT_LOOKBACK = 3

class Quote:

    def __init__(self):
        pass

    def trim_quotes(self, quote_df, years):
        index = quote_df.index
        begin_year = index[0].split('-')[0]
        begin_month = index[0].split('-')[1]
        begin_day = index[0].split('-')[2]
        end_year = index[-1].split('-')[0]
        end_month = index[-1].split('-')[1]
        end_day = index[-1].split('-')[2]
        if (int(end_year) - years) > int(begin_year):
            begin_year = str(int(end_year) - years)
        begin_month = end_month
        begin_day = end_day
        new_begin = begin_year + '-' + begin_month + '-' + begin_day

        for i, item in enumerate(index):
            if item > new_begin:
                break

        return quote_df[i:]

    def get_quotes_alphavantage(self, sym, compact = True):
        av = AlphaVantage()
        if compact is True: 
            return av.compact_quotes(sym)
        else:
            return av.full_quotes(sym)

    def update(self, sym, latest_date = None, lookback = DEFAULT_LOOKBACK):

        print 'Updating quote for', sym, '.....' 

        already_up_to_date = False

        if os.path.isfile(DATA_DIR + sym + '.csv'):
            print 'Quote file for', sym, 'exists, read it in'
            df = pd.read_csv(DATA_DIR + sym + '.csv', index_col = 0)
            print 'latest_date =', latest_date, 'last_index =', df.index[-1]

            if latest_date is None or df.index[-1] < latest_date:
                print 'Donot know latest date or latest date in file not up to date'
                new_df = self.get_quotes_alphavantage(sym, True)

                if new_df is None: 
                    return None, already_up_to_date

                print 'Got quote for symbol:', sym, ', Last index =', new_df.index[-1]

                if df.index[-1] < new_df.index[-1]:
                    while new_df.index[0] <= df.index[-1]:
                        new_df = new_df.drop(new_df.index[0])

                    if new_df.empty is False:
                        df = df.append(new_df)
                else:
                    already_up_to_date = True
                    print 'Quote data already up to date'
            else:
                already_up_to_date = True
                print 'Quote data already up to date'
        else:
            print 'Quote file for', sym, 'doesnot exist'
            df = self.get_quotes_alphavantage(sym, False)
            print 'Got quote for symbol:', sym, ', Last index =', df.index[-1]

        if df is not None:
            df = self.trim_quotes(df, lookback)
            df.to_csv(DATA_DIR + sym + '.csv')
            return df.index[-1], already_up_to_date
        else:
            return None, already_up_to_date

    def intraday(self, sym):
        av = AlphaVantage()
        df = av.full_quotes_intraday(sym)
