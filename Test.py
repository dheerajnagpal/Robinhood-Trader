from auth import login
import utils as utils
import os
from time import sleep
import robin_stocks.robinhood as rs
import logging
from datetime import date


login()

#markets = rs.get_markets()
#print(markets)
#market_open = rs.get_market_today_hours('XNYS') # Is NYSE Open Today?
print(rs.get_market_hours("XNAS",date.today()))
#print(market_open)

print(utils.is_market_open())
