import os
import sys
import time

PATH_TO_ADD = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if PATH_TO_ADD not in sys.path:
    sys.path.append(PATH_TO_ADD)

from wazirx_sapi_client.rest import Client

# Keys for private events
api_key = "test_api_key"
secret_key = "test_secret_key"

# public
c = Client()
print(c.send("ping"))
print(c.send("time"))
print(c.send("system_status"))
print(c.send("exchange_info"))

# private
c = Client(api_key=api_key, secret_key=secret_key)
print(c.send("historical_trades",
             {"limit": 10, "symbol": "btcinr", "recvWindow": 10000, "timestamp": int(time.time() * 1000)}
             ))
print(c.send('create_order',
             {"symbol": "btcinr", "side": "buy", "type": "limit", "price": 500, "quantity": 1, "recvWindow": 10000,
              "timestamp": int(time.time() * 1000)}))
