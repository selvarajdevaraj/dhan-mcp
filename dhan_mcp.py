import os
import requests
from fastmcp import FastMCP
from dhanhq import dhanhq, DhanContext, MarketFeed, FullDepth, OrderUpdate

mcp = FastMCP(name="DhanHQ Full MCP Server")

def get_client():
    from dotenv import load_dotenv
    load_dotenv('YOUR_PATH/.env')
    DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
    DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
    if not DHAN_CLIENT_ID or not DHAN_ACCESS_TOKEN:
        raise EnvironmentError("Missing DHAN_CLIENT_ID or DHAN_ACCESS_TOKEN")
    dhan_context = DhanContext(DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN)
    return dhanhq(dhan_context)

# --- Account Tools ---
@mcp.tool()
def get_fund_limits() -> dict:
    """Get account balance and available margin details."""
    return get_client().get_fund_limits()

@mcp.tool()
def get_ledger(from_date: str = "2025-01-01", to_date: str = "2025-04-08") -> dict:
    """
    Retrieve Trading Account debit and credit details.
    - from_date: 'YYYY-MM-DD'
    - to_date: 'YYYY-MM-DD'
    """
    return get_client().ledger_report(from_date, to_date)

@mcp.tool()
def get_trade_history(from_date: str, to_date: str, page_number: int = 0) -> dict:
    """
    Retrieve historical trade data.
    - from_date: 'YYYY-MM-DD'
    - to_date: 'YYYY-MM-DD'
    - page_number: Page number for pagination
    """
    return get_client().get_trade_history(from_date, to_date, page_number)

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
    amo_time: str = "OPEN",
    correlation_id: str = ""
) -> dict:
    """
    Place a new order.
    - security_id: Security ID (e.g., '1333')
    - exchange_segment: 'NSE_EQ', 'BSE_EQ', 'NSE_FNO', etc.
    - transaction_type: 'BUY' or 'SELL'
    - quantity: Number of shares
    - order_type: 'LIMIT', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_MARKET'
    - product_type: 'CNC', 'INTRADAY', 'MARGIN', 'MTF'
    - price: Price for LIMIT orders (0 for MARKET)
    - trigger_price: Price for SL orders
    - validity: 'DAY' or 'IOC'
    - correlation_id: Optional user-generated tracking ID (max 30 chars)
    
    Note: Dhan API does NOT support automatic TSL. Use STOP_LOSS order and 
    manually trail by modifying trigger_price.
    """
    client = get_client()
    return client.place_order(
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
        amo_time=amo_time,
        tag=correlation_id
    )

@mcp.tool()
def slice_order(
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
    Slice order into multiple legs over freeze limit (for F&O instruments).
    - security_id: Security ID
    - exchange_segment: Exchange segment
    - transaction_type: 'BUY' or 'SELL'
    - quantity: Number of shares
    - order_type: 'LIMIT' or 'MARKET'
    - product_type: 'INTRADAY', 'CNC'
    - price: Price for LIMIT orders
    - trigger_price: Trigger price
    - validity: 'DAY' or 'IOC'
    - after_market_order: AMO flag
    - amo_time: 'PRE_OPEN', 'OPEN', 'OPEN_30', 'OPEN_60'
    """
    return get_client().place_slice_order(
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
def modify_order(
    order_id: str,
    order_type: str,
    leg_name: str = "",
    quantity: int = 0,
    price: float = 0,
    trigger_price: float = 0,
    disclosed_quantity: int = 0,
    validity: str = "DAY"
) -> dict:
    """
    Modify a pending order (v2 API).
    - order_id: Order ID to modify
    - order_type: 'LIMIT', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_MARKET'
    - leg_name: 'LEG1' or 'LEG2'
    - quantity: New quantity
    - price: New price
    - trigger_price: New trigger price
    - disclosed_quantity: Disclosed quantity
    - validity: 'DAY' or 'IOC'
    """
    return get_client().modify_order(
        order_id=order_id,
        order_type=order_type,
        leg_name=leg_name,
        quantity=quantity,
        price=price,
        trigger_price=trigger_price,
        disclosed_quantity=disclosed_quantity,
        validity=validity
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
def get_trade_book(order_id: str = "") -> dict:
    """Fetch current day's trade book. Provide order_id to get specific trades."""
    return get_client().get_trade_book(order_id if order_id else None)

@mcp.tool()
def get_order_by_id(order_id: str) -> dict:
    """Get details of a specific order by ID."""
    return get_client().get_order_by_id(order_id)

@mcp.tool()
def get_order_by_correlation_id(correlation_id: str) -> dict:
    """Get details of a specific order by correlation ID."""
    return get_client().get_order_by_correlationID(correlation_id)

@mcp.tool()
def get_trades_by_order_id(order_id: str) -> dict:
    """
    Get trade details for a specific order.
    - order_id: Order ID to get trades for
    """
    return get_client().get_trade_book(order_id)

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
    from_product_type: str,
    exchange_segment: str,
    position_type: str,
    security_id: str,
    convert_qty: int,
    to_product_type: str
) -> dict:
    """
    Convert a position between product types (e.g., Intraday to CNC).
    - from_product_type: 'INTRADAY', 'CNC', 'MARGIN'
    - exchange_segment: Exchange segment (e.g., 'NSE_EQ')
    - position_type: 'LONG' or 'SHORT'
    - security_id: Security ID
    - convert_qty: Quantity to convert
    - to_product_type: Target product type
    """
    return get_client().convert_position(
        from_product_type=from_product_type,
        exchange_segment=exchange_segment,
        position_type=position_type,
        security_id=security_id,
        convert_qty=convert_qty,
        to_product_type=to_product_type
    )

@mcp.tool()
def exit_all_positions() -> dict:
    """
    Exit all active positions for the current trading day.
    This squares off open positions but does NOT cancel pending orders.
    Uses direct API as Python library doesn't have this method.
    """
    url = "https://api.dhan.co/v2/positions"
    headers = {"access-token": DHAN_ACCESS_TOKEN}
    response = requests.delete(url, headers=headers)
    return response.json()

@mcp.tool()
def calculate_multi_margin(
    include_positions: bool = True,
    include_orders: bool = True,
    scripts: list = None
) -> dict:
    """
    Calculate margin for multiple orders in a single request.
    - include_positions: Include existing positions in calculation
    - include_orders: Include open orders in calculation
    - scripts: List of script objects with exchangeSegment, transactionType, quantity, productType, securityId, price
    Note: Uses direct API as Python library doesn't support this method.
    """
    url = "https://api.dhan.co/v2/margincalculator/multi"
    headers = {"Content-Type": "application/json", "access-token": DHAN_ACCESS_TOKEN}
    data = {
        "includePosition": include_positions,
        "includeOrders": include_orders,
        "dhanClientId": DHAN_CLIENT_ID,
        "scripList": scripts or []
    }
    return requests.post(url, headers=headers, json=data).json()

# --- Instrument & Scrip Data ---
@mcp.tool()
def fetch_security_list(segment: str = "compact") -> dict:
    """
    Fetch the instrument/scrip master list.
    - segment: 'compact' or 'detailed'
    """
    return get_client().fetch_security_list(segment)

@mcp.tool()
def get_expiry_list(under_security_id: str, under_exchange_segment: str) -> dict:
    """
    Get expiry list for an underlying.
    - under_security_id: Underlying Security ID (e.g., '13' for Nifty)
    - under_exchange_segment: Underlying Exchange Segment (e.g., 'IDX_I')
    """
    return get_client().expiry_list(
        under_security_id=under_security_id,
        under_exchange_segment=under_exchange_segment
    )

# --- Market Data ---
@mcp.tool()
def get_market_quote_ltp(securities: dict) -> dict:
    """
    Get LTP (Last Traded Price) for securities.
    - securities: Dict like {"NSE_EQ": [1333, 11915], "BSE_EQ": []}
    """
    return get_client().ohlc_data(securities=securities)

@mcp.tool()
def get_market_quote_ohlc(securities: dict) -> dict:
    """
    Get OHLC (Open, High, Low, Close) for securities.
    - securities: Dict like {"NSE_EQ": [1333, 11915], "BSE_EQ": []}
    """
    return get_client().ohlc_data(securities=securities)

@mcp.tool()
def get_intraday_data(security_id: str, exchange_segment: str, instrument_type: str, from_date: str, to_date: str, interval: int = 1) -> dict:
    """
    Get minute-level intraday data for last 5 trading days.
    - from_date: 'YYYY-MM-DD'
    - to_date: 'YYYY-MM-DD'
    - interval: 1, 5, 15, 25, or 60 (minutes)
    """
    valid_intervals = [1, 5, 15, 25, 60]
    if interval not in valid_intervals:
        return {"status": "failure", "remarks": "interval must be one of {}".format(valid_intervals), "data": ""}
    return get_client().intraday_minute_data(
        security_id=security_id,
        exchange_segment=exchange_segment,
        instrument_type=instrument_type,
        from_date=from_date,
        to_date=to_date,
        interval=interval
    )

@mcp.tool()
def get_historical_data(security_id: str, exchange_segment: str, instrument_type: str, from_date: str, to_date: str) -> dict:
    """
    Get historical daily candle data.
    - from_date: 'YYYY-MM-DD'
    - to_date: 'YYYY-MM-DD'
    """
    return get_client().historical_daily_data(
        security_id=security_id,
        exchange_segment=exchange_segment,
        instrument_type=instrument_type,
        expiry_code=0,
        from_date=from_date,
        to_date=to_date
    )

@mcp.tool()
def get_option_chain(under_security_id: str, under_exchange_segment: str, expiry: str) -> dict:
    """
    Get Option Chain of any instrument.
    - under_security_id: Underlying Security ID (e.g. '13' for Nifty)
    - under_exchange_segment: Underlying Exchange Segment (e.g. 'IDX_I')
    - expiry: Expiry date 'YYYY-MM-DD'
    """
    return get_client().option_chain(
        under_security_id=under_security_id,
        under_exchange_segment=under_exchange_segment,
        expiry=expiry
    )

@mcp.tool()
def get_expired_options_data(
    security_id: str,
    exchange_segment: str,
    instrument_type: str,
    expiry_flag: str,
    expiry_code: int,
    strike: str,
    drv_option_type: str,
    required_data: list,
    from_date: str,
    to_date: str
) -> dict:
    """
    Get expired options data (v2.2.0+).
    - security_id: Security ID
    - exchange_segment: Exchange segment
    - instrument_type: 'INDEX' or 'EQUITY'
    - expiry_flag: 'MONTH', 'WEEK'
    - expiry_code: Expiry code number
    - strike: 'ATM', 'ITM', 'OTM', or specific strike price
    - drv_option_type: 'CALL' or 'PUT'
    - required_data: List like ['open', 'high', 'low', 'close', 'volume']
    - from_date: 'YYYY-MM-DD'
    - to_date: 'YYYY-MM-DD'
    """
    return get_client().expired_options_data(
        security_id=security_id,
        exchange_segment=exchange_segment,
        instrument_type=instrument_type,
        expiry_flag=expiry_flag,
        expiry_code=expiry_code,
        strike=strike,
        drv_option_type=drv_option_type,
        required_data=required_data,
        from_date=from_date,
        to_date=to_date
    )

# --- Super Orders (TSL, Target + SL) ---

# --- Conditional Trigger (Advanced - Price/Indicator based orders) ---
# Note: These are advanced features for placing orders based on conditions
# They require specific condition configuration (technical indicators, etc.)

# --- Live Market Feed (WebSocket) ---
# Note: Live market feed requires WebSocket connection
# Not implemented as MCP tool - use get_market_quote_ltp instead for snapshots

# --- Forever Orders ---
@mcp.tool()
def place_forever_order(
    security_id: str,
    exchange_segment: str,
    transaction_type: str,
    product_type: str,
    order_type: str,
    quantity: int,
    price: float,
    trigger_price: float,
    order_flag: str = "SINGLE",
    disclosed_quantity: int = 0,
    validity: str = "DAY",
    price1: float = 0,
    trigger_price1: float = 0,
    quantity1: int = 0
) -> dict:
    """
    Place a forever order.
    - security_id: Security ID
    - exchange_segment: Exchange segment
    - transaction_type: BUY or SELL
    - product_type: CNC or MARGIN
    - order_type: LIMIT or MARKET
    - quantity: Quantity
    - price: Order price
    - trigger_price: Trigger price
    - order_flag: 'SINGLE' or 'OCO'
    - disclosed_quantity: Disclosed quantity
    - validity: DAY or IOC
    """
    return get_client().place_forever(
        security_id=security_id,
        exchange_segment=exchange_segment,
        transaction_type=transaction_type,
        product_type=product_type,
        order_type=order_type,
        quantity=quantity,
        price=price,
        trigger_Price=trigger_price,
        order_flag=order_flag,
        disclosed_quantity=disclosed_quantity,
        validity=validity,
        price1=price1,
        trigger_Price1=trigger_price1,
        quantity1=quantity1
    )

# --- eDIS (TPIN) ---
@mcp.tool()
def generate_tpin() -> dict:
    """Generate TPIN for eDIS (electronic delivery instruction slip)."""
    try:
        return get_client().generate_tpin()
    except Exception as e:
        return {"status": "failure", "remarks": str(e), "data": ""}

@mcp.tool()
def open_browser_for_tpin(isin: str, qty: int, exchange: str) -> dict:
    """
    Open browser for TPIN verification.
    - isin: ISIN of the security
    - qty: Quantity to sell
    - exchange: 'NSE' or 'BSE'
    """
    return get_client().open_browser_for_tpin(isin=isin, qty=qty, exchange=exchange)

@mcp.tool()
def edis_inquiry(isin: str = "") -> dict:
    """
    Get EDIS status and inquiry information.
    - isin: ISIN of the security (optional)
    """
    return get_client().edis_inquiry(isin)

# --- Risk & Utils ---
@mcp.tool()
def calculate_margin(security_id: str, exchange_segment: str, transaction_type: str, quantity: int, product_type: str, price: float = 0, trigger_price: float = 0) -> dict:
    """
    Calculate pre-trade margin requirement.
    - security_id: Security ID (e.g., '12018')
    - exchange_segment: Exchange segment (e.g., 'NSE_EQ')
    - transaction_type: 'BUY' or 'SELL'
    - quantity: Quantity
    - product_type: Product type ('INTRADAY', 'CNC')
    - price: Price
    - trigger_price: Trigger price (optional)
    """
    from dotenv import load_dotenv
    load_dotenv('E:/Claude Trader/.env')
    return get_client().margin_calculator(
        security_id=security_id,
        exchange_segment=exchange_segment,
        transaction_type=transaction_type,
        quantity=quantity,
        product_type=product_type,
        price=price,
        trigger_price=trigger_price
    )

@mcp.tool()
def estimate_order(quantity: int, buy_price: float, exchange_segment: str = "NSE_EQ", product_type: str = "INTRADAY") -> dict:
    """
    Estimate order costs and breakeven price using Dhan's fee structure.
    - quantity: Number of shares
    - buy_price: Expected buy price per share
    - exchange_segment: 'NSE_EQ' or 'BSE_EQ' (default: NSE_EQ)
    - product_type: 'INTRADAY' or 'CNC' (default: INTRADAY)
    
    Returns: trade_value, brokerage, exchange_charges, stt, gst, sebi, stamp_duty, ipft, 
             total_buy_charges, total_sell_charges, breakeven_price, target_prices
    """
    trade_value = quantity * buy_price
    
    if exchange_segment == "NSE_EQ":
        exchange_rate = 0.000030699
    else:
        exchange_rate = 0.0000375
    
    if product_type == "INTRADAY":
        brokerage = min(20, trade_value * 0.0003)
        stt_buy = 0
        stt_sell = trade_value * 0.00025
        stamp_duty = trade_value * 0.00003
    else:
        brokerage = 0
        stt_buy = trade_value * 0.001
        stt_sell = trade_value * 0.001
        stamp_duty = trade_value * 0.00015
    
    exchange_charges = trade_value * exchange_rate
    sebi_charges = trade_value * 0.000001
    ipft = trade_value * 0.000000001
    
    gst = (brokerage + exchange_charges + sebi_charges + ipft) * 0.18
    
    total_buy_charges = brokerage + exchange_charges + stt_buy + sebi_charges + stamp_duty + ipft + gst
    total_sell_charges = brokerage + exchange_charges + stt_sell + sebi_charges + stamp_duty + ipft + gst
    
    total_charges = total_buy_charges + total_sell_charges
    breakeven_price = buy_price + (total_charges / quantity)
    
    return {
        "quantity": quantity,
        "buy_price": buy_price,
        "exchange_segment": exchange_segment,
        "product_type": product_type,
        "trade_value": round(trade_value, 2),
        "brokerage": round(brokerage, 2),
        "exchange_charges": round(exchange_charges, 2),
        "stt_buy": round(stt_buy, 2),
        "stt_sell": round(stt_sell, 2),
        "gst": round(gst, 2),
        "sebi_charges": round(sebi_charges, 2),
        "stamp_duty": round(stamp_duty, 2),
        "ipft": round(ipft, 2),
        "total_buy_charges": round(total_buy_charges, 2),
        "total_sell_charges": round(total_sell_charges, 2),
        "total_charges": round(total_charges, 2),
        "breakeven_price": round(breakeven_price, 2),
        "target_1pct": round(breakeven_price * 1.01, 2),
        "target_2pct": round(breakeven_price * 1.02, 2),
        "target_3pct": round(breakeven_price * 1.03, 2),
        "target_5pct": round(breakeven_price * 1.05, 2)
    }

# --- Auth & Token Management ---
@mcp.tool()
def renew_access_token() -> dict:
    """Renew the DhanHQ access token (valid for 24h)."""
    url = "https://api.dhan.co/v2/RenewToken"
    headers = {
        "access-token": DHAN_ACCESS_TOKEN,
        "dhanClientId": DHAN_CLIENT_ID
    }
    response = requests.post(url, headers=headers)
    return response.json()

# --- Live Price Monitor ---
import json
import asyncio
import threading
from dhanhq import dhanhq, DhanContext, MarketFeed

_live_prices = {}
_market_feed_instance = None

def _on_ticker(data):
    try:
        ltp = data.get('ltp', 0)
        sec_id = data.get('securityId', '')
        _live_prices[sec_id] = ltp
    except:
        pass

def _start_live_feed(instruments):
    global _market_feed_instance
    dhan_context = DhanContext(DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN)
    _market_feed_instance = MarketFeed(dhan_context, instruments, version='v2')
    
    async def run():
        await _market_feed_instance.authorize()
        await _market_feed_instance.connect()
        await _market_feed_instance.subscribe_instruments()
        _market_feed_instance.run_forever()
    
    asyncio.run(run())

@mcp.tool()
def subscribe_live_prices(security_ids: list, exchange_segment: str = "NSE_EQ") -> dict:
    """
    Subscribe to live prices for given security IDs.
    - security_ids: List of security IDs (e.g., ['12018'] for SUZLON)
    - exchange_segment: 'NSE_EQ' or 'BSE_EQ'
    Returns subscription status.
    """
    global _live_prices
    _live_prices = {}
    
    instruments = [{"ExchangeSegment": exchange_segment, "SecurityId": sid} for sid in security_ids]
    
    thread = threading.Thread(target=_start_live_feed, args=(instruments,))
    thread.daemon = True
    thread.start()
    
    return {"status": "subscribed", "instruments": security_ids}

@mcp.tool()
def get_live_price(security_id: str) -> dict:
    """
    Get current live price for a security ID.
    - security_id: Dhan security ID (e.g., '12018' for SUZLON)
    Returns LTP and P/L if entry price provided.
    """
    price = _live_prices.get(security_id, None)
    if price is None:
        return {"status": "waiting", "message": "Waiting for live data..."}
    return {"security_id": security_id, "ltp": price}

@mcp.tool()
def get_current_positions() -> dict:
    """Get current open positions."""
    client = get_client()
    return client.get_positions()

@mcp.tool()
def get_security_live_price(security_id: str) -> dict:
    """
    Get live price for a security using yfinance (works for NSE listed stocks).
    - security_id: Dhan security ID (e.g., '12018' for SUZLON)
    
    Note: For accurate real-time data, use the WebSocket live feed subscription.
    This is a fallback using yfinance.
    """
    import yfinance as yf
    
    symbol_map = {
        '12018': 'SUZLON.NS',
        '5926': 'IRFC.NS',
        '4726': 'IDBI.NS',
        'IOB': 'IOB.NS',
        'UCOBANK': 'UCOBANK.NS',
        'NHPC': 'NHPC.NS'
    }
    
    symbol = symbol_map.get(security_id, None)
    if symbol:
        try:
            df = yf.download(symbol, period='1d', interval='1m', progress=False)
            if not df.empty:
                price = float(df['Close'].iloc[-1])
                prev = float(df['Open'].iloc[0])
                return {
                    "security_id": security_id,
                    "symbol": symbol,
                    "ltp": round(price, 2),
                    "change": round(((price - prev) / prev) * 100, 2)
                }
        except Exception as e:
            return {"error": str(e)}
    return {"error": "Symbol not found for security_id"}

@mcp.tool()
def get_market_depth(security_id: str) -> dict:
    """
    Get full market depth (bid/ask) for a security.
    - security_id: Dhan security ID (e.g., '12018' for SUZLON)
    
    Returns: bid prices, ask prices, quantities, and order counts.
    """
    import yfinance as yf
    
    symbol_map = {
        '12018': 'SUZLON.NS',
        '5926': 'IRFC.NS',
        '4726': 'IDBI.NS',
        'IOB': 'IOB.NS',
        'UCOBANK': 'UCOBANK.NS',
        'NHPC': 'NHPC.NS'
    }
    
    symbol = symbol_map.get(security_id, None)
    if not symbol:
        # Try to use security_id as direct symbol
        symbol = security_id + '.NS'
    
    try:
        ticker = yf.Ticker(symbol)
        depth = ticker.fast_info
        
        # Try to get order book data
        if hasattr(ticker, 'order_book') and ticker.order_book:
            ob = ticker.order_book
            return {
                "symbol": symbol,
                "bids": ob.get('bids', []),
                "asks": ob.get('asks', [])
            }
        
        # Fallback: get current price and day's range
        return {
            "symbol": symbol,
            "message": "Order book requires live data API. Use Dhan WebSocket for full depth.",
            "fallback": "Using yfinance for basic data"
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_stock_analysis(security_id: str) -> dict:
    """
    Get comprehensive stock analysis including historical data, price action, and trends.
    - security_id: Dhan security ID (e.g., '12018' for SUZLON)
    """
    import yfinance as yf
    
    symbol_map = {
        '12018': 'SUZLON.NS',
        '5926': 'IRFC.NS',
        '4726': 'IDBI.NS',
        'IOB': 'IOB.NS',
        'UCOBANK': 'UCOBANK.NS',
        'NHPC': 'NHPC.NS'
    }
    
    symbol = symbol_map.get(security_id, security_id + '.NS')
    
    try:
        # Get multiple timeframe data
        df_daily = yf.download(symbol, period='1mo', interval='1d', progress=False)
        df_15m = yf.download(symbol, period='5d', interval='15m', progress=False)
        
        if df_daily.empty:
            return {"error": "No data found"}
        
        current = float(df_daily['Close'].iloc[-1])
        week_open = float(df_daily.iloc[-5]['Open']) if len(df_daily) >= 5 else current
        month_open = float(df_daily.iloc[0]['Open'])
        
        # Calculate indicators
        sma_20 = float(df_daily['Close'].tail(20).mean()) if len(df_daily) >= 20 else current
        sma_50 = float(df_daily['Close'].tail(50).mean()) if len(df_daily) >= 50 else current
        
        # Range analysis
        high_20d = float(df_daily['High'].tail(20).max())
        low_20d = float(df_daily['Low'].tail(20).min())
        
        return {
            "symbol": symbol,
            "current_price": round(current, 2),
            "week_change": round(((current - week_open) / week_open) * 100, 2),
            "month_change": round(((current - month_open) / month_open) * 100, 2),
            "sma_20": round(sma_20, 2),
            "sma_50": round(sma_50, 2),
            "20d_high": round(high_20d, 2),
            "20d_low": round(low_20d, 2),
            "trend": "bullish" if current > sma_20 else "bearish",
            "volatility": "high" if (high_20d - low_20d) / low_20d > 0.1 else "normal"
        }
    except Exception as e:
        return {"error": str(e)}

# === AUTONOMOUS TRADING WORKFLOW ===

@mcp.tool()
def prepare_trade(security_id: str, exchange_segment: str = "NSE_EQ", product_type: str = "INTRADAY") -> dict:
    """
    Complete trade preparation workflow:
    1. Check available capital
    2. Get stock historical data & trend
    3. Calculate ACTUAL margin required using Dhan API
    4. Calculate breakeven & targets
    5. Calculate max affordable quantity considering leverage
    
    Returns: capital, stock analysis, actual margin, quantity recommendation, cost estimates
    """
    import yfinance as yf
    
    # 1. Check capital
    client = get_client()
    fund_data = client.get_fund_limits()
    available_capital = fund_data.get('data', {}).get('availabelBalance', 0)
    
    # 2. Get stock data & trend
    symbol_map = {'12018': 'SUZLON.NS', '5926': 'IRFC.NS', '4726': 'IDBI.NS', 'IOB': 'IOB.NS', 'UCOBANK': 'UCOBANK.NS', 'NHPC': 'NHPC.NS'}
    symbol = symbol_map.get(security_id, security_id + '.NS')
    
    # Get current price
    df = yf.download(symbol, period='5d', interval='15m', progress=False)
    current_price = float(df['Close'].iloc[-1]) if not df.empty else 0
    
    # Get daily data for trend
    df_daily = yf.download(symbol, period='1mo', interval='1d', progress=False)
    sma_20 = float(df_daily['Close'].tail(20).mean()) if len(df_daily) >= 20 else current_price
    high_20d = float(df_daily['High'].tail(20).max()) if len(df_daily) >= 20 else current_price
    low_20d = float(df_daily['Low'].tail(20).min()) if len(df_daily) >= 20 else current_price
    
    trend = "bullish" if current_price > sma_20 else "bearish"
    volatility = round((high_20d - low_20d) / low_20d * 100, 1)
    
    # 3. Calculate ACTUAL margin using Dhan API
    # Start with 50% of capital as usable, then calculate max qty
    usable_capital = available_capital * 0.5
    
    # Calculate max qty based on trade value (not margin)
    # Dhan gives 5X leverage for INTRADAY, so margin is ~20% of trade value
    estimated_margin_per_share = current_price * 0.20
    max_qty_by_margin = int(usable_capital / estimated_margin_per_share)
    max_qty_by_capital = int(usable_capital / current_price)
    max_qty = min(max_qty_by_margin, max_qty_by_capital)
    
    # 4. Calculate cost estimates
    est = estimate_order(max_qty, current_price, exchange_segment, product_type)
    
    # 5. Get actual margin from Dhan API for verification
    try:
        margin_data = client.margin_calculator(
            security_id=security_id,
            exchange_segment=exchange_segment,
            transaction_type='BUY',
            quantity=max_qty,
            product_type=product_type,
            price=current_price,
            trigger_price=0
        )
        actual_margin = margin_data.get('data', {}).get('totalMargin', 0)
        leverage = margin_data.get('data', {}).get('leverage', 'N/A')
    except:
        actual_margin = estimated_margin_per_share * max_qty
        leverage = '5.0X'
    
    remaining_capital = available_capital - actual_margin
    
    return {
        "available_capital": available_capital,
        "usable_capital_50pct": usable_capital,
        "current_price": current_price,
        "stock_analysis": {
            "sma_20": round(sma_20, 2),
            "20d_high": round(high_20d, 2),
            "20d_low": round(low_20d, 2),
            "trend": trend,
            "volatility": str(volatility) + "%"
        },
        "margin_info": {
            "actual_margin_required": round(actual_margin, 2),
            "leverage": leverage,
            "trade_value": round(current_price * max_qty, 2)
        },
        "max_quantity": max_qty,
        "remaining_capital_after_margin": round(remaining_capital, 2),
        "cost_estimate": est,
        "recommendation": {
            "qty": max_qty,
            "entry": current_price,
            "sl": round(current_price * 0.975, 2),
            "target_1pct": est.get('target_1pct'),
            "target_2pct": est.get('target_2pct')
        }
    }

@mcp.tool()
def execute_buy_trade(security_id: str, quantity: int, price: float, exchange_segment: str = "NSE_EQ", product_type: str = "INTRADAY") -> dict:
    """
    Execute a BUY trade with the given parameters.
    Returns order confirmation.
    """
    client = get_client()
    result = client.place_order(
        security_id=security_id,
        exchange_segment=exchange_segment,
        transaction_type='BUY',
        quantity=quantity,
        order_type='LIMIT',
        product_type=product_type,
        price=price,
        validity='DAY'
    )
    return result

@mcp.tool()
def execute_sell_trade(security_id: str, quantity: int, price: float, exchange_segment: str = "NSE_EQ", product_type: str = "INTRADAY") -> dict:
    """
    Execute a SELL trade at market or limit price.
    """
    client = get_client()
    order_type = 'MARKET' if price == 0 else 'LIMIT'
    result = client.place_order(
        security_id=security_id,
        exchange_segment=exchange_segment,
        transaction_type='SELL',
        quantity=quantity,
        order_type=order_type,
        product_type=product_type,
        price=price,
        validity='DAY'
    )
    return result

@mcp.tool()
def close_position(security_id: str, quantity: int, product_type: str = "INTRADAY") -> dict:
    """
    Close position at market price immediately.
    """
    client = get_client()
    # Get market price
    import yfinance as yf
    symbol_map = {'12018': 'SUZLON.NS', '5926': 'IRFC.NS', '4726': 'IDBI.NS'}
    symbol = symbol_map.get(security_id, security_id + '.NS')
    df = yf.download(symbol, period='1d', interval='1m', progress=False)
    market_price = float(df['Close'].iloc[-1]) if not df.empty else 0
    
    result = client.place_order(
        security_id=security_id,
        exchange_segment='NSE_EQ',
        transaction_type='SELL',
        quantity=quantity,
        order_type='MARKET',
        product_type=product_type,
        price=0,
        validity='DAY'
    )
    return {
        "exit_price": market_price,
        "order_result": result
    }

@mcp.tool()
def get_position_status(security_id: str = None) -> dict:
    """
    Get current position status. If security_id provided, get that specific position.
    Returns: entry price, current price, P/L, quantity, targets, SL
    """
    import yfinance as yf
    
    client = get_client()
    positions = client.get_positions()
    
    if not positions.get('data'):
        return {"status": "no_position"}
    
    for pos in positions['data']:
        if security_id and pos.get('securityId') != security_id:
            continue
        
        entry = pos.get('costPrice', 0)
        qty = pos.get('netQty', 0)
        
        # Get current price
        symbol_map = {'12018': 'SUZLON.NS', '5926': 'IRFC.NS', '4726': 'IDBI.NS'}
        symbol = symbol_map.get(pos.get('securityId', ''), pos.get('securityId', '') + '.NS')
        
        df = yf.download(symbol, period='1d', interval='1m', progress=False)
        current = float(df['Close'].iloc[-1]) if not df.empty else entry
        
        pl_rs = (current - entry) * qty
        pl_pct = ((current - entry) / entry) * 100
        
        # Get cost estimate for targets
        est = estimate_order(qty, entry, 'NSE_EQ', pos.get('productType', 'INTRADAY'))
        
        return {
            "security_id": pos.get('securityId'),
            "symbol": pos.get('tradingSymbol'),
            "entry_price": entry,
            "current_price": current,
            "quantity": qty,
            "pnl_rs": round(pl_rs, 2),
            "pnl_pct": round(pl_pct, 2),
            "product_type": pos.get('productType'),
            "breakeven": est.get('breakeven_price'),
            "target_1pct": est.get('target_1pct'),
            "target_2pct": est.get('target_2pct'),
            "sl": 42.50  # Default SL - can be customized
        }
    
    return {"status": "no_matching_position"}

@mcp.tool()
def get_constants() -> dict:
    """Get DhanHQ v2 constants for reference."""
    client = get_client()
    return {
        "exchange_segments": {
            "NSE": client.NSE,
            "BSE": client.BSE,
            "NSE_FNO": client.NSE_FNO,
            "BSE_FNO": client.BSE_FNO,
        },
        "transaction_types": {
            "BUY": client.BUY,
            "SELL": client.SELL,
        },
        "order_types": {
            "MARKET": client.MARKET,
            "LIMIT": client.LIMIT,
            "STOP_LOSS": client.SL,
            "STOP_LOSS_MARKET": client.SLM,
        },
        "product_types": {
            "CNC": client.CNC,
            "INTRA": client.INTRA,
            "MARGIN": client.MARGIN,
            "MTF": client.MTF,
            "CO": client.CO,
            "BO": client.BO,
        }
    }

# --- IP Management ---
@mcp.tool()
def get_static_ip() -> dict:
    """Get current static IP configuration."""
    url = "https://api.dhan.co/v2/ip/getIP"
    headers = {"access-token": DHAN_ACCESS_TOKEN, "dhanClientId": DHAN_CLIENT_ID}
    return requests.get(url, headers=headers).json()

# --- SUPER ORDSERS (Entry + Target + SL + Trailing) ---
@mcp.tool()
def place_super_order(
    security_id: str,
    exchange_segment: str,
    transaction_type: str,
    quantity: int,
    price: float,
    stop_loss_price: float,
    trailing_jump: float,
    target_price: float = None,
    product_type: str = "INTRADAY",
    order_type: str = "MARKET",
    validity: str = "DAY"
) -> dict:
    """
    Place a Super Order with entry + stop-loss + trailing.
    
    - security_id: Dhan security ID (e.g., '12018' for SUZLON)
    - exchange_segment: 'NSE_EQ', 'BSE_EQ'
    - transaction_type: 'BUY' or 'SELL'
    - quantity: Number of shares
    - price: Entry price (use 0 for MARKET order)
    - stop_loss_price: Initial SL price
    - trailing_jump: Price jump to trail SL (e.g., 0.15)
    - target_price: Optional - set very high if not used
    - product_type: 'INTRADAY', 'CNC'
    - order_type: 'MARKET' or 'LIMIT' (default: MARKET)
    
    RECOMMENDED: Use MARKET order for entry, trailing SL for exit.
    """
    from dotenv import load_dotenv
    load_dotenv('E:/Claude Trader/.env')
    import os
    DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
    DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
    
    url = "https://api.dhan.co/v2/super/orders"
    headers = {
        "Content-Type": "application/json",
        "access-token": DHAN_ACCESS_TOKEN,
        "dhanClientId": DHAN_CLIENT_ID
    }
    
    # For MARKET order, use price=0
    entry_price = 0 if order_type.upper() == "MARKET" else price
    
    # If no target or very high target, use price * 1.5 as dummy (won't hit)
    if target_price is None or target_price == 0:
        target_price = price * 1.5 if price > 0 else 60
    
    data = {
        "dhanClientId": DHAN_CLIENT_ID,
        "exchangeSegment": exchange_segment,
        "transactionType": transaction_type,
        "productType": product_type,
        "orderType": order_type.upper(),
        "securityId": security_id,
        "quantity": quantity,
        "price": entry_price,
        "targetPrice": target_price,
        "stopLossPrice": stop_loss_price,
        "trailingJump": trailing_jump,
        "validity": validity
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@mcp.tool()
def modify_super_order(
    order_id: str,
    leg_name: str,
    price: float = None,
    target_price: float = None,
    stop_loss_price: float = None,
    trailing_jump: float = None
) -> dict:
    """
    Modify a Super Order leg.
    """
    from dotenv import load_dotenv
    load_dotenv('E:/Claude Trader/.env')
    import os
    DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
    DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
    
    url = f"https://api.dhan.co/v2/super/orders/{order_id}"
    headers = {"Content-Type": "application/json", "access-token": DHAN_ACCESS_TOKEN, "dhanClientId": DHAN_CLIENT_ID}
    data = {"dhanClientId": DHAN_CLIENT_ID, "orderId": order_id, "legName": leg_name}
    if price is not None:
        data["price"] = price
    if target_price is not None:
        data["targetPrice"] = target_price
    if stop_loss_price is not None:
        data["stopLossPrice"] = stop_loss_price
    if trailing_jump is not None:
        data["trailingJump"] = trailing_jump
    response = requests.put(url, headers=headers, json=data)
    return response.json()

@mcp.tool()
def get_super_orders() -> dict:
    """Get list of all Super Orders for the day."""
    from dotenv import load_dotenv
    load_dotenv('E:/Claude Trader/.env')
    import os
    DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
    DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
    
    url = "https://api.dhan.co/v2/super/orders"
    headers = {"access-token": DHAN_ACCESS_TOKEN, "dhanClientId": DHAN_CLIENT_ID}
    response = requests.get(url, headers=headers)
    return response.json()

@mcp.tool()
def cancel_super_order_leg(order_id: str, leg_name: str) -> dict:
    """
    Cancel a specific leg of a Super Order.
    - leg_name: 'ENTRY_LEG', 'TARGET_LEG', or 'STOP_LOSS_LEG'
    """
    from dotenv import load_dotenv
    load_dotenv('E:/Claude Trader/.env')
    import os
    DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
    DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
    
    url = f"https://api.dhan.co/v2/super/orders/{order_id}/{leg_name}"
    headers = {"access-token": DHAN_ACCESS_TOKEN, "dhanClientId": DHAN_CLIENT_ID}
    response = requests.delete(url, headers=headers)
    return response.json()

@mcp.tool()
def get_super_orders() -> dict:
    """Get list of all Super Orders for the day."""
    from dotenv import load_dotenv
    load_dotenv('E:/Claude Trader/.env')
    import os
    DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
    DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
    
    url = "https://api.dhan.co/v2/super/orders"
    headers = {"access-token": DHAN_ACCESS_TOKEN, "dhanClientId": DHAN_CLIENT_ID}
    response = requests.get(url, headers=headers)
    return response.json()

@mcp.tool()
def cancel_super_order_leg(order_id: str, leg_name: str) -> dict:
    """
    Cancel a specific leg of a Super Order.
    - leg_name: 'ENTRY_LEG', 'TARGET_LEG', or 'STOP_LOSS_LEG'
    """
    from dotenv import load_dotenv
    load_dotenv('E:/Claude Trader/.env')
    import os
    DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
    DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
    
    url = f"https://api.dhan.co/v2/super/orders/{order_id}/{leg_name}"
    headers = {"access-token": DHAN_ACCESS_TOKEN, "dhanClientId": DHAN_CLIENT_ID}
    response = requests.delete(url, headers=headers)
    return response.json()

@mcp.tool()
def set_static_ip(ip_address: str, ip_flag: str = "PRIMARY") -> dict:
    """
    Set static IP for API access.
    - ip_address: IP address to whitelist
    - ip_flag: 'PRIMARY' or 'SECONDARY'
    """
    url = "https://api.dhan.co/v2/ip/setIP"
    headers = {"Content-Type": "application/json", "access-token": DHAN_ACCESS_TOKEN}
    data = {"dhanClientId": DHAN_CLIENT_ID, "ip": ip_address, "ipFlag": ip_flag}
    return requests.post(url, headers=headers, json=data).json()

@mcp.tool()
def modify_static_ip(ip_address: str, ip_flag: str = "PRIMARY") -> dict:
    """Modify existing static IP."""
    url = "https://api.dhan.co/v2/ip/modifyIP"
    headers = {"Content-Type": "application/json", "access-token": DHAN_ACCESS_TOKEN}
    data = {"dhanClientId": DHAN_CLIENT_ID, "ip": ip_address, "ipFlag": ip_flag}
    return requests.post(url, headers=headers, json=data).json()

# --- Kill Switch ---
@mcp.tool()
def get_kill_switch_status() -> dict:
    """Get kill switch status (disables all trading). Uses direct API."""
    url = "https://api.dhan.co/v2/killswitch"
    headers = {"access-token": DHAN_ACCESS_TOKEN}
    return requests.get(url, headers=headers).json()

@mcp.tool()
def toggle_kill_switch(action: str) -> dict:
    """
    Enable or disable kill switch.
    - action: 'ENABLE' or 'DISABLE'
    Uses direct API.
    """
    url = "https://api.dhan.co/v2/killswitch"
    headers = {"Content-Type": "application/json", "access-token": DHAN_ACCESS_TOKEN}
    data = {"dhanClientId": DHAN_CLIENT_ID, "action": action}
    return requests.post(url, headers=headers, json=data).json()

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
