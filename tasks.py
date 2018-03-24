import sys
import time
from datetime import datetime
import config
import utils
from quote import Quote
from tech import TechData
from analysis import Analysis
from filter import Filter

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

def update_quotes(symbols):

    print 'Updating quotes .....'

    q = Quote()
    latest_date = latest_date_str()
    for sym in symbols:
        latest_date, already_up_to_date = q.update(sym, latest_date)
        if already_up_to_date is False:
            time.sleep(2)

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

    symbol_files = ['symbols_etf.csv', 'symbols_stock.csv']
    for f in symbol_files:
        print '-----------------------', 'Updating data for symbols in', f, '-----------------------'
        symbols, names = utils.read_symbol_file(f)
        update_quotes(symbols)
        update_tech_data(symbols)
        update_analysis(symbols)

    print '-----------------------', 'Updating filter data', '-----------------------'
    update_filters()

    end_time = str(datetime.now())

    print 'Begin:', begin_time, ', End:', end_time

if __name__ == '__main__':
    main(sys.argv[1:])
