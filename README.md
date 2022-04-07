# Wazirx Python

[![Pyhton](https://img.shields.io/badge/python-3-green)](https://docs.wazirx.com)

This is an official Python wrapper for the Wazirx exchange REST and WebSocket APIs.

##### Notice

We are now at 1.0 and there may be things breaking, don't hesitate to raise an issue if you feel so!

## Installation
Generate **API KEY** and **Secret Key** from Wazirx website [here](https://wazirx.com/settings/keys)

```python
pip3 install -r requirements.txt
```

## Features

#### Current

* Basic implementation of REST API
  * Easy to use authentication
  * Methods return parsed JSON
  * No need to generate timestamps
  * No need to generate signatures
* Basic implementation of WebSocket API
  * Create task using `asyncio` inside async main function
  * Single and multiple streams supported
  * All methods runs with `await` call inside async function

#### Planned

* Exception handling with responses
* High level abstraction

## Getting Started

#### REST Client

Import Wazirx Client for Rest:

```python
from wazirx_sapi_client.rest import Client
```

Create a new instance of the REST Client:

```python
# If you only plan on touching public API endpoints, you can forgo any arguments
client = Client()
# Otherwise provide an api_key and secret_key as keyword arguments
client = Client(api_key='x', secret_key='y')
```

Create various requests:

## General Endpoints

#### Ping

```python
client.send("ping")
```
Response:
```json-doc
{}
```
#### Server time

```python
client.send("time")
```
Response:
```json-doc
{
    "serverTime": 1632375945160
}
```
#### System status

```python
client.send("system_status")
```
Response:
```json-doc
{
    "status": "normal",
    "message": "System is running normally."
}
```
#### Exchange info

```python
client.send("exchange_info")
```
Response:
```json-doc
{
    "timezone": "UTC",
    "serverTime": 1632376074413,
    "symbols": [
        {
            "symbol": "wrxinr",
            "status": "trading",
            "baseAsset": "wrx",
            "quoteAsset": "inr",
            "baseAssetPrecision": 5,
            "quoteAssetPrecision": 0,
            "orderTypes": [
                "limit",
                "stop_limit"
            ],
            "isSpotTradingAllowed": true,
            "filters": [
                {
                    "filterType": "PRICE_FILTER",
                    "minPrice": "1",
                    "tickSize": "1"
                }
            ]
        }
    ]
}
```
#### Create an order
```python
client.send("create_order", {"symbol": 'btcinr', "side": 'buy', "type": 'limit',
  "quantity": 100, "price": 0.00055, "recvWindow": 1000})
```
Response:
```json-doc
{"id"=>27007862, "symbol"=>"btcinr", "type"=>"limit", "side"=>"buy",
"status"=>"wait", "price"=>"210.0", "origQty"=>"2.0", "executedQty"=>"0.0",
"createdTime"=>1632310960000, "updatedTime"=>1632310960000}
```
##### For other api methods follow [this](https://github.com/WazirX/wazirx-connector-python/blob/master/wazirx_sapi_client/rest/api_mapper.json).

##### For example and better understanding the api client usage refer [here](https://github.com/WazirX/wazirx-connector-python/blob/master/wazirx_sapi_client/rest/test.py)

Required and optional parameters, as well as enum values, can be found on the [Wazirx Documentation](https://docs.wazirx.com). Parameters should always be passed to client methods as keyword arguments in snake_case form.

#### WebSocket Client

Import Wazirx Client for WebSocket and [AsyncIO](https://docs.python.org/3/library/asyncio.html)

```python
import asyncio
from wazirx_sapi_client.websocket import WebsocketClient
```

Create a new instance of the REST Client:

```python
# If you only plan on touching public API endpoints, you can forgo any arguments
ws = WebsocketClient()
# Otherwise provide an api_key and secret_key as keyword arguments
ws = WebsocketClient(api_key='x', secret_key='y')
```

Create a connection with the websocket using:

```python
asyncio.create_task(
    ws.connect()
)
```

Create various WebSocket streams with `await`

```python
# Pass the symbol/symbols to subscribe to trades
await ws.trades(symbol=['btcinr','wrxinr'], id=0, action='subscribe')

# Pass the symbol/symbols to subscribe to depth
await ws.depth(symbol=['btcinr','wrxinr'], id=0, action='subscribe')

# For all market tickers
await ws.all_market_ticker(id=0, action='subscribe')
```

##### Note:
* `symbol` can be `Array` for multiple symbols.
* `id` by default is `0`, for unique identification any positive integer can be used.
* `action` only needs to pass in case of `unsubscribe`, default is `subscribe` if no data passed.
#### User Data Stream

User data streams utilize both the REST and WebSocket APIs.

Request a listen key from the REST API, and then create a WebSocket stream using it.

```python
await ws.user_stream(streams=['orderUpdate', 'ownTrade', 'outboundAccountPosition'], id=0, action='subscribe')
```

To make sure that websocket stays live add the given below code for your `main`.

```python
loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
```

##### For other websocket methods follow [this](https://github.com/WazirX/wazirx-connector-python/blob/master/wazirx_sapi_client/websocket/websocket_client.py).

##### For example and better understanding the websocket client usage refer [here](https://github.com/WazirX/wazirx-connector-python/blob/master/wazirx_sapi_client/websocket/test.py)

## Development

After checking out the repo, run `python3 wazirx_sapi_client/rest/test.py` or `python3 wazirx_sapi_client/websocket/test.py` to run the rest apis or websocket tests or experiments respectively.

## Contributing

Bug reports and pull requests are welcome on GitHub at [Issues](https://github.com/WazirX/wazirx-connector-python/issues).

## License

The gem is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
