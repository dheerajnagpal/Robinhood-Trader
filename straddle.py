#
# This code places trades at end of day for chosen stocks at 2% above or below the trading price to 
# utilize high volatility
#
# This is a demo strategy and not gauranteed to make money
#
# - Environment Variables required
# $robin_user - Username for the robinhood user
# $robin_pass - password for the robinhood user
# $robin_2FA - 2 FA code for the 2FA for the user. If no 2FA, leave blank. 
#
# In your robinhood account, create a watchlist called "Straddle" that will store the stocks that you want it to trade automatically
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


tradePlaced = False

tradeQuantity = 1 #Quantity of trades to be placed on each stock

#This is the robinhood watchlist for straddle strategy
straddleList = "Straddle"


while tradePlaced == False:
    extendedMarket = utils.is_extended_market()
    if extendedMarket :
        login()
        stockList = utils.build_stocklist(straddleList)
        for stock in stockList :
            quote = rs.stocks.get_quotes(stock)
            lastTradePrice = float(quote[0]['last_trade_price'])
            previousClose = float(quote[0]['previous_close'])
            buyPrice = min(lastTradePrice,previousClose) * 0.98 # Buy order at 2% below lower of current or last close price
            sellPrice = max(lastTradePrice,previousClose) * 1.02 # Sell order at 2% above higher of last trade or close

            # Caveat - Sell would work only if you have the stocks. Else, Robinhood will not place a trade on margin
            buyTrade = utils.buy_stock_units(stock,tradeQuantity,buyPrice)
            if buyTrade == True :
                logging.info(f'{tradeQuantity} units of {stock} purchased at {buyPrice}')
            # End if

            sellTrade = utils.sell_stock_units(stock,tradeQuantity,sellPrice)
            if sellTrade == True :
                logging.info(f'{tradeQuantity} units of {stock} sold at {buyPrice}')
            # End if
        # End For
        tradePlaced = True
    else :
        sleep(300)
    # End If
#End While









