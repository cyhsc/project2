import sys
import getopt
import time
from datetime import datetime
import pandas as pd
import csv
import config
import utils
from quote import Quote
from tech import TechData
from analysis import Analysis
from filter import Filter
from iex import IEX

DATA_DIR = config.DATA_DIR
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

def update_quotes_batch(symbols):

    iex = IEX()
    date, temp_open, temp_high, temp_low, temp_close, temp_volume = iex.quote('SPY')
    print 'Latest date string is', date
    quotes = iex.batch_quotes(symbols)
    for key in quotes:
        print key, quotes[key]
        sym = key
        df = utils.read_quote_file(sym)
        if date not in df.index:
            open = float(quotes[key][0])
            high = float(quotes[key][1])
            low = float(quotes[key][2])
            close = float(quotes[key][3])
            volume = int(quotes[key][4])
            row = pd.Series({'open':open,'high':high,'low':low,'close':close,'volume':volume},name=date)
            df = df.append(row)
            df.to_csv(DATA_DIR + sym + '.csv')

def update_quotes_bulk():

    symbol_files = ['symbols_etf.csv', 'symbols_stock.csv']
    for f in symbol_files:
        print '-----------------------', 'Updating data for symbols in', f, '-----------------------'
        symbols, names = utils.read_symbol_file(f)
        update_quotes_batch(symbols)

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
    f.three_percent('stock')
    f.three_percent_track('stock')

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
        opts, args = getopt.getopt(argv,"hbs:l:")
    except getopt.GetoptError:
        print 'task.py -s <symbol>'
        sys.exit(2)

    sym = None
    sym_list = []
    for opt, arg in opts: 
        if opt == '-h':
            print 'task.py -s csco -l \'intc, msft\''
            sys.exit(2)
        elif opt == '-b':
            print 'Bulk updating ...'
            update_quotes_bulk()
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
