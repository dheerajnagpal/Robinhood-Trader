# Robinhood-Trader

Code for algorithmic trading in Robinhood. 

**Please note, this is a test strategy to demonstrate how automated transaction can be done on Robinhood. This is not a strategy recommendation. A good possibility is that this strategy would lose money**


The following items are required for the code to function.

## Prerequisites

- Environment variables
    - $robin_user - Username for the robinhood user
    - $robin_pass - password for the robinhood user
    - $robin_2FA - 2 FA code for the 2FA for the user. If there is no 2FA on the account, then leave this blank. To set up a 2FA (Highy recommended), in Robinhood app, go to Settings --> Security and enable 2FA authentication. Once the bar code is generated, choose "Cannot scan code" and then save the generated code in this environment variable. Also save the code in your TOTP authenticator (Google Authenticator or similar) so that you can log into the account from web.
- Python (3.x) and pip
- Install robin_stocks. ```pip install robin_stocks```
- Install pytz. ```pip install pytz```

## Robinhood account changes
- Watchlist named "Movement_Trades" 
    - In your robinhood account, create a watchlist called "Movement_Trades" that will store the stocks that you want it to trade automatically
    - To change the name of the list, change it in global.py


## Configuration

- Modify the buyOnMovement.py file to set the number of stocks to buy and thresholds at which to buy. There are 5 thresholds and corresponding number of stocks. Only 3 are in use, hence others are set at 0
