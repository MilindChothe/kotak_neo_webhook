from enum import Enum
import os

config = {**os.environ}


class Env(Enum):
    CONSUMER_KEY = config.get("CONSUMER_KEY")
    CONSUMER_SECRET = config.get("CONSUMER_SECRET")
    MOBILENUMBER = config.get("MOBILENUMBER")
    PASSWORD = config.get("PASSWORD")
    MPIN = config.get("MPIN")
    BOT_TOKEN = config.get("BOT_TOKEN")
    CHAT_ID = config.get("CHAT_ID")
