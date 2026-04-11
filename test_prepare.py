import os
import sys
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

from dhanhq import dhanhq

client = dhanhq(os.getenv("DHAN_CLIENT_ID"), os.getenv("DHAN_ACCESS_TOKEN"))

print("=== PREPARE TRADE TEST ===\n")

security_id = "12018"
symbol_map = {"12018": "SUZLON.NS", "5926": "IRFC.NS", "4726": "IDBI.NS"}
symbol = symbol_map.get(security_id, security_id + ".NS")

fund_data = client.get_fund_limits()
available_capital = fund_data.get("data", {}).get("availabelBalance", 0)

df = yf.download(symbol, period="5d", interval="15m", progress=False)
current_price = float(df["Close"].iloc[-1]) if not df.empty else 0

df_daily = yf.download(symbol, period="1mo", interval="1d", progress=False)
sma_20 = (
    float(df_daily["Close"].tail(20).mean()) if len(df_daily) >= 20 else current_price
)
high_20d = (
    float(df_daily["High"].tail(20).max()) if len(df_daily) >= 20 else current_price
)
low_20d = (
    float(df_daily["Low"].tail(20).min()) if len(df_daily) >= 20 else current_price
)

usable_capital = available_capital * 0.5
max_qty = int(usable_capital / (current_price * 0.20))

print(f"Capital: Rs {available_capital}")
print(f"Price: Rs {current_price}")
print(f"SMA20: Rs {sma_20}")
print(f"Max Qty: {max_qty}")
