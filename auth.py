from globals import robin_2FA, robin_pass, robin_user
import utils as utils
import robin_stocks as rs
import pyotp
import logging

'''
 # Logs into the Robinhood account. Doesn't take any parameters but utilizes the environment variables defined
 # in globals to get username, password and TOTP seed. If totp is blank, tries to log in with username and password
 # if a usernae or password are missing, they are asked for in the console. 
 # 
 # Additionally, sets the session headers in Utils for RASSION to run direct commands against Robinhood API 
 
 '''

def login():
    if robin_2FA != "" :
        robinOTP = pyotp.TOTP(robin_2FA).now()
        login_ticket = rs.login(username=robin_user,
            password=robin_pass,
            expiresIn=86400,
            mfa_code=robinOTP)
    else :
        login_ticket = rs.login(username=robin_user,
            password=robin_pass,
            expiresIn=86400,
            by_sms=True)
    #End else
    logging.debug(f'Login ticket is \n {login_ticket}')
    utils.update_session('Authorization', '{0} {1}'.format(login_ticket['token_type'], login_ticket['access_token']))
#End login
