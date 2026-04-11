import os
import sys
from dotenv import load_dotenv

load_dotenv()

from dhanhq import dhanhq

client_id = os.getenv("DHAN_CLIENT_ID")
access_token = os.getenv("DHAN_ACCESS_TOKEN")

print(f"Client: {client_id}")

try:
    client = dhanhq(client_id, access_token)
    print("\n=== FUND LIMITS ===")
    print(client.get_fund_limits())

    print("\n=== HOLDINGS ===")
    print(client.get_holdings())

except Exception as e:
    print(f"Error: {e}")
