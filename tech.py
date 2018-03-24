import os
import sys
import numpy as np
import pandas as pd
import talib
import math
import config
import utils

DATA_DIR = config.DATA_DIR
ANALYSIS_DIR = config.ANALYSIS_DIR

ma_periods = config.MA_PERIODS

class TechData:

    def __init__(self, ref_sym = 'spy'):
        self.ref_sym = ref_sym

    #-------------------------------------------------------------------
    #   Calculate Moving Averages
    #   - data: Pandas dataframe object containing quotes
    #   - period: moving average period such as 50, 200, etc.
    #-------------------------------------------------------------------
    def sma(self, data, period):
        np_closes = np.array(data['close'], dtype=float)
        data['sma' + str(period)] = talib.SMA(np_closes, timeperiod=period).tolist()

    #-------------------------------------------------------------------
    #   Calculate Moving Averages
    #   - data: Pandas dataframe object containing quotes
    #   - period: moving average period such as 50, 200, etc.
    #-------------------------------------------------------------------
    def ema(self, data, period):
        np_closes = np.array(data['close'], dtype=float)
        data['ema' + str(period)] = talib.EMA(np_closes, timeperiod=period).tolist()

    #-------------------------------------------------------------------
    #   Calculate MACD
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def macd(self, data):
        np_closes = np.array(data['close'], dtype=float)
        macd, macd_sig, macd_hist = talib.MACD(np_closes)
        data['macd'] = macd.tolist()
        data['macd_sig'] = macd_sig.tolist()
        data['macd_hist'] = macd_hist.tolist()

        data['macd_roc'] = utils.roc(data['macd'])
        data['macd_roc_pb'] = utils.positive_bars(data['macd_roc'])
        data['macd_sig_roc'] = utils.roc(data['macd_sig'])
        data['macd_sig_roc_pb'] = utils.positive_bars(data['macd_sig_roc'])
        data['macd_hist_roc'] = utils.roc(data['macd_hist'])
        data['macd_hist_pb'] = utils.positive_bars(data['macd_hist'])
        data['macd_hist_roc_pb'] = utils.positive_bars(data['macd_hist_roc'])

    #-------------------------------------------------------------------
    #   Calculate Moving Averages
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def ma(self, data):
        np_closes = np.array(data['close'], dtype=float)
        for period in ma_periods:
            data['ema' + str(period)] = talib.EMA(np_closes, timeperiod=period).tolist()
            data['ema' + str(period) + '_roc'] = utils.roc(data['ema' + str(period)])

    # ---------------------------------------------------
    # Perform analysis of Guppy
    # - Data: dataframe containing quote and tech info
    # ---------------------------------------------------
    def guppy(self, data):

        fwidth = []
        swidth = []
        rwb = []

        for index, row in data.iterrows():
            fast = [row['ema3'], row['ema5'], row['ema7'], row['ema10'], row['ema12'], row['ema15']]
            slow = [row['ema30'], row['ema35'], row['ema40'], row['ema45'], row['ema50'], row['ema60']]
            fmin, fmax = utils.minmax(fast)
            smin, smax = utils.minmax(slow)

            if row['ema3'] > row['ema15']:
                fwidth.append(fmax - fmin)
            else:
                fwidth.append(fmin - fmax)

            if row['ema30'] > row['ema60']:
                swidth.append(smax - smin)
            else:
                swidth.append(smin - smax)

            if fmin > smax:
                rwb.append(fmin - smax)
            elif smin > fmax:
                rwb.append(fmax - smin)
            else:
                rwb.append(0.0)

        data['fwidth'] = fwidth
        data['fwidth_pb'] = utils.positive_bars(data['fwidth'])
        data['fwidth_roc'] = utils.roc(fwidth)
        data['fwidth_roc_pb'] = utils.positive_bars(data['fwidth_roc'])
        data['fwidth_ranking'] = utils.relative_rank(data['fwidth'])
        data['swidth'] = swidth
        data['swidth_pb'] = utils.positive_bars(data['swidth'])
        data['swidth_roc'] = utils.roc(swidth)
        data['swidth_roc_pb'] = utils.positive_bars(data['swidth_roc'])
        data['swidth_ranking'] = utils.relative_rank(data['swidth'])
        data['rwb'] = rwb
        data['rwb_pb'] = utils.positive_bars(data['rwb'])
        data['rwb_roc'] = utils.roc(rwb)
        data['rwb_roc_pb'] = utils.positive_bars(data['rwb_roc'])
        data['rwb_ranking'] = utils.relative_rank(data['rwb'])

    #-------------------------------------------------------------------
    #   Calculate Volume Moving Averages
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def volume(self, data):
        np_volumes = np.array(data['volume'], dtype=float)
        data['vol_sma50'] = talib.SMA(np_volumes, timeperiod=50).tolist()

    #-------------------------------------------------------------------
    #   Calculate Relative Performance
    #   - data: Pandas dataframe object containing quotes
    #   - base_data: Pandas dataframe object containing quotes for base symbol
    #
    #   Assuming base_data contains more bars than data
    #-------------------------------------------------------------------
    def relative(self, data, base_data):
        closes = data['close']
        r_closes = closes[::-1]
        base_closes = base_data['close']
        r_base_closes = base_closes[::-1]

        len_closes = len(closes)
        len_base_closes = len(base_closes)
        min_len = min(len_closes, len_base_closes)
 
        rel = []
        for index in xrange(min_len):
            rel.insert(0, (r_closes[index]/r_base_closes[index]))

        data['rel'] = rel
        np_rel = np.array(rel, dtype=float)
        data['rel_ema30'] = talib.EMA(np_rel, timeperiod=30).tolist()

    #-------------------------------------------------------------------
    #   Calculate ATR
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def atr(self, data):
        np_close = np.array(data['close'], dtype=float)
        np_high= np.array(data['high'], dtype=float)
        np_low= np.array(data['low'], dtype=float)
        data['atr'] = talib.ATR(np_high, np_low, np_close, timeperiod=14)

    #-------------------------------------------------------------------
    #   Calculate Stochastic chart
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def stochastic(self, data):
        np_close = np.array(data['close'], dtype=float)
        np_high= np.array(data['high'], dtype=float)
        np_low= np.array(data['low'], dtype=float)
        slowk, slowd = talib.STOCH(np_high, np_low, np_close, fastk_period=14, slowk_period=3)
        data['slowk'] = slowk
        data['slowd'] = slowd
        data['slowk_roc'] = utils.roc(data['slowk'])
        data['slowd_roc'] = utils.roc(data['slowd'])

    #-------------------------------------------------------------------
    #   Calculate Renko chart
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def renko(self, data):
        closes = data['close']
        closes_list = closes.tolist()
        renko_df = closes.to_frame()
        atr = data['atr'].tolist()[-1]
        renko_bars = [None] * len(closes_list)

        if np.isnan(atr) == False:

            for index, elem in enumerate(closes_list):
                if index == 0: 
                    high = closes_list[index]
                    low = closes_list[index]
                    renko_bars[index] = 'Base,' + str(high) + ',' + str(low)
                elif (closes_list[index] < (high + atr)) and (closes_list[index] > (low - atr)):
                    renko_bars[index] = '<'
                else: 
                    #-------------------------------------------------
                    # We need to draw some bars 
                    #-------------------------------------------------
                    if high == low:  
                        #-------------------------------------------------
                        # Drawing first bar
                        #-------------------------------------------------
                        if (closes_list[index] >= (high + atr)):
                            bars = int((closes_list[index] - high)/atr)
                            high = high + atr*bars
                            low = low + atr*(bars - 1)
                            renko_bars[index] = 'W,' + str(bars) + ',' + str(high) + ',' + str(low)
                        else:
                            bars = int((low - closes_list[index])/atr)
                            high = high - atr*(bars - 1)
                            low = low - atr*bars
                            renko_bars[index] = 'B,' + str(bars) + ',' + str(high) + ',' + str(low)
                    else:
                        #-------------------------------------------------
                        # Drawing subsequent bars 
                        #-------------------------------------------------
                        if (closes_list[index] >= (high + atr)):
                            bars = int((closes_list[index] - high)/atr)
                            high = high + atr*bars
                            low = low + atr*bars
                            renko_bars[index] = 'W,' + str(bars) + ',' + str(high) + ',' + str(low)
                        else:
                            bars = int((low - closes_list[index])/atr)
                            high = high - atr*bars
                            low = low - atr*bars
                            renko_bars[index] = 'B,' + str(bars) + ',' + str(high) + ',' + str(low)


        renko_df['renko'] = renko_bars
        data['renko'] = renko_bars
   
    def update(self, sym):
        print 'Updating technical analysis for', sym, '.....'
        df = utils.read_quote_file(sym)
        if df is None: 
            return 
       
        self.volume(df)
        self.macd(df)
        self.ma(df)
        self.guppy(df)
        self.atr(df)
        self.renko(df)
        self.stochastic(df)

        if (self.ref_sym is not None) and (self.ref_sym != sym.lower()): 
            if os.path.isfile(DATA_DIR + self.ref_sym + '.csv'):
                ref_df = pd.read_csv(DATA_DIR + self.ref_sym + '.csv', index_col = 0)
                self.relative(df, ref_df)
            else:
                print 'No data for', self.ref_sym, ', no relative calculation'
        else:
            print 'Ref sym =', self.ref_sym, ', no relative calculation'

        #-------------------------------------------------
        # Save the data to file 
        #-------------------------------------------------

        df.to_csv(ANALYSIS_DIR + sym + '_analysis' + '.csv')

        return 

