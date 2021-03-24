
import numpy as np
import pandas as pd
import statsmodels.api as sm
from decimal import Decimal
import robin_stocks.robinhood as r
import pyotp
import sched
import time
from secret import username, password, apikey

# defining variables
s = sched.scheduler(time.time, time.sleep)
TICKER = 'ETH'
enteredTrade = False
betAmount = 20


# login to robinhood
def login():
    totp = pyotp.TOTP(apikey).now()
    r.login(username, password, mfa_code=totp)
    print('Successfully Logged In to Robinhood')


def run(zscores):
    # defining global variables

    global betAmount
    global enteredTrade
    global TICKER

    def coinSwitch(TICKER):
        if (TICKER == 'BCH'):
            return 0
        elif TICKER == 'ETC':
            return 1
        elif TICKER == 'LTC':
            return 2
        elif TICKER == 'DOGE':
            return 3
        elif TICKER == 'ETH':
            return 4
        elif TICKER == 'BTC':
            return 5
        elif TICKER == 'USD':
            return 6
        else:
            return 5

    csvFilePath = '/Users/carlos/Documents/Python/Robinhood/mypython/Coin Data/ETH-Spreads.csv'
    moneyInAccount = round(Decimal(r.profiles.load_account_profile('crypto_buying_power')), 2)
    currentPriceOfCrypto = round(Decimal(r.get_crypto_quote(TICKER)['bid_price']), 2)
    quantityOfCoins = round(Decimal(r.get_crypto_positions('quantity')[coinSwitch(TICKER)]), 8)

    # start all the calculations for the z score number
    data = pd.read_csv(csvFilePath, index_col ='Date')
    data['ratio'] = data['Bid']/data['Ask']

    S1 = data['Bid']
    S2 = data['Ask']

    S1 = sm.add_constant(S1)
    results = sm.OLS(S2, S1).fit()
    S1 = S1['Bid']
    b = results.params['Bid']
    spread = S2 - b * S1
    spread.plot()

    def zscore(series):
        return (series - series.mean()) / np.std(series)

    zscore = zscore(spread)[-1]
    # end of all the zscore calculations
    # Execution of trades buying and selling
    if(zscore <= -1.5 and not enteredTrade and moneyInAccount > 5):
        print('the current z_score is below -1 going long : ' + TICKER)
        r.orders.order_buy_crypto_by_price(TICKER, float(betAmount))
        print('With a z_score of : ' + str(zscore)+ " you bought $ " + str(betAmount)+ " worth of "+ TICKER)
        enteredTrade = True
# selling conditions
    if(zscore >= 1.5 and enteredTrade):
        print('the z_score rose above 1 selling the position in : '+ TICKER)
        r.order_sell_crypto_limit(TICKER, float(quantityOfCoins), float(currentPriceOfCrypto))
        print('z_score is : '+ str(zscore)+ " sold your " + TICKER + " position")
        enteredTrade = False
    else:
        if(zscore >= 1.5):
            print('the z_score is above 1 selling your position in : '+ TICKER)
            r.order_sell_crypto_limit(TICKER, float(quantityOfCoins), float(currentPriceOfCrypto))
            print('z_score is : '+ str(zscore)+ " sold your " + TICKER + " position")
            enteredTrade = False

    s.enter(1800, 1, run, (zscores,))


login()
s.enter(1, 1, run, (s,))
s.run()
