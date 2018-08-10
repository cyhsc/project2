import sys
import urllib2
from urllib2 import urlopen
import json
import pandas as pd
from dateutil import parser
import utils

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

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):

    sym = 'AAPL'
    iex = IEX()
    df = iex.compact_quotes(sym)

    print df

if __name__ == '__main__':
    main(sys.argv[1:])
