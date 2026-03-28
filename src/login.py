import pyotp
from neo_api_client import NeoAPI

from .constants import Env


def get_client() -> NeoAPI:
    # on_message, on_open, on_close and on_error is a call back function we will provide the response for the subscribe method.
    # access_token is an optional one. If you have barrier token then pass and consumer_key and consumer_secret will be optional.
    # environment by default uat you can pass prod to connect to live server
    client = NeoAPI(
        environment="prod",
        access_token=None,
        neo_fin_key=None,
        consumer_key=Env.CONSUMER_KEY.value,
    )

    totp = pyotp.TOTP(Env.TOTP_KEY.value)

    client.totp_login(
        mobile_number=Env.MOBILENUMBER.value, ucc=Env.UCC.value, totp=totp.now()
    )

    client.totp_validate(mpin=Env.MPIN.value)

    return client
