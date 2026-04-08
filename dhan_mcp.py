import os
import requests
from fastmcp import FastMCP
from dhanhq import dhanhq, DhanContext

mcp = FastMCP(name="DhanHQ Full MCP Server")

# Initialize credentials from environment
def get_client():
    client_id = os.getenv("DHAN_CLIENT_ID")
    access_token = os.getenv("DHAN_ACCESS_TOKEN")
    if not client_id or not access_token:
        raise EnvironmentError("Missing DHAN_CLIENT_ID or DHAN_ACCESS_TOKEN")
    return dhanhq(client_id, access_token)

# --- Account Tools ---
@mcp.tool()
def get_profile() -> dict:
    """Get user profile and account information."""
    return get_client().get_profile()

@mcp.tool()
def get_fund_limits() -> dict:
    """Get account balance and available margin details."""
    return get_client().get_fund_limits()

# --- Order Management ---
@mcp.tool()
def place_order(
    security_id: str,
    exchange_segment: str,
    transaction_type: str,
    quantity: int,
    order_type: str,
    product_type: str,
    price: float = 0,
    trigger_price: float = 0,
    validity: str = "DAY",
    after_market_order: bool = False,
    amo_time: str = "OPEN"
) -> dict:
    """
    Place a new order.
    - security_id: Security ID (e.g., '1333')
    - exchange_segment: 'NSE_EQ', 'BSE_EQ', 'NSE_FNO', etc.
    - transaction_type: 'BUY' or 'SELL'
    - quantity: Number of shares
    - order_type: 'LIMIT', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_MARKET'
    - product_type: 'CNC', 'INTRADAY', 'MARGIN', 'MTF', 'CO', 'BO'
    - price: Price for LIMIT orders (0 for MARKET)
    - trigger_price: Price for SL orders
    - validity: 'DAY' or 'IOC'
    """
    return get_client().place_order(
        security_id=security_id,
        exchange_segment=exchange_segment,
        transaction_type=transaction_type,
        quantity=quantity,
        order_type=order_type,
        product_type=product_type,
        price=price,
        trigger_price=trigger_price,
        validity=validity,
        after_market_order=after_market_order,
        amo_time=amo_time
    )

@mcp.tool()
def modify_order(order_id: str, quantity: int, order_type: str, price: float = 0, trigger_price: float = 0) -> dict:
    """Modify a pending order."""
    return get_client().modify_order(
        order_id=order_id,
        quantity=quantity,
        order_type=order_type,
        price=price,
        trigger_price=trigger_price
    )

@mcp.tool()
def cancel_order(order_id: str) -> dict:
    """Cancel a pending order."""
    return get_client().cancel_order(order_id)

@mcp.tool()
def get_order_book() -> dict:
    """Fetch current day's order book."""
    return get_client().get_order_list()

@mcp.tool()
def get_trade_book() -> dict:
    """Fetch current day's trade book."""
    return get_client().get_trade_book()

@mcp.tool()
def get_order_by_id(order_id: str) -> dict:
    """Get details of a specific order by ID."""
    return get_client().get_order_by_id(order_id)

# --- Portfolio Management ---
@mcp.tool()
def get_holdings() -> dict:
    """Get long-term holdings in the portfolio."""
    return get_client().get_holdings()

@mcp.tool()
def get_positions() -> dict:
    """Get real-time open positions."""
    return get_client().get_positions()

@mcp.tool()
def convert_position(
    from_product: str,
    to_product: str,
    exchange_segment: str,
    security_id: str,
    transaction_type: str,
    quantity: int
) -> dict:
    """Convert a position between product types (e.g., Intraday to CNC)."""
    return get_client().convert_position(
        from_product=from_product,
        to_product=to_product,
        exchange_segment=exchange_segment,
        security_id=security_id,
        transaction_type=transaction_type,
        quantity=quantity
    )

# --- Market Data ---
@mcp.tool()
def get_market_quote(instruments: list) -> dict:
    """
    Get real-time snapshot for up to 1000 instruments.
    - instruments: List of dicts like [{"ExchangeSegment": "NSE_EQ", "SecurityId": "1333"}]
    """
    # Using the Market Quote REST API
    url = "https://api.dhan.co/v2/marketquote/quote"
    headers = {
        "access-token": os.getenv("DHAN_ACCESS_TOKEN"),
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={"instruments": instruments})
    return response.json()

@mcp.tool()
def get_historical_data(security_id: str, exchange_segment: str, instrument_type: str, from_date: str, to_date: str, interval: str = "DAY") -> dict:
    """
    Get historical candle data.
    - from_date: 'YYYY-MM-DD'
    - to_date: 'YYYY-MM-DD'
    - interval: '1', '5', '15', '25', '60', 'DAY'
    """
    return get_client().get_historical_data(
        security_id=security_id,
        exchange_segment=exchange_segment,
        instrument_type=instrument_type,
        expiry_code=0,
        from_date=from_date,
        to_date=to_date,
        interval=interval
    )

@mcp.tool()
def get_intraday_data(security_id: str, exchange_segment: str, instrument_type: str, interval: str = "1") -> dict:
    """Get minute-level intraday data for last 5 trading days."""
    return get_client().get_intraday_data(
        security_id=security_id,
        exchange_segment=exchange_segment,
        instrument_type=instrument_type,
        interval=interval
    )

# --- Risk & Utils ---
@mcp.tool()
def calculate_margin(security_id: str, exchange_segment: str, transaction_type: str, quantity: int, order_type: str, product_type: str, price: float = 0) -> dict:
    """Calculate pre-trade margin requirement."""
    return get_client().calculate_margin(
        security_id=security_id,
        exchange_segment=exchange_segment,
        transaction_type=transaction_type,
        quantity=quantity,
        order_type=order_type,
        product_type=product_type,
        price=price
    )

@mcp.tool()
def renew_access_token() -> dict:
    """Renew the DhanHQ access token (valid for 24h)."""
    url = "https://api.dhan.co/v2/RenewToken"
    headers = {
        "access-token": os.getenv("DHAN_ACCESS_TOKEN"),
        "dhanClientId": os.getenv("DHAN_CLIENT_ID")
    }
    response = requests.post(url, headers=headers)
    return response.json()

def main():
    """Main entry point for the MCP server."""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
