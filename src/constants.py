from enum import Enum
import os

config = {**os.environ}


class Env(Enum):
    CONSUMER_KEY = config.get("CONSUMER_KEY")
    UCC = config.get("UCC")
    MOBILENUMBER = config.get("MOBILENUMBER")
    TOTP_KEY = config.get("TOTP_KEY")
    MPIN = config.get("MPIN")
    BOT_TOKEN = config.get("BOT_TOKEN")
    CHAT_ID = config.get("CHAT_ID")
