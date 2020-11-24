#
# This codde trades stock on Robinhood at different thresholds as defined in buy and sell thresholds for stocks. 
#
# - Environment Variables required
# $robin_user - Username for the robinhood user
# $robin_pass - password for the robinhood user
# $robin_2FA - 2 FA code for the 2FA for the user. If no 2FA, leave blank. 
#
#
#
#

from auth import *
#from globals import *
import os
from time import sleep
#from utils import *


# For purchase, only first three values are being used. Hence, last two threshold are 0 i.e. if stock price becomes 0, then only buy last two items.
buyStockUnits = [1, 2, 3, 0, 0]
buyStockDollars = [50, 100, 150, 0, 0]
buyThresholds = [0.99, 0.98, 0.95, 0, 0]

# For sell, only first two values are being used. Hence, last three threshold are 2 i.e. if stock price becomes double, then only sell last three items (which are 0).
sellStockUnits = [1, 3, 0, 0, 0]
sellStockDollars = [50, 150, 0, 0, 0]
sellThresholds = [1.05, 1.1, 2.0, 2.0, 2.0 ]


#Stocks that need to be traded automatically. 
stock_list = ['SCHB','SPYV','SCHM','MDYV','SCHA','SLYV','VEA','SCHC','VYMI','USRT','VNQI','SPEM','GE','ABBV','INTC','XLC','IETC']
stockList = {}

for key in stock_list :
    stockList[key]=[True,True,True,True,True]
    print(key,": ", stockList[key])

login()

getHoldings()

while marketOpen == True :
    for stock_name,tradeStatus in stockList.items():
#        print(stock_name)
        quote = rs.stocks.get_quotes(stock_name)
    #    ask_price = quote.get('ask_price')
        last_trade_price = float(quote[0]['last_trade_price'])
        previous_close = float(quote[0]['previous_close'])
        print(stock_name + ': Last Trade price is ' + str(last_trade_price) + ' and previous close was ' + str(previous_close))
        
        for ctr in range(len(buyThresholds)):
            if last_trade_price/previous_close < buyThresholds[ctr] and tradeStatus[ctr] == True:
                print(f'Buy {str(buyStockUnits[ctr]):3} stocks of {stock_name}')
                tradeStatus[ctr] = buy_stock_units(stock_name,buyStockUnits[ctr],last_trade_price) 
            # end if
        # End For

        for ctr in range(len(sellThresholds)):
            if last_trade_price/previous_close > sellThresholds[ctr] and tradeStatus[ctr] == True:
                print(f'Sell {str(sellStockUnits[ctr]):3} stocks of {stock_name}')
                tradeStatus[ctr] = sell_stock_units(stock_name,sellStockUnits[ctr],last_trade_price) 
            # End If
        # End For


#Wait for 5 minutes before running the script again. 
    sleep(300)
    now = datetime.now(timeZone)
    print('Current Time is : ' + str(now))
    if now.hour < marketStart.hour or ( now.hour == marketStart.hour and now.minute < marketStart.minute ):
        # now is after market open
        marketOpen = False
    elif now.hour >= marketEnd.hour :
        marketOpen = False
    else:
        marketOpen = True
    # End If Else
# End While