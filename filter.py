import pandas as pd
import numpy as np
import config
import utils

RESULT_DIR = config.RESULT_DIR

class Filter:

    def __init__(self):
        pass

    def basic_trend(self, type): 

        if type == 'etf': 
            symbol_file = 'symbols_etf.csv'
        elif type == 'stock':
            symbol_file = 'symbols_stock.csv'
        else:
            print 'Enter valid type, etf or stock'
            return
 
        symbols, names = utils.read_symbol_file(symbol_file)
      
        slow_align_total = []
        fast_align_total = []
        slow_roc_total = []
        fast_roc_total = []
        for sym in symbols: 
            df = utils.read_analysis_file(sym)
            if df is None:
                print 'Analysis file for', sym, ' doesnot exist'
                continue

            slow_align_total.append(df['slow_align_total'][-1])
            slow_roc_total.append(df['slow_roc_total'][-1])
            fast_align_total.append(df['fast_align_total'][-1])
            fast_roc_total.append(df['fast_roc_total'][-1])

        align_total_df = pd.DataFrame(index = symbols)
        align_total_df['name'] = names
        align_total_df['slow_align_total'] = slow_align_total
        align_total_df['slow_roc_total'] = slow_roc_total
        align_total_df['fast_align_total'] = fast_align_total
        align_total_df['fast_roc_total'] = fast_roc_total
    
        ret_df = align_total_df.sort_values(['slow_align_total', 'slow_roc_total', 'fast_align_total', 'fast_roc_total'], ascending=[False, False, False, False])

        ret_df.to_csv(RESULT_DIR + 'result_' + type + '.csv')

        return ret_df
