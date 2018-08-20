import sys
import urllib2
from urllib2 import urlopen
import json
import pandas as pd
from dateutil import parser
import utils
import config

DATA_DIR = config.DATA_DIR
API_BASE = 'https://api.iextrading.com/1.0/'
API_BASE_STOCK = API_BASE + 'stock/'

class IEX:

    def __init__(self):
        pass

    def quote(self, sym):

        sym = sym.replace('-', '.')

        url = API_BASE_STOCK + sym + '/quote'
        data = utils.get_url(url)
        if data is None:
            return None, 0, 0, 0, 0, 0
        else:
            jdata = json.loads(data)
            dt = parser.parse(jdata['latestTime'])
            date = dt.strftime('%Y-%m-%d')
            return date, float(jdata['open']), float(jdata['high']), float(jdata['low']), float(jdata['close']), int(jdata['latestVolume'])

    def historical_quotes(self, sym, is_compact):

        sym = sym.replace('-', '.')
    
        qdate, qopen, qhigh, qlow, qclose, qvolume = self.quote(sym)
        if qdate is None:
            return None

        if is_compact is True:
            url = API_BASE_STOCK + sym + '/chart/3m'
        else:
            url = API_BASE_STOCK + sym + '/chart/2y'
        
        data = utils.get_url(url)
        if data is None:
            return None

        jdata = json.loads(data)
        dates = []
        open = []
        high = []
        low = []
        close = []
        volume = []
        for item in jdata:
            if 'open' not in item:
                return None
            dates.append(item['date'])
            open.append(float(item['open']))
            high.append(float(item['high']))
            low.append(float(item['low']))
            close.append(float(item['close']))
            volume.append(int(item['volume']))

        if dates[-1] < qdate:
            dates.append(qdate)
            open.append(qopen)
            high.append(qhigh)
            low.append(qlow)
            close.append(qclose)
            volume.append(qvolume)

        df = pd.DataFrame(index = dates)
        df.index.name = 'date'
        df['open'] = open
        df['high'] = high
        df['low'] = low
        df['close'] = close
        df['volume'] = volume

        return df

    def full_quotes(self, sym):
        return self.historical_quotes(sym, False)

    def compact_quotes(self, sym):
        return self.historical_quotes(sym, True)

    def batch_quotes(self, symlist):
        quotes = {}
        symbols = ''
        count = 0
        num_sym = len(symlist)
        for sym in symlist:
            symbols = symbols + sym + ','
            count = count + 1
            if count == 100:
                url = API_BASE_STOCK + 'market/batch?symbols=' + symbols + '&types=quote'    
                data = utils.get_url(url)
                jdata = json.loads(data)
                symbols = ''
                count = 0
                for key in jdata:
                    entry = jdata[key]['quote']
                    quote = [entry['open'], entry['high'], entry['low'], entry['close'], entry['latestVolume']]
                    quotes[key] = quote
    
        if symbols != '': 
            url = API_BASE_STOCK + 'market/batch?symbols=' + symbols + '&types=quote'    
            data = utils.get_url(url)
            jdata = json.loads(data)
            for key in jdata:
                entry = jdata[key]['quote']
                quote = [entry['open'], entry['high'], entry['low'], entry['close'], entry['latestVolume']]
                quotes[key] = quote

        return quotes

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):

    iex = IEX()

if __name__ == '__main__':
    main(sys.argv[1:])
