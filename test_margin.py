import os
import sys
from dotenv import load_dotenv

load_dotenv()

from dhanhq import dhanhq

client = dhanhq(os.getenv("DHAN_CLIENT_ID"), os.getenv("DHAN_ACCESS_TOKEN"))

print("=== MARGIN CALCULATOR TEST ===\n")

for qty in [10, 20, 50, 100]:
    result = client.margin_calculator(
        security_id="12018",
        exchange_segment="NSE_EQ",
        transaction_type="BUY",
        quantity=qty,
        product_type="INTRADAY",
        price=44.03,
        trigger_price=0,
    )

    if result.get("status") == "success":
        data = result.get("data", {})
        trade_value = qty * 44.03
        margin = data.get("totalMargin")
        leverage = data.get("leverage")
        print(
            f"Qty: {qty} | Trade: Rs {trade_value:.2f} | Margin: Rs {margin} | Leverage: {leverage}"
        )
