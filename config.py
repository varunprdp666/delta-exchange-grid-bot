import os

API_KEY = os.getenv("DELTA_API_KEY")
API_SECRET = os.getenv("DELTA_API_SECRET")

BASE_URL = "https://api.testnet.delta.exchange"

SYMBOL = "ETHUSDT"
PRODUCT_ID = 4  # ETHUSDT perpetual on testnet

CAPITAL_USD = 200.0  # Total capital available for trading

GRID_LOWER = 2800
GRID_UPPER = 3000
GRID_INTERVAL = 20  # $20 grid intervals

ORDER_SIZE_USD = 10  # $ amount per order size (will convert to ETH qty)

TAKE_PROFIT_DOLLARS = 10  # Target profit per trade ($10)
STOP_LOSS_DOLLARS = 5     # Max loss per trade ($5)

MAX_ORDERS_OPEN = 5  # Max open orders at once

PRICE_CHECK_INTERVAL = 20  # seconds between price checks
