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

## Available Tools

### Account
- `get_fund_limits()` - Account balance & margin
- `get_ledger()` - Debit/credit history
- `get_trade_history()` - Historical trades

### Orders
- `place_order()` - Place buy/sell orders
- `modify_order()` - Modify pending orders
- `cancel_order()` - Cancel orders
- `get_order_book()` - Today's orders
- `get_trade_book()` - Today's trades

### Portfolio
- `get_positions()` - Open positions
- `get_holdings()` - Long-term holdings
- `convert_position()` - Convert intraday to CNC

### Market Data
- `get_market_quote_ltp()` - Live prices
- `get_intraday_data()` - Minute data
- `get_historical_data()` - Daily candles
- `get_option_chain()` - Option chains

### Risk & estimation
- `calculate_margin()` - Pre-trade margin
- `estimate_order()` - Brokerage & breakeven

### Advanced Orders
- `place_super_order()` - Entry + SL + trailing

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