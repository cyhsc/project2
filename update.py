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
# Get update status 
#--------------------------------------------------------------------------
def get_update_status():
    reader = csv.reader(open(status_file, 'r'))
    d = {}
    for row in reader:
       k, v = row
       d[k] = v

    print d
    return d

#--------------------------------------------------------------------------
# Save update status 
#--------------------------------------------------------------------------
def save_update_status(status):
    with open(status_file,'wb') as f:
        w = csv.writer(f)
        w.writerows(status.items())
    

#--------------------------------------------------------------------------
# Update quotes, tech_data and analysis
#   
# Arguments:
#    - symbols: list of symbols
#--------------------------------------------------------------------------
def update_quotes(symbols):

    print 'Updating quotes .....'

    i = 1

    q = Quote()
    latest_date = utils.latest_date_str()
    for sym in symbols:
        new_latest_date, already_up_to_date = q.update(sym, latest_date)

        if new_latest_date > latest_date:
            latest_date = new_latest_date

        if already_up_to_date is False:
            i = i + 1
            #time.sleep(1)

        #if i % 5 == 0: 
        #    print '..... i =', i, ', sleep longer'
        #    time.sleep(10)
        #    i = 1

def update_tech_data(symbols):
    print 'Updating technical data .....'
    td = TechData()
    for sym in symbols:
        td.update(sym)

def update_analysis(symbols):
    print 'Updating analysis data .....'
    a = Analysis()
    for sym in symbols: 
        a.update(sym)

def update_filters():
    f = Filter()
    f.basic_trend('etf')
    f.basic_trend('stock')

#--------------------------------------------------------------------------
#   Update everything in database
#--------------------------------------------------------------------------
def update_all():

    print 'Updating all ......'

    begin_time = str(datetime.now())

    latest_date = utils.latest_date_str()
    status = get_update_status()

    symbol_files = ['symbols_etf.csv', 'symbols_stock.csv']
    for f in symbol_files:
        print '-----------------------', 'Updating data for symbols in', f, '-----------------------'
        print latest_date, len(latest_date)
        print status[f], len(status[f])
        if latest_date == status[f]:
            print '   - Symbols in', f, 'already update to date'
            continue
        symbols, names = utils.read_symbol_file(f)

        update_quotes(symbols)
        update_tech_data(symbols)
        update_analysis(symbols)

        status[f] = latest_date
        save_update_status(status)

    print '-----------------------', 'Updating filter data', '-----------------------'
    update_filters()

    end_time = str(datetime.now())

    print 'Begin:', begin_time, ', End:', end_time

#--------------------------------------------------------------------------
#   Update list of symbols
#--------------------------------------------------------------------------
def update(symbols):
    print symbols
    return
    update_quotes(symbols)
    update_tech_data(symbols)
    update_analysis(symbols)

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):

    # --------------------------------------------------------------------- 
    #  Default action, update everything
    # --------------------------------------------------------------------- 
    if not argv: 
        update_all()
        return

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
        update(sym_list)

if __name__ == '__main__':
    main(sys.argv[1:])
