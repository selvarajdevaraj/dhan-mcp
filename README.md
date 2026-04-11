# DhanHQ MCP Server

A Model Context Protocol (MCP) server for DhanHQ trading API. Exposes trading tools to AI agents like opencode for autonomous trading.

## Quick Start

### 1. Install

```bash
pip install dhanhq fastmcp python-dotenv yfinance requests
```

### 2. Configure Credentials

Create `.env` file:
```env
DHAN_CLIENT_ID=your_client_id
DHAN_ACCESS_TOKEN=your_access_token
```

### 3. Run Server

```bash
python dhan_mcp.py
```

Or with uv:
```bash
uv run --with dhanhq --with fastmcp --with python-dotenv --with yfinance --with requests python dhan_mcp.py
```

## Available Tools (55+ tools)

### Account
- `get_fund_limits()` - Account balance & margin
- `get_ledger()` - Debit/credit history
- `get_trade_history()` - Historical trades
- `renew_access_token()` - Renew 24h access token

### Order Management
- `place_order()` - Place buy/sell orders
- `slice_order()` - Slice orders over freeze limit (F&O)
- `modify_order()` - Modify pending orders
- `cancel_order()` - Cancel orders
- `get_order_book()` - Today's orders
- `get_trade_book()` - Today's trades
- `get_order_by_id()` - Order details by ID
- `get_order_by_correlation_id()` - Order by correlation ID
- `get_trades_by_order_id()` - Trades for specific order

### Portfolio
- `get_positions()` - Open positions
- `get_holdings()` - Long-term holdings
- `get_current_positions()` - Current positions
- `convert_position()` - Convert intraday to CNC
- `exit_all_positions()` - Square off all positions
- `get_position_status()` - Position P/L & targets

### Market Data
- `get_market_quote_ltp()` - Live prices (LTP)
- `get_market_quote_ohlc()` - OHLC data
- `get_intraday_data()` - Minute-level data
- `get_historical_data()` - Daily candle data
- `get_option_chain()` - Option chain
- `get_expired_options_data()` - Expired options data
- `get_market_depth()` - Bid/ask depth
- `get_stock_analysis()` - Stock analysis with SMA/trend

### Live Price (WebSocket)
- `subscribe_live_prices()` - Subscribe to live prices
- `get_live_price()` - Get subscribed live price
- `get_security_live_price()` - Live price via yfinance

### Trading Workflow
- `prepare_trade()` - Complete trade prep with margin & targets
- `execute_buy_trade()` - Execute BUY order
- `execute_sell_trade()` - Execute SELL order
- `close_position()` - Close at market price

### Risk & Estimation
- `calculate_margin()` - Pre-trade margin
- `calculate_multi_margin()` - Multi-order margin
- `estimate_order()` - Brokerage, breakeven, targets

### Instruments
- `fetch_security_list()` - Scrip master list
- `get_expiry_list()` - Expiry list for underlying
- `get_constants()` - Trading constants

### Super Orders (Advanced)
- `place_super_order()` - Entry + SL + trailing
- `modify_super_order()` - Modify Super Order leg
- `get_super_orders()` - List Super Orders
- `cancel_super_order_leg()` - Cancel Super Order leg

### Forever Orders
- `place_forever_order()` - Forever order (SINGLE/OCO)

### eDIS (TPIN)
- `generate_tpin()` - Generate TPIN
- `open_browser_for_tpin()` - Open browser for TPIN
- `edis_inquiry()` - EDIS status inquiry

### IP & Security
- `get_static_ip()` - Get static IP config
- `set_static_ip()` - Set static IP
- `modify_static_ip()` - Modify static IP
- `get_kill_switch_status()` - Kill switch status
- `toggle_kill_switch()` - Enable/disable kill switch

## Market Timings (IST)

| Event | Time |
|-------|------|
| Market Open | 9:15 AM |
| Market Close | 3:30 PM |
| **Dhan Auto-Square-Off** | **3:19 PM** |
| Weekend | Closed |

**Important**: Close positions by 3:15 PM to avoid auto-square-off charges (₹20+GST).

## Usage with opencode

### Option 1: Using uv (recommended)
```json
{
  "mcp": {
    "dhan": {
      "type": "local",
      "command": ["uv", "run", "--with", "dhanhq", "--with", "fastmcp", "--with", "python-dotenv", "--with", "yfinance", "--with", "requests", "python", "path/to/dhan_mcp.py"],
      "enabled": true
    }
  }
}
```

### Option 2: Using conda
```json
{
  "mcp": {
    "dhan": {
      "type": "local",
      "command": ["conda", "run", "-n", "your_env_name", "python", "path/to/dhan_mcp.py"],
      "enabled": true
    }
  }
}
```

### Option 3: Using virtual env
```json
{
  "mcp": {
    "dhan": {
      "type": "local",
      "command": ["path/to/venv/Scripts/python.exe", "path/to/dhan_mcp.py"],
      "enabled": true
    }
  }
}
```

Replace `your_env_name` with your conda environment name, or `path/to/dhan_mcp.py` with the actual path.

## Security Notes

- Never commit `.env` file with credentials
- Rotate API tokens regularly from Dhan dashboard
- Close positions before 3:15 PM to avoid square-off fees
- Use trailing stop-loss for automated exits

## License

MIT