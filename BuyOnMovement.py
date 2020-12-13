#
# This codde trades stock on Robinhood at different thresholds as defined in buy and sell thresholds for stocks. 
#
# - Environment Variables required
# $robin_user - Username for the robinhood user
# $robin_pass - password for the robinhood user
# $robin_2FA - 2 FA code for the 2FA for the user. If no 2FA, leave blank. 
#
# In your robinhood account, create a watchlist called "Movement_Trades" that will store the stocks that you want it to trade automatically
# To change the name of the list, go to global.py
#
#

from auth import login
import utils as utils
import globals as globals
import os
from time import sleep
import robin_stocks as rs
import logging

# For purchase, only first three values are being used. Hence, last two threshold are 0 i.e. if stock price becomes 0, then only buy last two items.
buyStockUnits = [1, 2, 3, 0, 0]
buyStockDollars = [50, 100, 150, 0, 0]
buyThresholds = [0.99, 0.98, 0.95, 0, 0]

# For sell, only first two values are being used. Hence, last three threshold are 2 i.e. if stock price becomes double, then only sell last three items (which are 0).
sellStockUnits = [1, 3, 0, 0, 0]
sellStockDollars = [50, 150, 0, 0, 0]
sellThresholds = [1.02, 1.05, 2.0, 2.0, 2.0 ]

login()

#Stocks that need to be traded automatically are in the list name in globals. 
stock_list = utils.build_stocklist(globals.listName)
stockList = {}

for key in stock_list :
    for key2 in range(len(buyThresholds)):
        stockList.setdefault(key,[]).append(True)
    logging.info(f'{key:5} :{stockList[key]}')


logging.info('\nCurrent Holdings are')
utils.get_holdings()
logging.info('\nBeginning Trade Sequence')
marketOpen = True

while marketOpen == True :
    for stock_name,tradeStatus in stockList.items():
        quote = rs.stocks.get_quotes(stock_name)
        last_trade_price = float(quote[0]['last_trade_price'])
        previous_close = float(quote[0]['previous_close'])
        logging.info(f'{stock_name.rjust(5)}: Last trade price is {last_trade_price:10.3f} and previous close was {previous_close:10.3f}')
        for ctr in range(len(buyThresholds)):
            if last_trade_price/previous_close < buyThresholds[ctr] and tradeStatus[ctr] == True:
                tradeConf = utils.buy_stock_units(stock_name,buyStockUnits[ctr],last_trade_price) 
                if tradeConf == True :
                    logging.info(f'Bought {str(buyStockUnits[ctr]):3} stocks of {stock_name}\n')
                    tradeStatus[ctr] = False
                # End If
            # End if
        # End For

        for ctr in range(len(sellThresholds)):
            if last_trade_price/previous_close > sellThresholds[ctr] and tradeStatus[ctr] == True:
                tradeConf = utils.sell_stock_units(stock_name,sellStockUnits[ctr],last_trade_price) 
                if tradeConf == True :
                    logging.info(f'Sold {str(sellStockUnits[ctr]):3} stocks of {stock_name}\n')
                    tradeStatus[ctr] = False
                # End If
            # End If
        # End For
    #Wait for 5 minutes before running the script again. 
    sleep(300)
    marketOpen = utils.is_market_open()
    # End If Else
# End While