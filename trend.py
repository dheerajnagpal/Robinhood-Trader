import numpy as np
import logging
import json
import os
from time import sleep
from datetime import datetime
from pytz import timezone
import pytz
import csv

# Get a separate stream handler to configure separately than File Level
console = logging.StreamHandler()

#Setting console logging at INFO. This has to be same or higher level than basic config below
console.setLevel(logging.DEBUG)

#Setting the base logging level to DEBUG for file hander and INFO for console takes over. Add console and file handlers
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        console
    ]
)


def trend(index,series,order=1) :
    coeff = np.polyfit(index,list(series),order)
    return coeff



stockList = ['SPY', 'VYM', 'VO', 'VOE', 'VB', 'VNQ', 'VNQI', 'VBR', 'VEA', 'VSS']

stockData = {}
emaDuration1 = 13
emaDuration2 = 26
csvData = {}



with open("StockData.json", 'r') as stockDataFileReader:
    stockDataHistorical = json.load(stockDataFileReader)

for stock in stockList:
    logging.debug(f'{stock}')
    stockData = stockDataHistorical[stock] # Get the stock data dictionary from the item in stocklist
#    logging.info(stockData[-1])
    i = 0
    dateIndex = []
    numericIndex = []
    emaDifference = []
    for pointer in range(-10,0):
        priorDateStr = stockData[pointer]['date']
        dateIndex.append(priorDateStr)
        numericIndex.append(i)
#        dateIndex.append(datetime.strptime(priorDateStr,"%Y-%m-%dT%H:%M:%SZ"))
#        dateIndex[i] = datetime.strptime(priorDateStr,"%Y-%m-%dT%H:%M:%SZ")
        logging.debug(dateIndex[i])
        priorEMA1 = stockData[pointer]['ema'+str(emaDuration1)]
        priorEMA2 = stockData[pointer]['ema'+str(emaDuration2)]
        emaDifference.append(priorEMA1 - priorEMA2)
        logging.debug(f'I is {i}, Date is {dateIndex[i]} and EMA Difference is {emaDifference[i]}')
        i = i+1
    logging.debug(emaDifference)
    trendCoeff = trend(numericIndex,emaDifference,1)
    csvUnit = {}
    csvUnit['stock'] = stock
    csvUnit['ema'+ str(emaDuration1)] = priorEMA1
    csvUnit['trend'] = trendCoeff[-2]
    csvData.setdefault(str(dateIndex[-1]),[]).append(csvUnit)
    logging.info(f'Stock is {stock} Date is {dateIndex[-1]}, Current Value is {priorEMA1} and Trend Coefficient is {trendCoeff[-2]}')

file = open('trend.csv', 'w+', newline ='') 
with file:
    write = csv.writer(file) 
    write.writerows(csvData) 

    

