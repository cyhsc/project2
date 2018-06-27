import os
import sys
import getopt
import time
from datetime import datetime
import csv
import pandas as pd
import config
import utils
from quote import Quote
from tech import TechData
from analysis import Analysis
from filter import Filter

RESULT_DIR = config.RESULT_DIR
status_file = RESULT_DIR + 'status.csv'

#--------------------------------------------------------------------------
#   Check up the stock
#--------------------------------------------------------------------------
def checkup(symbols):

    latest_date = utils.latest_date_str()
    q = Quote()
    td = TechData()
    a = Analysis()

    swidth = []
    swidth_pb = []
    fwidth = []
    fwidth_pb = []
    rwb = []
    macd_hist_pb = []
    swidth_roc_pb = []

    latest_timestamp = None

    for sym in symbols: 
        print '\n'
        print 'Checking up', sym, '......'
        df = q.intraday(sym)

        if latest_timestamp is None:
            latest_timestamp = df.index[-1]

        td.macd(df)
        td.ma(df)
        td.guppy(df)
        a.guppy_alignment(df)
        a.guppy_roc(df)

        tmp_df = df[['swidth', 'swidth_pb', 'fwidth', 'fwidth_pb', 'rwb', 'macd_hist_pb', 'swidth_roc_pb']]
        print '++++++++', sym, '+++++++++'
        print tmp_df.tail(5)

        swidth.append(df['swidth'][-1])
        swidth_pb.append(df['swidth_pb'][-1])
        fwidth.append(df['fwidth'][-1])
        fwidth_pb.append(df['fwidth_pb'][-1])
        rwb.append(df['rwb'][-1])
        macd_hist_pb.append(df['macd_hist_pb'][-1])
        swidth_roc_pb.append(df['swidth_roc_pb'][-1])

    total_df = pd.DataFrame(index = symbols)
    total_df['swidth'] = swidth
    total_df['swidth_pb'] = swidth_pb
    total_df['fwidth'] = fwidth
    total_df['fwidth_pb'] = fwidth_pb
    total_df['rwb'] = rwb
    total_df['macd_hist_pb'] = macd_hist_pb
    total_df['swidth_roc_pb'] = swidth_roc_pb

    print '\n'
    print '---------------------------------', latest_timestamp, '---------------------------------'
    print total_df

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    # --------------------------------------------------------------------- 
    #  Parse the command line option 
    # --------------------------------------------------------------------- 
    try:
        opts, args = getopt.getopt(argv,"hs:l:f:")
    except getopt.GetoptError:
        print 'task.py -s <symbol>'
        sys.exit(2)

    sym = None
    sym_list = []
    for opt, arg in opts: 
        if opt == '-h':
            print 'task.py -s csco -l \'intc, msft\' -f filename'
            sys.exit(2)
        elif opt == '-s': 
            sym = arg
            print 'sym =', sym
            sym_list.append(sym.upper())
        elif opt == '-l':
            tmp = arg.split(',')
            for item in tmp:
                sym_list.append(item.strip().upper())
        elif opt == '-f':
            symbol_file = arg
            print symbol_file
            if os.path.isfile(symbol_file): 
                print 'Reading file', symbol_file, '....'
                lines = open(symbol_file, 'r').read().split('\n')
                for line in lines:
                    # Skip empty lines
                    if len(line) == 0:
                        continue
            
                    sym_list.append(line.strip('\n'))
            else:
                print 'File', symbol_file, 'doesnot exist'
                return

    print 'sym_list =', sym_list
    if sym_list:
        checkup(sym_list)

if __name__ == '__main__':
    main(sys.argv[1:])
