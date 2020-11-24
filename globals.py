#import sys
import os
from requests import Session
from datetime import datetime
from pytz import timezone



RASESSION = Session()
orderRetries = 5
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


marketOpen = True
marketStartOffset = "09:30:00" # Time in EST for market open. 
marketEndOffset = "16:00:00" # Time in EST for Market close
timeMask = "%H:%M:%S"

#Market Start time
marketStart = datetime.strptime(marketStartOffset,timeMask) # convert to time object and get the start time
marketEnd = datetime.strptime(marketEndOffset,timeMask) # convert to time object and get close time.
# All transactions are going to happen in US East timezone. 
timeZone = timezone('US/Eastern')

#Show the current time in US Eastern Timezone
now = datetime.now(timeZone)
print('Current Time is : ' + str(now))


