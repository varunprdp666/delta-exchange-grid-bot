import time
from config import GRID_LOWER, GRID_UPPER, GRID_INTERVAL, TAKE_PROFIT_DOLLARS, STOP_LOSS_DOLLARS, PRICE_CHECK_INTERVAL, MAX_ORDERS_OPEN
from utils import get_market_price, place_order, get_order_quantity

class GridBot:
    def __init__(self):
        self.grid_levels = [x for x in range(GRID_LOWER, GRID_UPPER + GRID_INTERVAL, GRID_INTERVAL)]
        self.open_orders = {}  # key: order_id, value: dict with details

    def calculate_tp_sl(self, price, side):
        if side == "buy":
            tp = round(price + TAKE_PROFIT_DOLLARS, 2)
            sl = round(price - STOP_LOSS_DOLLARS, 2)
        else:
            tp = round(price - TAKE_PROFIT_DOLLARS, 2)
            sl = round(price + STOP_LOSS_DOLLARS, 2)
        return tp, sl

    def place_grid_order(self, side, price):
        size = get_order_quantity(price)
        res = place_order(side, price, size)
        # In production, parse and store order ID, TP and SL here for tracking
        # For demo, just print
        return res

    def run(self):
        print("Starting Grid Bot...")
        while True:
            price = get_market_price()
            if not price:
                print("Error fetching price. Retrying...")
                time.sleep(10)
                continue

            print(f"Current price: ${price}")
            # Simple grid logic - place orders near grid levels
            # Avoid placing too many orders (MAX_ORDERS_OPEN)
            for level in self.grid_levels:
                if abs(price - level) <= GRID_INTERVAL / 2 and len(self.open_orders) < MAX_ORDERS_OPEN:
                    if price < level:
                        print(f"Placing BUY order at {level}")
                        self.place_grid_order("buy", level)
                    else:
                        print(f"Placing SELL order at {level}")
                        self.place_grid_order("sell", level)
            time.sleep(PRICE_CHECK_INTERVAL)

if __name__ == "__main__":
    bot = GridBot()
    bot.run()
