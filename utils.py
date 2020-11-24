from time import sleep
from globals import *
import robin_stocks as rs


def update_session(key, value):
    """Updates the RASESSION header used by the requests library.
    :param key: The key value to update or add to session header.
    :type key: str
    :param value: The value that corresponds to the key.
    :type value: str
    :returns: None. Updates the session header with a value.
    """
    RASESSION.headers[key] = value



# Sell the quantity worth of dollars of stockName
def sell_stock_units(stockName,quantity,price):
    """Sell the requested quantity of stockName
    :param stockName: The stock to sell.
    :type stockName: str
    :param quantity: number of units of stockName to sell. Will not sell anything if more units are being sold than in acount. 
    :type quantity: int
    :param price: Price at which to sell the stocks
    :type price: float
    :returns: Boolean. True or false depending on if stock sold. Sells the stock and outputs the status. Robinhood has in built-in checks to not sell if you don't own a stock 
    """    
    orderAwaiting = True
    count = 0
    orderInfo = {}
    while orderAwaiting and count < 5 :
#        orderStatus = rs.order_sell_fractional_by_price(stockName,quantity,timeInForce='gfd',priceType='ask_price')
        orderStatus = rs.order_sell_limit(stockName,quantity,price,timeInForce='gfd',extendedHours=True)
        print(orderStatus)
        sleep(2)
        orderStatus = RASESSION.get(orderStatus['url'])
        orderStatus.raise_for_status()
        orderInfo = orderStatus.json()
        count = count + 1
        if orderInfo['state'] == 'queued' or orderInfo['state'] == 'confirmed':
            orderAwaiting = False
            print("Order Placed for :" + str(stockName) + " at price of : " + str(quantity) )
        else :
            while orderInfo['state'] == "unconfirmed" :
                sleep(1)
                orderStatus = RASESSION.get(orderStatus['url'])
                orderStatus.raise_for_status()
                orderInfo = orderStatus.json()
            # end while
        # end else
    # end while
    if orderAwaiting :
        print("Max retries reached, order not placed")
    # End if
    return orderAwaiting
# End Function

# Purchase the quantity worth of dollars of stockName
def buy_stock_units(stockName,quantity,price):
    """Purchase the quantity of stockName at price. 
    :param stockName: The stock to purchase.
    :type stockName: str
    :param quantity: Amount of $ worth of stocks to purchase
    :type quantity: int
    :param price: Price at which to buy the stocks
    :type price: float
    :returns: Boolean - Value whether stock purchased or not
    """
    orderAwaiting = True
    count = 0
    orderInfo = {}
    while orderAwaiting and count < 5 :

#        orderStatus = rs.order_buy_fractional_by_price(stockName,quantity,timeInForce='gfd',priceType='bid_price')
        orderStatus = rs.order_buy_limit(stockName,quantity,price,timeInForce='gfd',extendedHours=True)
        print(orderStatus)
        sleep(2)
        orderStatus = RASESSION.get(orderStatus['url'])
        orderStatus.raise_for_status()
        orderInfo = orderStatus.json()
        count = count + 1
        if orderInfo['state'] == 'queued' or orderInfo['state'] == 'confirmed':
            orderAwaiting = False
            print("Order Placed for :" + str(stockName) + " at price of : " + str(quantity) )
        else :
            while orderInfo['state'] == "unconfirmed" :
                sleep(1)
                orderStatus = RASESSION.get(orderStatus['url'])
                orderStatus.raise_for_status()
                orderInfo = orderStatus.json()
            # end while
        # end else
    # end while
    if orderAwaiting :
        print("Max retries reached, order not placed")
    # end if
    return orderAwaiting
# End Function


# Purchase the quantity worth of dollars of stockName
def buy_stock_fractional(stockName,quantity):
    """Updates the session header used by the requests library.
    :param stockName: The stock to purchase.
    :type stockName: str
    :param quantity: Amount of $ worth of stocks to purchase
    :type quantity: int
    :returns: None. Purchases the stock and outputs the status.
    """
    orderAwaiting = True
    count = 0
    orderInfo = {}
    while orderAwaiting and count < 5 :

        orderStatus = rs.order_buy_fractional_by_price(stockName,quantity,timeInForce='gfd',priceType='bid_price')
        print(orderStatus)
        sleep(2)
        orderStatus = RASESSION.get(orderStatus['url'])
        orderStatus.raise_for_status()
        orderInfo = orderStatus.json()
        count = count + 1
        if orderInfo['state'] == 'queued' or orderInfo['state'] == 'confirmed':
            orderAwaiting = False
            print("Order Placed for :" + str(stockName) + " at price of : " + str(quantity) )
        else :
            while orderInfo['state'] == "unconfirmed" :
                sleep(1)
                orderStatus = RASESSION.get(orderStatus['url'])
                orderStatus.raise_for_status()
                orderInfo = orderStatus.json()
            # end while
        # end else
    # end while
    if orderAwaiting :
        print("Max retries reached, order not placed")
    # end if
    return orderAwaiting
# End Function


# Sell the quantity worth of dollars of stockName
def sell_stock_fractional(stockName,quantity):
    """Updates the session header used by the requests library.
    :param stockName: The stock to sell.
    :type stockName: str
    :param quantity: Amount of $ worth of stocks to sell
    :type quantity: int
    :returns: None. Sales the stock and outputs the status. Robinhood has in built-in checks to not sell if you don't own a stock 
    """    
    orderAwaiting = True
    count = 0
    orderInfo = {}
    while orderAwaiting and count < 5 :
        orderStatus = rs.order_sell_fractional_by_price(stockName,quantity,timeInForce='gfd',priceType='ask_price')
        print(orderStatus)
        sleep(2)
        orderStatus = RASESSION.get(orderStatus['url'])
        orderStatus.raise_for_status()
        orderInfo = orderStatus.json()
        count = count + 1
        if orderInfo['state'] == 'queued' or orderInfo['state'] == 'confirmed':
            orderAwaiting = False
            print("Order Placed for :" + str(stockName) + " at price of : " + str(quantity) )
        else :
            while orderInfo['state'] == "unconfirmed" :
                sleep(1)
                orderStatus = RASESSION.get(orderStatus['url'])
                orderStatus.raise_for_status()
                orderInfo = orderStatus.json()
            # end while
        # end else
    # end while
    if orderAwaiting :
        print("Max retries reached, order not placed")
    # End if
    return orderAwaiting
# End Function


def get_holdings():
    holdings = rs.build_holdings()
    for key,value in holdings.items():
        print(f'{key:5}:  {value["quantity"].rjust(13)}')
    #End For
# End Function

def is_market_open():
    now = datetime.now(timeZone)
    print(f'Current time is : {now}\n')
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