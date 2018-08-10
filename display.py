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

def basic_trend(type):
    if type == 'etf': 
        print '=============================================  ETF  ==================================================='
        filename = 'basic_trend_etf.csv'
    else:
        print '=============================================  STOCK ==================================================='
        filename = 'basic_trend_stock.csv'

    df = pd.read_csv(RESULT_DIR + filename, index_col = 0)
    temp_df = df[(df.swidth_pb >= 1) & (df.rwb >= 0) & (df.fwidth_pb >= 1)]
    print temp_df[['name', 'slow_align_total', 'slow_roc_total', 'rwb', 'swidth_pb', 'fwidth_pb', 'macd_hist_pb', 'swidth_roc_pb', 'diff_slow_kd_pb', 'slowk', 'slowd']]

def basic_trend_emerging(type):
    if type == 'etf': 
        print '=============================================  ETF  ==================================================='
        filename = 'basic_trend_etf.csv'
    else:
        print '=============================================  STOCK ==================================================='
        filename = 'basic_trend_stock.csv'
        
    df = pd.read_csv(RESULT_DIR + filename, index_col = 0)
    temp_df = df[((df.macd_hist_pb == 1) | (df.fwidth_pb == 1)) & (df.swidth_pb >= 1) & (df.rwb >= 0)]
    print temp_df[['name', 'slow_align_total', 'slow_roc_total', 'rwb', 'swidth_pb', 'fwidth_pb', 'macd_hist_pb', 'swidth_roc_pb', 'diff_slow_kd_pb', 'slowk', 'slowd']]

def basic_trend_stoch_cross(type):
    if type == 'etf': 
        print '=============================================  ETF  ==================================================='
        filename = 'basic_trend_etf.csv'
    else:
        print '=============================================  STOCK ==================================================='
        filename = 'basic_trend_stock.csv'

    df = pd.read_csv(RESULT_DIR + filename, index_col = 0)
    temp_df = df[(df.diff_slow_kd_pb == 1) & ((df.slowk < 50) | (df.slowd < 50)) & (df.swidth_pb >= 1) & (df.rwb >= 0) & (df.fwidth_pb >= 1)]
    print temp_df[['name', 'slow_align_total', 'slow_roc_total', 'rwb', 'swidth_pb', 'fwidth_pb', 'macd_hist_pb', 'swidth_roc_pb', 'diff_slow_kd_pb', 'slowk', 'slowd']]

def column_names():
    df = pd.read_csv(ANALYSIS_DIR + 'SPY_analysis.csv', index_col = 0)
    print df.columns.values.tolist()

def show_one_stock(sym, col, rows):
    print sym, col
    print type(rows)
    r = int(rows)
    df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)
    if col == []:
        if r != 0:
            print df[-r:]
        else:
            print df
    else:
        if r != 0:
            print df[col][-r:]
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
        opts, args = getopt.getopt(argv,"hns:c:r:")
    except getopt.GetoptError:
        print 'display.py '
        sys.exit(2)

    sym = None
    col = []
    rows = 0

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
        elif opt in ('-r'):
            rows = arg

    if sym is not None:
        show_one_stock(sym.upper(), col, rows)
        sys.exit(2)

    print '\n###################################################     Emerging     ######################################################\n'

    basic_trend_emerging('etf')
    basic_trend_emerging('stock')

    print '\n###################################################     Stoch Cross     ######################################################\n'

    basic_trend_stoch_cross('etf')
    basic_trend_stoch_cross('stock')

    print '\n###################################################       All        ######################################################\n'

    basic_trend('etf')
    basic_trend('stock')

if __name__ == '__main__':
    main(sys.argv[1:])
