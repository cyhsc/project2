import os
import pandas as pd
import numpy as np
from time import gmtime, strftime
from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen
import datetime
import config

DATA_DIR = config.DATA_DIR
ANALYSIS_DIR = config.ANALYSIS_DIR

##############################################################################################
#
#    Time and Date related functions
#
##############################################################################################

# ----------------------------------------------------------------
#            Get current date and time
# Directive     Meaning
# %a    Weekday name.
# %A    Full weekday name.
# %b    Abbreviated month name.
# %B    Full month name.
# %c    Appropriate date and time representation.
# %d    Day of the month as a decimal number [01,31].
# %H    Hour (24-hour clock) as a decimal number [00,23].
# %I    Hour (12-hour clock) as a decimal number [01,12].
# %j    Day of the year as a decimal number [001,366].
# %m    Month as a decimal number [01,12].
# %M    Minute as a decimal number [00,59].
# %p    Equivalent of either AM or PM.
# %S    Second as a decimal number [00,61].
# %U    Week number of the year (Sunday as the first day of the week) as a decimal number [00,53].
#       All days in a new year preceding the first Sunday are considered to be in week 0.
# %w    Weekday as a decimal number [0(Sunday),6].
# %W    Week number of the year (Monday as the first day of the week) as a decimal number [00,53].
#       All days in a new year preceding the first Monday are considered to be in week 0.
# %x    Appropriate date representation.
# %X    Apropriate time representation.
# %y    Year without century as a decimal number [00,99].
# %Y    Year with century as a decimal number.
# %Z    Time zone name (no characters if no time zone exists).
# %%    A literal '%' character.
# ----------------------------------------------------------------
def current_date_time_str():
    return strftime("%Y-%m-%d %H:%M:%S")

def current_date():
    return strftime("%Y"), strftime("%m"), strftime("%d")

def current_time():
    return strftime("%H"), strftime("%M"), strftime("%S")

def current_weekday():
    return strftime("%A")

def current_date_str():
    return datetime.date.today().strftime('%Y-%m-%d')

def previous_date_str(n):
    return (datetime.date.today() - datetime.timedelta(n)).strftime('%Y-%m-%d')

##############################################################################################
#
#    File Handling functions
#
##############################################################################################

# ---------------------------------------------------
#   Read symbols file
#   Return: an array of symbols
# ---------------------------------------------------
def read_symbol_file(file_name):
    symbols = []
    names = []
    symbol_file = config.CONFIG_DIR + file_name
    print symbol_file
    lines = open(symbol_file, 'r').read().split('\n')
    for line in lines:
        # Skip empty lines
        if len(line) == 0:
            continue

        # Skip comment lines
        if line[0] == '#':
            continue

        #for item in line.split(','):
        #    symbols.append(item)
        symbols.append(line.split(',')[0])
        names.append(line.split(',')[1])

    return symbols, names

# -----------------------------------------------------------------------------------
#   Read quote file
#   Return: dataframe of csv file, None if file doesn't exist
# -----------------------------------------------------------------------------------
def read_quote_file(sym):
    if os.path.isfile(DATA_DIR + sym + '.csv'):
        print 'Quote file for', sym, 'exists, read it in'
        df = pd.read_csv(DATA_DIR + sym + '.csv', index_col = 0)
        return df
    else:
        print 'Quote file for', sym, 'donot exist, bail'
        return None

# -----------------------------------------------------------------------------------
#   Read analysis file
#   Return: dataframe of csv file, None if file doesn't exist
# -----------------------------------------------------------------------------------
def read_analysis_file(sym):
    if os.path.isfile(ANALYSIS_DIR + sym + '_analysis.csv'):
        print 'Analysis file for', sym, 'exists, read it in'
        df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)
        return df
    else:
        print 'Analysis file for', sym, 'donot exist, bail'
        return None


##############################################################################################
#
#    Calulation functions
#
##############################################################################################

# ---------------------------------------------------
#   Calculate rate of change
#   Return: an array of rate of change
# ---------------------------------------------------
def roc(data_series):
    r = []
    for index, elem in enumerate(data_series):
        if index == 0:
            r.append(float('NaN'))
        else:
            r.append(elem - data_series[index - 1])
    return r

# ---------------------------------------------------
# Calculate min/max of a data series
# Return: min, max
# ---------------------------------------------------
def minmax(data_series, ignore_nan = 0):
    initialized = 0
    min = float('NaN')
    max = float('NaN')
    for index, elem in enumerate(data_series):
        if np.isnan(elem) == False:
            if initialized == 1:
                if elem < min:
                    min = elem
                if elem > max:
                    max = elem
            else:
                initialized = 1
                min = elem
                max = elem
        else:
            if ignore_nan == 0:
                min = float('NaN')
                max = float('NaN')
                break

    return min, max

# ---------------------------------------------------
#   Calculate number of consecutive positive bars
#   Return: an array of positive bars count
# ---------------------------------------------------
def positive_bars(data_series, nonneg = True):
    r = []
    bars = 0
    for index, elem in enumerate(data_series):
        if np.isnan(elem) == True:
            bars = 0
        elif elem < 0:
            if bars < 0:
                bars = bars - 1
            else:
                bars = -1
        elif elem == 0:
            if nonneg == True:
                if bars >= 0:
                    bars = bars + 1
                else:
                    bars = 1
            else:
                bars = 0
        else:
            if bars >= 0:
                bars = bars + 1
            else:
                bars = 1

        r.append(bars)

    return r

# ----------------------------------------------------------------------
#   Calculate relative ranking of each member with a data series
#   Return: an array of relative ranking from -100 to 100
# ----------------------------------------------------------------------
def relative_rank(data_series):
    max = data_series.max()
    min = data_series.min()
    ranking = []
    data_list = data_series.tolist()
    for i in data_list:
        if i >= 0:
            ranking.append((i/max)*100)
        else:
            ranking.append(-(i/min)*100)

    return ranking

##############################################################################################
#
# Internet fectching related functions 
#
##############################################################################################
def get_url_soup(url):
    try:
        #print url
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        req = urllib2.Request(url, '', headers)
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html, "lxml")
        return soup

    except urllib2.URLError as e:
        print 'Failed to open', url, 'because of', e.reason
        return None

def get_url_soup_no_user_agent(url):
    try:
        #print url
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        return soup

    except urllib2.URLError as e:
        print 'Failed to open', url, 'because of', e.reason
        return None

##############################################################################################
#
# Misc
#
##############################################################################################

#-----------------------------------------------------------------------------------
# Convert "[1, 2, 3]" to [1, 2, 3]
#-----------------------------------------------------------------------------------
def list_string_to_list(line):
    list = line.lstrip('[').rstrip(']').split(',')
    return list
