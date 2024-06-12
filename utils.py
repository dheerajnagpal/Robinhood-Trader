from time import sleep
from datetime import datetime
from globals import RASESSION, timeZone, marketEnd, marketStart, orderRetries, extMarketEnd
import robin_stocks.robinhood as rs
import logging


'''
# Updates the RASESSION header to be used by utils library. 

# @param  {String} key  -  key to udpate in the session header
# @param {string} value - corresponding value to add to key

# @return  none - Updates the session header with the key,value pair

''' 
def update_session(key, value) :

    RASESSION.headers[key] = value
# End function


'''
# Fetches the status of order from a given order url. Uses RASESSION to send the session data to Robinhood.
# If order stays unconfirmed for long, it sends a false though order may confirm after some time. This should 
# not happen in normal circumstances at robinhood but there is always a system overload

# @param  {String} url  -  url of the stock transaction

# @return  {Boolean} - If transaction completed or not

''' 
def order_status(url):

    orderInfo = RASESSION.get(url)
    orderInfo.raise_for_status()
    orderStatus = {}
    orderStatus = orderInfo.json()
    if orderStatus['state'] == 'queued' or orderStatus['state'] == 'confirmed' or orderStatus['state'] == 'filled':
        logging.info(f'Order placed for {url}')
        return True
    else :
        count = 0
        while orderStatus['state'] == "unconfirmed" and count < 5 :
            sleep(1)
            count = count + 1
            orderInfo = RASESSION.get(url)
            orderInfo.raise_for_status()
            orderStatus = orderInfo.json()
        # End of while
        if orderStatus['state'] == 'queued' or orderStatus['state'] == 'confirmed' or orderStatus['state'] == 'filled':
            logging.info(f'Order placed for {url}')
            return True
        # End of If
        logging.warning(f'Order is placed but not yet confirmed. Order may confirm later and result in multiple offers\n \
        Validate online for status. Order details are: \n {orderStatus}')
        return False
    # End of If
# End of Function


'''
# Sells the given quantity of stockname at price. It then waits for 2 seconds, and checks for the order status 
# if the order is submitted, returns true. If not submitted, or is unconfirmed, tries 5 times to submit
# There is one issue though. If the order stays unconfirmed for over 10 seconds at Robinhood, then the order gets placed
# again and may result in multiple orders if Robinhood is extremely slow on a given day. This can be controlled by changing
# orderRetries to 1 in globals.

# @param  {String} stockName  -  Stock symbol to sell
# @param  {int} quantity - number of stocks to transact.
# @param  {float} price - price at which to transact

# @return  {Boolean} - If transaction complete or not

''' 
def sell_stock_units(stockName,quantity,price):

    count = 0
    stockOrdered = False
    while stockOrdered == False and count < orderRetries :
        orderStatus = rs.order_sell_limit(stockName,quantity,price,timeInForce='gfd',extendedHours=True)
        logging.debug(f'Order Status is {orderStatus}')
        sleep(1)
        stockOrdered = order_status(orderStatus['url'])
        count = count + 1
    # End of While
    if stockOrdered == False :
        logging.info(f'Order not placed. Maximum retries reached')
    # End of If
    return stockOrdered
#End of Function




'''
# Buys the given quantity of stockname at price. It then waits for 2 seconds, and checks for the order status 
# if the order is submitted, returns true. If not submitted, or is unconfirmed, tries 5 times to submit
# There is one issue though. If the order stays unconfirmed for over 10 seconds at Robinhood, then the order gets placed
# again and may result in multiple orders if Robinhood is extremely slow on a given day. This can be controlled by changing
# orderRetries to 1 in globals.

# @param  {String} stockName  -  Stock symbol to buy
# @param  {int} quantity - number of stocks to transact.
# @param  {float} price - price at which to transact

# @return  {Boolean} - If transaction complete or not

''' 
def buy_stock_units(stockName,quantity,price):
    count = 0
    stockOrdered = False
    while stockOrdered == False and count < orderRetries :
        #orderStatus = rs.order_buy_limit(symbol=stockName,quantity=quantity,limitPrice=price,timeInForce='gfd',extendedHours=True) Broken due to a bug
        orderStatus = rs.order_buy_market(stockName,quantity,timeInForce="gfd",extendedHours="False")
        logging.debug(f'Order Status is {orderStatus}')
        sleep(2)
        stockOrdered = order_status(orderStatus['url'])
        count = count + 1
    # End of While
    if stockOrdered == False :
        logging.info(f'Order not placed. Maximum retries reached')
    # End of If
    return stockOrdered
#End of Function



'''
# Buys the given dollars of stockname. This buys fractional stocks. It then waits for 2 seconds, and checks for the order status 
# if the order is submitted, returns true. If not submitted, or is unconfirmed, tries 5 times to submit
# There is one issue though. If the order stays unconfirmed for over 10 seconds at Robinhood, then the order gets placed
# again and may result in multiple orders if Robinhood is extremely slow on a given day. This can be controlled by changing
# orderRetries to 1 in globals.

# @param  {String} stockName  -  Stock symbol to buy
# @param  {int} quantity - Dollar value of stock to buy

# @return  {Boolean} - If transaction complete or not

'''     
def buy_stock_fractional(stockName,quantity):
    count = 0
    stockOrdered = False
    while stockOrdered == False and count < orderRetries :
        orderStatus = rs.order_buy_fractional_by_price(stockName,quantity,timeInForce='gfd',priceType='bid_price')
        logging.debug(f'Order Status is {orderStatus}')
        sleep(2)
        stockOrdered = order_status(orderStatus['url'])
        count = count + 1
    # End of While
    if stockOrdered == False :
        logging.info(f'Order not placed. Maximum retries reached')
    # End of If
    return stockOrdered
#End of Function



'''
# Sells the given dollars of stockname. This sells fractional stocks. It then waits for 2 seconds, and checks for the order status 
# if the order is submitted, returns true. If not submitted, or is unconfirmed, tries 5 times to submit
# There is one issue though. If the order stays unconfirmed for over 10 seconds at Robinhood, then the order gets placed
# again and may result in multiple orders if Robinhood is extremely slow on a given day. This can be controlled by changing
# orderRetries to 1 in globals.

# @param  {String} stockName  -  Stock symbol to sell
# @param  {int} quantity - Dollar value of stock to sell.

# @return  {Boolean} - If transaction complete or not

''' 
def sell_stock_fractional(stockName,quantity):
    count = 0
    stockOrdered = False
    while stockOrdered == False and count < orderRetries :
        orderStatus = rs.order_sell_fractional_by_price(stockName,quantity,timeInForce='gfd',priceType='ask_price')
        logging.debug(f'Order Status is {orderStatus}')
        sleep(2)
        stockOrdered = order_status(orderStatus['url'])
        count = count + 1
    # End of While
    if stockOrdered == False :
        logging.info(f'Order not placed. Maximum retries reached')
    # End of If
    return stockOrdered
#End of Function


'''
# lists the current holdings of the stocks. 
# TODO - Return the current holdings value

'''  
def get_holdings():
    holdings = rs.build_holdings()
    holdingValues = {}
    logging.info(f' Stock        Quantity')
    for key,value in holdings.items():
        logging.info(f' {key:5}:  {value["quantity"].rjust(13)}')
        holdingValues.setdefault(key,[]).append(value['quantity'])
    return holdingValues
    #End For
# End Function


'''
# returns if market is open or not

# @return  {Boolean} - If market is open or not

'''  
def is_market_open():
 
    now = datetime.now(timeZone)
    logging.info(f'Current time is : {now}\n')
    if now.hour < marketStart.hour or (now.hour == marketStart.hour and now.minute < marketStart.minute):
        # now is before market open
        return False
    elif now.hour >= marketEnd.hour :
        # now is after market close
        return False
    else:
        # market is open
        return True
    #end If Else
# End Fuction


'''
# returns if market is in extended market or not

# @return  {Boolean} - If market is in extended market. It returns false if Market is open in regular time

'''  
def is_extended_market():
 
    now = datetime.now(timeZone)
    logging.info(f'Current time is : {now}\n')
    if (now.hour == marketStart.hour and now.minute < marketStart.minute):
        # now is extended market before market open
        return True
    elif now.hour >= marketEnd.hour and now.hour < extMarketEnd.hour :
        # now is extended market after market close
        return True
    else:
        # market is not in extended zone
        return False
    #end If Else
# End Fuction



'''
# returns the list of stocks in a given watchlist as a list.

# @param {string} listname - Name of watchlist to fetch stocks from. 
# @return  {list} - list of symbols in the watchlist

''' 
def build_stocklist(listName) :

    stockListItems = rs.get_watchlist_by_name(listName)
    stockList = []
    for item in stockListItems['results'] :
        stockList.append(item['symbol'])
    # End For
    logging.debug(f'The stock list items are :\n {stockList}')
    return stockList
# End Function
 

 
'''
# Sells the given quantity of stockname at price and sets a good till cancel order. 
# 
# 
#   
# @param  {String} stockName  -  Stock symbol to sell
# @param  {int} quantity - number of stocks to transact.
# @param  {float} price - price at which to transact

# @return  {Boolean} - If transaction complete or not

''' 
def sell_stock_gtc(stockName,quantity,price):

    count = 0
    stockOrdered = False
    while stockOrdered == False and count < orderRetries :
        orderStatus = rs.order_sell_limit(stockName,quantity,price,timeInForce='gtc',extendedHours=True)
        logging.debug(f'Order Status is {orderStatus}')
        sleep(1)
        stockOrdered = order_status(orderStatus['url'])
        count = count + 1
    # End of While
    if stockOrdered == False :
        logging.info(f'Order not placed. Maximum retries reached')
    # End of If
    return stockOrdered
#End of Function




'''
# Buys the given quantity of stockname at price and sets a good till cancel order. 
# 
# 
# 
# 

# @param  {String} stockName  -  Stock symbol to buy
# @param  {int} quantity - number of stocks to transact.
# @param  {float} price - price at which to transact

# @return  {Boolean} - If transaction complete or not

''' 
def buy_stock_gtc(stockName,quantity,price):
    count = 0
    stockOrdered = False
    while stockOrdered == False and count < orderRetries :
        orderStatus = rs.order_buy_limit(stockName,quantity,price,timeInForce='gtc',extendedHours=True)
        logging.debug(f'Order Status is {orderStatus}')
        sleep(1)
        stockOrdered = order_status(orderStatus['url'])
        count = count + 1
    # End of While
    if stockOrdered == False :
        logging.info(f'Order not placed. Maximum retries reached')
    # End of If
    return stockOrdered
#End of Function