import numpy as np
import pandas as pd
import os
import sys
import getopt
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

def column_names():
    df = pd.read_csv(ANALYSIS_DIR + 'SPY_analysis.csv', index_col = 0)
    print df.columns.values.tolist()

def show_one_stock(sym, col):
    print sym, col
    df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)
    if col == []:
        print df
    else:
        print df[col]

# ==============================================================================
#   Main
#
#     * '-h': Help
#     * '-n': Display column names of analysis file
#     * '-s': Symbol of analysis file to be displayed
#     * '-c': Columns of analysis file to be displayed, should be comma separated strings
#
#   Example
#     > python display.py -s CSCO -c open,close,macd
# ==============================================================================
def main(argv):

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    # ---------------------------------------------------------------------
    #  Parse the command line option
    # ---------------------------------------------------------------------
    try:
        opts, args = getopt.getopt(argv,"hns:c:")
    except getopt.GetoptError:
        print 'display.py '
        sys.exit(2)

    sym = None
    col = []

    for opt, arg in opts:
        if opt == '-h':
            print 'display.py -hns:c:'
            sys.exit(2)
        elif opt == '-n':
            column_names()
            sys.exit(2)
        elif opt in ('-s'):
            sym = arg
        elif opt in ('-c'):
            col = arg.split(',')

    if sym is not None:
        show_one_stock(sym.upper(), col)
        sys.exit(2)

    print '\n###################################################     Emerging     ######################################################\n'

    basic_trend_emerging()

    print '\n###################################################       All        ######################################################\n'

    basic_trend()

if __name__ == '__main__':
    main(sys.argv[1:])
