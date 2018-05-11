import sys
import getopt
import time
from datetime import datetime
import csv
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
def checkup(sym_list):

    print 'Checking up ......'

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):

    # --------------------------------------------------------------------- 
    #  Parse the command line option 
    # --------------------------------------------------------------------- 
    try:
        opts, args = getopt.getopt(argv,"hs:l:")
    except getopt.GetoptError:
        print 'task.py -s <symbol>'
        sys.exit(2)

    sym = None
    sym_list = []
    for opt, arg in opts: 
        if opt == '-h':
            print 'task.py -s csco -l \'intc, msft\''
            sys.exit(2)
        elif opt in ('-s'): 
            sym = arg
            print 'sym =', sym
            sym_list.append(sym)
        elif opt in ('-l'):
            tmp = arg.split(',')
            for item in tmp:
                sym_list.append(item.strip())

    print 'sym_list =', sym_list
    if sym_list:
        checkup(sym_list)

if __name__ == '__main__':
    main(sys.argv[1:])
