from datetime import datetime, tzinfo
import json
from logging import getLogger
from zoneinfo import ZoneInfo
import aiohttp
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from src.constants import Env

from src.login import get_client
from src.models import Payload
from neo_api_client import NeoAPI
import jwt


LOGGER = getLogger()

CLIENT: NeoAPI = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global CLIENT
    CLIENT = get_client()
    yield
    CLIENT.logout()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def status():
    return {"status": "OK"}


@app.post("/webhook")
async def webhook(body: Payload):
    global CLIENT

    try:
        # Verify bearer_token
        jwt.decode(CLIENT.configuration.bearer_token, options={
            'verify_signature': False,
            'verify_exp': True,
        })
        # Verify edit_token
        jwt.decode(CLIENT.configuration.edit_token, options={
            'verify_signature': False,
            'verify_exp': True,
        })
    except Exception as e:
        LOGGER.exception(e)
        CLIENT = get_client()

    try:
        oid = CLIENT.place_order(
            trading_symbol=body.trading_symbol,
            quantity=body.quantity,
            transaction_type=body.transaction_type,
            product=body.product,
            amo=body.amo,
            pf=body.pf,
            disclosed_quantity=body.disclosed_quantity,
            price=body.price,
            exchange_segment=body.exchange_segment,
            order_type=body.order_type,
            validity=body.validity,
        )

        payload = {
            "datetime": datetime.now(tz=ZoneInfo('Asia/Kolkata')).strftime("%d-%m-%Y %H:%M:%S"),
            "body": body.model_dump(),
            "oid": oid,
        }

        LOGGER.info(payload)

        async with aiohttp.ClientSession() as session:
            base_url = f"https://api.telegram.org/bot{Env.BOT_TOKEN.value}/sendMessage"

            async with session.get(base_url, params={
                "chat_id": Env.CHAT_ID.value,
                "text": json.dumps(payload, indent=4)
            }) as _:
                pass

        return {"status": "Ok"}
    except Exception as e:
        LOGGER.exception(e)
        return {"status": "Not_Ok", "message": e}
