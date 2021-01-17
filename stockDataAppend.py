from auth import login
import utils as utils
import os
from time import sleep
import robin_stocks as rs
from datetime import datetime
from pytz import timezone
import pytz
import json
import logging

login()

# Get a separate stream handler to configure separately than File Level
console = logging.StreamHandler()

#Setting console logging at INFO. This has to be same or higher level than basic config below
console.setLevel(logging.DEBUG)

#Setting the base logging level to DEBUG for file hander and INFO for console takes over. Add console and file handlers
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        console
    ]
)
stockList = ['SPY', 'VYM', 'VO', 'VOE', 'VB', 'VNQ', 'VNQI', 'VBR', 'VEA', 'VSS']

stockData = {}
emaDuration1 = 13
emaDuration2 = 26


def get_EMA(currentPrice,priorEMA,emaDuration):
    smoothing = 2
    multiplier = smoothing / (emaDuration + 1)
    ema = (currentPrice * multiplier) + (priorEMA * (1-multiplier))
    return ema
#End function

with open("StockData.json", 'r') as stockDataFileReader:
    stockDataHistorical = json.load(stockDataFileReader)

for stock in stockList:
    logging.debug(f'{stock}')
    stockData = stockDataHistorical[stock] # Get the stock data dictionary from the item in stocklist
#    logging.info(stockData[-1])
    priorDateStr = stockData[-1]['date']
    priorDate = datetime.strptime(priorDateStr,"%Y-%m-%dT%H:%M:%SZ")
    logging.info(priorDate)
    priorEMA1 = stockData[-1]['ema'+str(emaDuration1)]
    priorEMA2 = stockData[-1]['ema'+str(emaDuration2)]
    history = rs.get_stock_historicals(stock,interval='day',span='week',bounds='regular')
    for item in history:
        unit = {}
        unit['date'] = item['begins_at']
        currentDate = datetime.strptime(unit['date'],"%Y-%m-%dT%H:%M:%SZ")
        if currentDate > priorDate:
            unit['open'] = float(item['open_price'])
            unit['close'] = float(item['close_price'])
            currentEMA1 = get_EMA(float(unit['close']), priorEMA1, emaDuration1)
            currentEMA2 = get_EMA(float(unit['close']), priorEMA2, emaDuration2)
            unit['ema'+str(emaDuration1)] = float(currentEMA1)
            unit['ema'+str(emaDuration2)] = float(currentEMA2)
            priorEMA1 = float(currentEMA1)
            priorEMA2 = float(currentEMA2)       
#        logging.info(unit)
            stockData.append(unit)
#        stockData.setdefault(stock,[]).append(unit)
    logging.info(stockData)
    stockDataHistorical[stock] = stockData

logging.info(stockDataHistorical)
stockDataFile = open("StockData.json", 'w')
stockDataFile.write(json.dumps(stockDataHistorical, indent=4))
