import sys
import pandas as pd
import numpy as np
import config
import utils

RESULT_DIR = config.RESULT_DIR

class Filter:

    def __init__(self):
        pass

    def basic_trend(self, type): 

        if type == 'etf': 
            symbol_file = 'symbols_etf.csv'
        elif type == 'stock':
            symbol_file = 'symbols_stock.csv'
        else:
            print 'Enter valid type, etf or stock'
            return
 
        symbols, names = utils.read_symbol_file(symbol_file)
      
        slow_align_total = []
        fast_align_total = []
        slow_roc_total = []
        fast_roc_total = []
        swidth_pb = []
        fwidth_pb = []
        rwb = []        
        macd_hist_pb = []
        swidth_roc_pb = []
        fwidth_roc_pb = []
        diff_slow_kd_pb = []
        slowk = []
        slowd = []
     
        for sym in symbols: 
            df = utils.read_analysis_file(sym)
            if df is None:
                print 'Analysis file for', sym, ' doesnot exist'
                continue

            slow_align_total.append(df['slow_align_total'][-1])
            slow_roc_total.append(df['slow_roc_total'][-1])
            fast_align_total.append(df['fast_align_total'][-1])
            fast_roc_total.append(df['fast_roc_total'][-1])
            swidth_pb.append(df['swidth_pb'][-1])
            fwidth_pb.append(df['fwidth_pb'][-1])
            rwb.append(df['rwb'][-1])
            macd_hist_pb.append(df['macd_hist_pb'][-1])
            swidth_roc_pb.append(df['swidth_roc_pb'][-1])
            fwidth_roc_pb.append(df['fwidth_roc_pb'][-1])
            diff_slow_kd_pb.append(df['diff_slow_kd_pb'][-1])
            slowk.append(df['slowk'][-1])
            slowd.append(df['slowd'][-1])

        align_total_df = pd.DataFrame(index = symbols)
        align_total_df['name'] = names
        align_total_df['slow_align_total'] = slow_align_total
        align_total_df['slow_roc_total'] = slow_roc_total
        align_total_df['fast_align_total'] = fast_align_total
        align_total_df['fast_roc_total'] = fast_roc_total
        align_total_df['rwb'] = rwb
        align_total_df['swidth_pb'] = swidth_pb
        align_total_df['fwidth_pb'] = fwidth_pb
        align_total_df['macd_hist_pb'] = macd_hist_pb
        align_total_df['swidth_roc_pb'] = swidth_roc_pb 
        align_total_df['fwidth_roc_pb'] = fwidth_roc_pb 
        align_total_df['diff_slow_kd_pb'] = diff_slow_kd_pb
        align_total_df['slowk'] = slowk
        align_total_df['slowd'] = slowd
    
        ret_df = align_total_df.sort_values(['slow_align_total', 'slow_roc_total', 'fast_align_total', 'fast_roc_total', 'swidth_pb'], ascending=[False, False, False, False, False])

        ret_df.to_csv(RESULT_DIR + 'basic_trend_' + type + '.csv')

        return ret_df

    def obsolete(self): 

        df = utils.read_analysis_file('spy')
        date = df.index[-1]

        etf_symbols, names = utils.read_symbol_file('symbols_etf.csv')
        stock_symbols, names = utils.read_symbol_file('symbols_stock.csv')
        combined_symbols = etf_symbols + stock_symbols
        obsolete_symbols = []

        for sym in combined_symbols:
            df = utils.read_analysis_file(sym)
            if df is None:
                print 'Analysis file for', sym, ' doesnot exist'
                continue
            
            if df.index[-1] < date: 
                print sym, 'is obsolete'
                obsolete_symbols.append(sym)

        print '------------------- Obsoleted Symbols -----------------------'
        print obsolete_symbols
        
    def three_percent(self, type): 

        if type == 'etf':
            symbol_file = 'symbols_etf.csv'
        elif type == 'stock':
            symbol_file = 'symbols_stock.csv'
        else:
            print 'Enter valid type, etf or stock'
            return

        symbols, names = utils.read_symbol_file(symbol_file)

        tp_symbols = []
        tp_changes = []
        tp_vchanges = []

        for sym in symbols:
            df = utils.read_analysis_file(sym)
            if df is None:
                print 'Analysis file for', sym, ' doesnot exist'
                continue

            closes = df['close']
            if len(closes) < 2:
                continue

            volumes = df['volume']
            vol_sma50 = df['vol_sma50']
            change = (100*(float(closes[-1]) - float(closes[-2])))/float(closes[-2])
            vchange = (100*(float(volumes[-1]) - float(vol_sma50[-1])))/float(vol_sma50[-1])
            swidth = df['swidth']
            sband_max = df['sband_max']
            if (change >= 3) and (vchange >= 150) and (swidth[-1] > 0) and (closes[-1] > sband_max[-1]): 
                tp_symbols.append(sym)
                tp_changes.append(change)
                tp_vchanges.append(vchange)

        tp_df = pd.DataFrame(index = tp_symbols)
        tp_df['change'] = tp_changes
        tp_df['volume_change'] = tp_vchanges

        tp_df.to_csv(RESULT_DIR + 'three_percent_' + type + '.csv')

        return tp_df

    def three_percent_track(self, type): 
        
        #--------------------------------------------------------------------------------
        # Read in new three percent stocks
        #--------------------------------------------------------------------------------
        lines = open(RESULT_DIR + 'three_percent_' + type + '.csv').read().split('\n')
        new_three_percent = []
        for line in lines[1:]:
            if len(line) > 0: 
                new_three_percent.append(line.split(',')[0])
                
        #--------------------------------------------------------------------------------
        # Read in three percent tracker 
        #--------------------------------------------------------------------------------
        lines = open(RESULT_DIR + 'three_percent_tracker.csv').read().split('\n')
        track = {}
        for line in lines:
            if len(line) > 0:
                items = line.split(',')
                sym = items[0]
                dates = []
                for item in items[1:]:
                    dates.append(item)
                track[sym] = dates

        #--------------------------------------------------------------------------------
        # Add new stocks to tracker 
        #--------------------------------------------------------------------------------
        for sym in new_three_percent: 
            df = utils.read_analysis_file(sym)
            latest_date = df.index[-1]
            if sym not in track:
                track[sym] = [latest_date]
            else:
                dates = track[sym]
                if latest_date not in dates:
                    dates.append(latest_date)

        #--------------------------------------------------------------------------------
        # Write back to track file
        #--------------------------------------------------------------------------------
        f = open(RESULT_DIR + 'three_percent_tracker.csv', 'w')
        for key in track:
            line = key
            for item in track[key]:
                line = line + ',' + item
            print line
            f.write(line + '\n')
        f.close()

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):

    f = Filter()
    f.three_percent('stock')

if __name__ == '__main__':
    main(sys.argv[1:])
