import numpy as np
import pandas as pd
import os
import sys
import utils
import config
import filter

DATA_DIR = config.DATA_DIR
ANALYSIS_DIR = config.ANALYSIS_DIR
RESULT_DIR = config.RESULT_DIR

def basic_trend():
    print '=============================================  ETF  ==================================================='
    df = pd.read_csv(RESULT_DIR + 'basic_trend_etf.csv', index_col = 0)
    print df
    print '=============================================  STOCK ==================================================='
    df = pd.read_csv(RESULT_DIR + 'basic_trend_stock.csv', index_col = 0)
    print df

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    basic_trend()

if __name__ == '__main__':
    main(sys.argv[1:])
