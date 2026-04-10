# DhanHQ Full MCP Server

A comprehensive Model Context Protocol (MCP) server for the DhanHQ v2 API. This server exposes a wide range of tools for trading, portfolio management, and market data analysis directly to AI agents.

## Features

- **Account Tools**: Get profile, fund limits, ledger, and trade history.
- **Order Management**: Place, modify, slice, and cancel orders (all types & products supported).
- **Portfolio Management**: Real-time positions, holdings, and position conversion.
- **Market Data**: Real-time quotes (LTP, OHLC), historical data, intraday data, option chains.
- **Risk Management**: Pre-trade margin calculation, multi-order margin, cost estimation.
- **Advanced Orders**: Super Orders (Entry + TSL + Target), Forever Orders, Slice Orders.
- **Live Price Monitoring**: WebSocket-based live price subscriptions.
- **eDIS**: TPIN generation and electronic delivery instructions.
- **Security**: Kill switch, static IP management.
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
- `get_fund_limits()`: Get account balance and available margin.
- `get_ledger(from_date, to_date)`: Get trading account debit/credit details.
- `get_trade_history(from_date, to_date, page_number)`: Get historical trade data.

### Order Management
- `place_order(...)`: Place new orders (LIMIT, MARKET, STOP_LOSS, STOP_LOSS_MARKET).
- `slice_order(...)`: Slice orders into multiple legs over freeze limit (for F&O).
- `modify_order(...)`: Modify pending orders.
- `cancel_order(order_id)`: Cancel pending orders.
- `get_order_book()`: Current day's order book.
- `get_trade_book(order_id)`: Current day's trade book.
- `get_order_by_id(order_id)`: Get specific order details.
- `get_order_by_correlation_id(correlation_id)`: Get order by correlation ID.
- `get_trades_by_order_id(order_id)`: Get trades for a specific order.

### Portfolio
- `get_holdings()`: Long-term holdings.
- `get_positions()`: Real-time open positions.
- `convert_position(...)`: Convert positions (Intraday to CNC, etc.).
- `exit_all_positions()`: Square off all active positions.
- `get_current_positions()`: Get current open positions.

### Market Data
- `get_market_quote_ltp(securities)`: Get LTP for securities.
- `get_market_quote_ohlc(securities)`: Get OHLC for securities.
- `get_intraday_data(...)`: Minute-level intraday data (last 5 days).
- `get_historical_data(...)`: Historical daily candle data.
- `get_option_chain(under_security_id, under_exchange_segment, expiry)`: Option chain data.
- `get_expired_options_data(...)`: Get expired options historical data.
- `get_market_depth(security_id)`: Get bid/ask market depth.
- `get_stock_analysis(security_id)`: Comprehensive stock analysis with trends.

### Live Price Monitoring
- `subscribe_live_prices(security_ids, exchange_segment)`: Subscribe to live prices via WebSocket.
- `get_live_price(security_id)`: Get current live price.
- `get_security_live_price(security_id)`: Get live price using yfinance fallback.

### Trading Workflow
- `prepare_trade(security_id, exchange_segment, product_type)`: Complete trade prep workflow with margin calculation and targets.
- `execute_buy_trade(...)`: Execute a BUY trade.
- `execute_sell_trade(...)`: Execute a SELL trade.
- `close_position(security_id, quantity, product_type)`: Close position at market price.
- `get_position_status(security_id)`: Get position status with P/L and targets.

### Risk & Utils
- `calculate_margin(...)`: Pre-trade single order margin calculation.
- `calculate_multi_margin(...)`: Calculate margin for multiple orders.
- `estimate_order(...)`: Estimate order costs, breakeven, and target prices.
- `get_constants()`: Get DhanHQ v2 constants for reference.

### Instruments
- `fetch_security_list(segment)`: Get instrument/scrip master list.
- `get_expiry_list(under_security_id, under_exchange_segment)`: Get expiry list for underlying.

### Advanced Orders
- `place_forever_order(...)`: Place a forever order (SINGLE or OCO).
- `place_super_order(...)`: Place Super Order with entry + stop-loss + trailing.
- `modify_super_order(...)`: Modify a Super Order leg.
- `get_super_orders()`: Get list of all Super Orders.
- `cancel_super_order_leg(order_id, leg_name)`: Cancel a Super Order leg.

### eDIS (TPIN)
- `generate_tpin()`: Generate TPIN for eDIS.
- `open_browser_for_tpin(isin, qty, exchange)`: Open browser for TPIN verification.
- `edis_inquiry(isin)`: Get EDIS status and inquiry.

### Auth & Token
- `renew_access_token()`: Renew the 24h access token.

### IP Management
- `get_static_ip()`: Get current static IP configuration.
- `set_static_ip(ip_address, ip_flag)`: Set static IP for API access.
- `modify_static_ip(ip_address, ip_flag)`: Modify existing static IP.

### Security
- `get_kill_switch_status()`: Get kill switch status.
- `toggle_kill_switch(action)`: Enable or disable kill switch.

## License
MIT