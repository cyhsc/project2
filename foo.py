import numpy as np
import pandas as pd
import os
import utils
import config
import filter

DATA_DIR = config.DATA_DIR
ANALYSIS_DIR = config.ANALYSIS_DIR

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

f = filter.Filter()
df = f.basic_trend('etf')
print df
