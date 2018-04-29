import sys
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
# Calculate latest date string in the quote
#--------------------------------------------------------------------------
def latest_date_str():
    hour, minute, second = utils.current_time()
    weekday = utils.current_weekday()
    if weekday.lower() == 'sunday':
        latest_date = utils.previous_date_str(2)
    elif weekday.lower() == 'saturday':
        latest_date = utils.previous_date_str(1)
    elif weekday.lower() == 'monday':
        if int(hour) < 16:
            latest_date = utils.previous_date_str(3)
        else:
            latest_date = utils.current_date_str()
    else:
        if int(hour) < 16:
            latest_date = utils.previous_date_str(1)
        else:
            latest_date = utils.current_date_str()

    return latest_date

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
# Update Quotes
#--------------------------------------------------------------------------
def update_quotes(symbols):

    print 'Updating quotes .....'

    i = 1

    q = Quote()
    latest_date = latest_date_str()
    for sym in symbols:
        latest_date, already_up_to_date = q.update(sym, latest_date)
        if already_up_to_date is False:
            i = i + 1
            time.sleep(2)

        if i % 6 == 0: 
            print '..... i =', i, ', sleep longer'
            time.sleep(30)
            i = 1

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

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):

    begin_time = str(datetime.now()) 

    latest_date = latest_date_str()
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
        save_update_status(status)

    print '-----------------------', 'Updating filter data', '-----------------------'
    update_filters()

    end_time = str(datetime.now())

    print 'Begin:', begin_time, ', End:', end_time

if __name__ == '__main__':
    main(sys.argv[1:])
