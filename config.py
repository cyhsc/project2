CONFIG_DIR = '../config/'
DATA_DIR = '../data2/'
ANALYSIS_DIR = '../analysis2/'
RESULT_DIR = '../result2/'
TRADABLE_STOCKS = '../data/tradable_stocks.txt'
IBD_STOCKS = '../analysis/ibd_stocks.json'
CUR_SYM = '../data/cur_symbol.txt'
TWEETS_DIR = '../tweets/'
SCRN_NAMES = TWEETS_DIR + 'scrn_names.txt'

TWITTER_KEY = CONFIG_DIR + 'twitter_key'
ALPHA_VANTAGE_KEY = CONFIG_DIR + 'alphavantage_key'

ACCESS_TOKEN = 0
ACCESS_SECRET = 1
CONSUMER_KEY = 2
CONSUMER_SECRET = 3

MA_PERIODS = [3, 5, 7, 10, 12, 15, 30, 35, 40, 45, 50, 60, 100, 150, 200]

def get_twitter_keys(id):
    lines = open(TWITTER_KEY, 'r').read().split('\n')
    return lines[id]

def get_alphavantage_key():
    lines = open(ALPHA_VANTAGE_KEY, 'r').read().split('\n')
    return lines[0]
