#
# This code places a trade above and below the current price to scalp money out from a stock.
#
# This is a demo strategy and not gauranteed to make money. Robinhood may not be an ideal platform for Scalping as well as it doesn't allow sales unless there are stocks already present. 
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

tradeQuantity = 2 #Quantity of trades to be placed on each stock
scalpThicknessByPrice = {10: 0.005, 20: 0.003, 30: 0.002, 40: 0.001, 50: 0.001} # Set different scalp thicknesses for different prices. at $10, a thickness of 0.005 would create a spread of 10 c (+/- 5c)


#This is the robinhood watchlist for straddle strategy
straddleList = "Straddle"


while tradePlaced == False:
    marketStatus = utils.is_market_open()
    if marketStatus :
        login()
        stockList = utils.build_stocklist(straddleList)
        for stock in stockList :
            quote = rs.stocks.get_quotes(stock)
            lastTradePrice = round(float(quote[0]['last_trade_price']),2)
            scalpIndex = (int(lastTradePrice/10) + 1)*10
            if scalpIndex > 50 :
                scalpIndex = 50
            scalpThickness = scalpThicknessByPrice[scalpIndex]
            buyPrice = round(lastTradePrice * (1 - scalpThickness),2)  # Buy order at scalp% below lower of current or last close price
            sellPrice = round(lastTradePrice  * (1 + scalpThickness),2)  # Sell order at 2% above higher of last trade or close
            logging.info(f'Last Trade Price of {stock} is {lastTradePrice}')
            # Caveat - Sell would work only if you have the stocks. Else, Robinhood will not place a trade on margin
            buyTrade = utils.buy_stock_gtc(stock,tradeQuantity,buyPrice)
            if buyTrade == True :
                logging.info(f'Buy order of {tradeQuantity} units of {stock} placed at {buyPrice}')
            # End if

            sellTrade = utils.sell_stock_gtc(stock,tradeQuantity,sellPrice)
            if sellTrade == True :
                logging.info(f'Sell order of {tradeQuantity} units of {stock} placed at {sellPrice}')
            # End if
        # End For
        tradePlaced = True
    else :
        sleep(300)
    # End If
#End While









