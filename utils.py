import time, hmac, hashlib, requests, json
from config import API_KEY, API_SECRET, BASE_URL, PRODUCT_ID, SYMBOL, ORDER_SIZE_USD

def sign_request(method, path, body=""):
    timestamp = str(int(time.time() * 1000))
    message = method + path + timestamp + body
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {
        "api-key": API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }
    return headers

def get_market_price():
    res = requests.get(f"{BASE_URL}/products")
    if res.status_code != 200:
        print("Failed to fetch products")
        return None
    for p in res.json().get("result", []):
        if p["symbol"] == SYMBOL:
            return float(p["spot_price"])
    return None

def get_order_quantity(price, order_size_usd=ORDER_SIZE_USD):
    # Convert USD size to ETH quantity (approx)
    qty = order_size_usd / price
    return round(qty, 6)

def place_order(side, price, size):
    path = "/v2/orders"
    method = "POST"
    body_dict = {
        "product_id": PRODUCT_ID,
        "limit_price": price,
        "size": size,
        "side": side,
        "order_type": "limit",
        "time_in_force": "gtc"
    }
    body = json.dumps(body_dict)
    headers = sign_request(method, path, body)
    res = requests.post(BASE_URL + path, headers=headers, data=body)
    if res.status_code == 200:
        print(f"[{side.upper()}] order placed at ${price} for {size} units.")
    else:
        print(f"Failed to place {side} order at ${price}: {res.text}")
    return res.json()
