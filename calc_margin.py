import os
from dotenv import load_dotenv

load_dotenv()

from dhanhq import dhanhq

client = dhanhq(os.getenv("DHAN_CLIENT_ID"), os.getenv("DHAN_ACCESS_TOKEN"))

result = client.margin_calculator(
    security_id="12018",
    exchange_segment="NSE_EQ",
    transaction_type="BUY",
    quantity=20,
    product_type="INTRADAY",
    price=44.03,
    trigger_price=0,
)
import json

print(json.dumps(result, indent=2))
