from neo_api_client import NeoAPI

from .constants import Env


def get_client() -> NeoAPI:
    # on_message, on_open, on_close and on_error is a call back function we will provide the response for the subscribe method.
    # access_token is an optional one. If you have barrier token then pass and consumer_key and consumer_secret will be optional.
    # environment by default uat you can pass prod to connect to live server
    client = NeoAPI(consumer_key=Env.CONSUMER_KEY.value, consumer_secret=Env.CONSUMER_SECRET.value,
                    environment='prod', on_message=None, on_error=None, on_close=None, on_open=None)

    # Initiate login by passing any of the combinations mobilenumber & password (or) pan & password (or) userid & password
    # Also this will generate the OTP to complete 2FA
    client.login(mobilenumber=Env.MOBILENUMBER.value,
                 password=Env.PASSWORD.value)

    # Complete login and generate session token
    client.session_2fa(OTP=Env.MPIN.value)

    return client
