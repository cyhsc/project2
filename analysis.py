import os
import pandas as pd
import numpy as np
import config
import utils

ANALYSIS_DIR = config.ANALYSIS_DIR

##############################################################################################
#
# This class will perform analysis 
#
##############################################################################################

class Analysis:

    def __init__(self):
        pass

    #---------------------------------------------------------------------
    # Calculate the Guppy ribbon alignment score
    #---------------------------------------------------------------------
    def alignment_score(self, ma_array): 
        # Assume ma_array is aranged with increasing moving average period
        # ma_array[0] .... ma_array[5]

        scores = []
        total = 0

        for i in xrange(1, len(ma_array)):
            score = 0
            for j in xrange(0, i):
                if ma_array[i] <= ma_array[j]:
                    score = score + 1
            scores.append(score)
            total = total + score
            
        return scores, total
        

    def guppy_alignment(self, df):
        fast_align = []
        fast_align_total = []
        slow_align = []
        slow_align_total = []
        for index, row in df.iterrows():
            fast = [row['ema3'], row['ema5'], row['ema7'], row['ema10'], row['ema12'], row['ema15']]
            slow = [row['ema30'], row['ema35'], row['ema40'], row['ema45'], row['ema50'], row['ema60']]
            fast_scores, fast_total = self.alignment_score(fast)
            fast_align.append(fast_scores)
            fast_align_total.append(fast_total)
            slow_scores, slow_total = self.alignment_score(slow)
            slow_align.append(slow_scores)
            slow_align_total.append(slow_total)

        df['fast_align'] = fast_align
        df['fast_align_total'] = fast_align_total
        df['slow_align'] = slow_align
        df['slow_align_total'] = slow_align_total

    def roc_score(self, roc_array):  
        scores = []
        total = 0
        for i in xrange(0, len(roc_array)):
            if roc_array[i] > 0:
                scores.append(2**i)
                total = total + (2**i)
            else: 
                scores.append(0)
        
        return scores, total

    def guppy_roc(self, df):
        fast_roc = []
        fast_roc_total = []
        slow_roc = []
        slow_roc_total = []
        for index, row in df.iterrows():
            fast = [row['ema3_roc'], row['ema5_roc'], row['ema7_roc'], row['ema10_roc'], row['ema12_roc'], row['ema15_roc']]
            slow = [row['ema30_roc'], row['ema35_roc'], row['ema40_roc'], row['ema45_roc'], row['ema50_roc'], row['ema60_roc']]
            fast_scores, fast_total = self.roc_score(fast)
            slow_scores, slow_total = self.roc_score(slow)
            fast_roc.append(fast_scores)
            fast_roc_total.append(fast_total)
            slow_roc.append(slow_scores)
            slow_roc_total.append(slow_total)

        df['fast_roc'] = fast_roc
        df['fast_roc_total'] = fast_roc_total
        df['slow_roc'] = slow_roc
        df['slow_roc_total'] = slow_roc_total

    def update(self, sym):
        print 'Updating analysis analysis for', sym, '.....'
        df = utils.read_analysis_file(sym)
        if df is None:
            return

        self.guppy_alignment(df)
        self.guppy_roc(df)

        df.to_csv(ANALYSIS_DIR + sym + '_analysis' + '.csv')
