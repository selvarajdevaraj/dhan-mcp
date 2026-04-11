import os
from dotenv import load_dotenv

load_dotenv()

from dhanhq import dhanhq

client = dhanhq(os.getenv("DHAN_CLIENT_ID"), os.getenv("DHAN_ACCESS_TOKEN"))

print("=== FUND LIMITS ===")
print(client.get_fund_limits())

print("\n=== POSITIONS ===")
print(client.get_positions())

print("\n=== ORDER BOOK ===")
print(client.get_order_book())
