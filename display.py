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
    temp_df = df[(df.swidth_pb > 70) & (df.rwb >= 0) & ((df.macd_hist_pb >= 1) | (df.fwidth_pb >= 1))]
    print temp_df
    print '=============================================  STOCK ==================================================='
    df = pd.read_csv(RESULT_DIR + 'basic_trend_stock.csv', index_col = 0)
    temp_df = df[(df.swidth_pb > 70) & (df.rwb >= 0) & ((df.macd_hist_pb >= 1) | (df.fwidth_pb >= 1))]
    print temp_df

def basic_trend_emerging():
    print '=============================================  ETF  ==================================================='
    df = pd.read_csv(RESULT_DIR + 'basic_trend_etf.csv', index_col = 0)
    temp_df = df[(((df.macd_hist_pb >= 1) & (df.macd_hist_pb <= 3)) | ((df.fwidth_pb >= 1) & (df.fwidth_pb <= 3))) & (df.swidth_pb > 70) & (df.rwb >= 0)]
    print temp_df
    print '=============================================  STOCK ==================================================='
    df = pd.read_csv(RESULT_DIR + 'basic_trend_stock.csv', index_col = 0)
    temp_df = df[(((df.macd_hist_pb >= 1) & (df.macd_hist_pb <= 3)) | ((df.fwidth_pb >= 1) & (df.fwidth_pb <= 3))) & (df.swidth_pb > 70) & (df.rwb >= 0)]
    print temp_df

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    print '\n###################################################     Emerging     ######################################################\n'

    basic_trend_emerging()

    print '\n###################################################       All        ######################################################\n'

    basic_trend()

if __name__ == '__main__':
    main(sys.argv[1:])
