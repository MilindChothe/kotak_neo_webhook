
from pydantic import BaseModel


class Payload(BaseModel):
    trading_symbol: str
    quantity: str
    transaction_type: str
    product: str
    amo: str = "NO"
    pf: str = "N"
    disclosed_quantity: str = "0"
    price: str = "0"
    exchange_segment: str = "NFO"
    order_type: str = "MKT"
    validity: str = "DAY"
