from datetime import datetime
from decimal import Decimal
import robin_stocks.robinhood as r
import pyotp
import csv
import sched
import time
import numpy as np
import pandas as pd
import statsmodels.api as sm


# defining variables
print('Defining variables .....')
s = sched.scheduler(time.time, time.sleep)
csvFilePath = 'mypython/DataCollectionBots/BitcoinData.csv'


# login to robinhood
def login():
    totp = pyotp.TOTP(apikey).now()
    r.login(username, password, mfa_code=totp)
    print('Successfully Logged In to Robinhood Collecting BTC Data .....')


# main function to collect OHLC data for BTC
def run(getData):
    global csvFilePath


    # retrieve prices use bid as the closing price
    opens = round(Decimal(r.get_crypto_quote('BTC')['open_price']), 6)
    high = round(Decimal(r.get_crypto_quote('BTC')['high_price']), 6)
    low =  round(Decimal(r.get_crypto_quote('BTC')['low_price']), 6)
    close = round(Decimal(r.get_crypto_quote('BTC')['bid_price']), 6)


    # get todays date and time including seconds
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')


    # save gathered data in a csv file
    with open(csvFilePath, 'a', newline='') as File:
        writer = csv.writer(File)
        writer.writerow([date, opens, high, low, close])
    File.close()


    # run script every 60 seconds with a 1 second wait period
    s.enter(60, 1, run, (getData,))


# run  the functions
login()
s.enter(1, 1, run, (s,))
s.run();
