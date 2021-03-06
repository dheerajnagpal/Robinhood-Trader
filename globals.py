#import sys
import os
from requests import Session
from datetime import datetime
from pytz import timezone
import logging

# Get a separate stream handler to configure separately than File Level
console = logging.StreamHandler()

#Setting console logging at INFO. This has to be same or higher level than basic config below
console.setLevel(logging.INFO)

#Setting the base logging level to DEBUG for file hander and INFO for console takes over. Add console and file handlers
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        console
    ]
)






RASESSION = Session()
RASESSION.headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "en-US,en;q=1",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "X-Robinhood-API-Version": "1.315.0",
    "Connection": "keep-alive",
    "User-Agent": "*"
}


#Set the environment variable to robinhood username and password. 
robin_user = os.environ.get("robin_user")
robin_pass = os.environ.get("robin_pass")
robin_2FA = os.environ.get("robin_2FA")


marketStartOffset = "09:30:00" # Time in EST for market open. 
marketEndOffset = "16:00:00" # Time in EST for Market close
extMarketEndOffset = "18:00:00" # Time in EST for Extended market close
timeMask = "%H:%M:%S"

#Market Start time
marketStart = datetime.strptime(marketStartOffset,timeMask) # convert to time object and get the start time
marketEnd = datetime.strptime(marketEndOffset,timeMask) # convert to time object and get close time.
extMarketEnd = datetime.strptime(extMarketEndOffset,timeMask) #Convert to time object and get close time
# All transactions are going to happen in US East timezone. 
timeZone = timezone('US/Eastern')

#Show the current time in US Eastern Timezone
now = datetime.now(timeZone)
logging.debug('Current time is: %s', str(now))
#print('Current Time is : ' + str(now))

# Number of times to retry an order that doesn't go through in first try. 
orderRetries = 5


