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



for stock in stockList:
    history = rs.get_stock_historicals(stock,interval='day',span='5year',bounds='regular')
#print(spy)
    priorEMA1 = 0
    priorEMA2 = 0
    for item in history :
        unit = {}
        unit['date'] = item['begins_at']
        unit['open'] = float(item['open_price'])
        unit['close'] = float(item['close_price'])
        if priorEMA1 == 0 :
            currentEMA1 = unit['close']
            emaDifference1 = 0
            currentEMA2 = unit['close']
            emaDifference2 = 0
        else :
            currentEMA1 = get_EMA(float(unit['close']),priorEMA1,emaDuration1)
            emaDifference1 = currentEMA1 - priorEMA1
            currentEMA2 = get_EMA(float(unit['close']),priorEMA2,emaDuration2)
            emaDifference2 = currentEMA2 - priorEMA2
        unit['ema'+str(emaDuration1)] = float(currentEMA1)
        unit['ema'+str(emaDuration2)] = float(currentEMA2)
        priorEMA1 = float(currentEMA1)
        priorEMA2 = float(currentEMA2)
        logging.info(unit)
        stockData.setdefault(stock,[]).append(unit)

stockDataFile = open("StockData.json",'w')
stockDataFile.write(json.dumps(stockData,indent=4))

