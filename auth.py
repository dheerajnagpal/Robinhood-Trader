from utils import *
import pyotp

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
    print(login_ticket)
    update_session('Authorization', '{0} {1}'.format(login_ticket['token_type'], login_ticket['access_token']))
#End login
