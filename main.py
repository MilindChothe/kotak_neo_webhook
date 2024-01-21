import json
import aiohttp
from fastapi import FastAPI
from src.constants import Env

from src.login import get_client
from src.models import Payload

app = FastAPI()


@app.get("/")
def status():
    return {"status": "OK"}


@app.post("/webhook")
async def webhook(body: Payload):
    try:
        client = get_client()

        oid = client.place_order(
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

        async with aiohttp.ClientSession() as session:
            base_url = f"https://api.telegram.org/bot{Env.BOT_TOKEN.value}/sendMessage"

            async with session.get(base_url, params={
                "chat_id": Env.CHAT_ID.value,
                "text": json.dumps({"body": body.model_dump(), "oid": oid}, indent=4)
            }) as _:
                pass

        return {"status": "Ok"}
    except Exception as e:
        return {"status": "Not_Ok", "message": e}
