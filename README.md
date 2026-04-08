# DhanHQ Full MCP Server

A comprehensive Model Context Protocol (MCP) server for the DhanHQ v2 API. This server exposes a wide range of tools for trading, portfolio management, and market data analysis directly to AI agents.

## Features

- **Account Tools**: Get profile, fund limits, and balance.
- **Order Management**: Place, modify, and cancel orders (all types & products supported).
- **Portfolio Management**: Real-time positions, holdings, and position conversion.
- **Market Data**: Real-time quotes (LTP, Quote, Full), historical data, and intraday data.
- **Risk Management**: Pre-trade margin calculation.
- **Token Management**: Renew access tokens for 24h validity.

## Installation

### Via Pip (Recommended)

```bash
pip install git+https://github.com/selvarajdevaraj/dhan-mcp.git
```

After installation, you can run the server using:
```bash
dhan-mcp
```

### Locally
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Configure your credentials in a `.env` file (see `.env.example`).

## Usage

Run the server with:
```bash
dhan-mcp
```

## Tools

### Account
- `get_profile()`: Get user profile.
- `get_fund_limits()`: Get account balance and margin.

### Trading
- `place_order(...)`: Place new orders.
- `modify_order(...)`: Modify pending orders.
- `cancel_order(order_id)`: Cancel pending orders.
- `get_order_book()`: Current day's order book.
- `get_trade_book()`: Current day's trade book.

### Portfolio
- `get_holdings()`: Long-term holdings.
- `get_positions()`: Real-time open positions.
- `convert_position(...)`: Convert positions (Intraday to CNC, etc.).

### Market Data
- `get_market_quote(instruments)`: Real-time snapshot for up to 1000 instruments.
- `get_historical_data(...)`: Historical candle data.
- `get_intraday_data(...)`: Minute-level intraday data (last 5 days).

### Utils
- `calculate_margin(...)`: Pre-trade margin calculation.
- `renew_access_token()`: Renew the 24h access token.

## License
MIT
