=================================
Welcome to python-wazirx v1.0.0
=================================

Updated 21th Sept 2021

.. image:: https://img.shields.io/badge/python-3-green

This is a Python3 wrapper for the `WazirX <https://wazirx.com>`__ public apis and websocket client integration.


Documentation
  https://docs.wazirx.com/

Features
--------

- Rest Public Apis
- Websocket Client implementation



Quick Start
-----------

    `Register an account with WazirX <https://wazirx.com/signup?source=menubar>`_.

    Generate Api Key and Secret Key and assign relevant permissions.

- You can install packages required for this project using pip3.

.. code::

    pip3 install -r requirements.txt

- Public Apis Example

.. code::

    from wazirx_sapi_client.rest import Client

    # public
    client = Client()
    print(client.send("ping"))
    print(client.send("time"))
    print(client.send("system_status"))
    print(client.send("exchange_info"))

    # private
    api_key = "test_api_key"
    secret_key = "test_secret_key"

    client = Client(api_key=api_key, secret_key=secret_key)

    print(client.send("historical_trades",
                 {"limit": 10, "symbol": "btcinr", "recvWindow": 10000, "timestamp": int(time.time() * 1000)}
                 ))

    print(client.send('create_order',
                 {"symbol": "btcinr", "side": "buy", "type": "limit", "price": 500, "quantity": 1, "recvWindow": 10000,
                  "timestamp": int(time.time() * 1000)}))



- Websocket Client Example

.. code::

    """
    For public streams, api_key and secret_key is not required i.e.
        ws_client = WebsocketClient()
    For private streams, api_key, secret_key are required while initialising WebsocketClient i.e.
        ws_client = WebsocketClient(api_key=api_key, secret_key=secret_key)

    """

    from wazirx_sapi_client.websocket import WebsocketClient

    api_key, secret_key = "test_api_key", "test_secret_key"
    ws_client = WebsocketClient(api_key=api_key, secret_key=secret_key)

    asyncio.create_task(
        ws_client.connect(
        )
    )

    # to subscribe
    await ws_client.subscribe(
        events=["btcinr@depth"],
    )

    await ws_client.subscribe(
        events=["wrxinr@depth"],
        id=1  # id param not mandatory
    )

    await ws_client.subscribe(
        events=["orderUpdate"]
    )

    await ws_client.subscribe(
        events=["outboundAccountPosition"],
        id=2  # id param not mandatory
    )

    ### to unsubscribe
    #await ws_client.unsubscribe(
    #    events=["outboundAccountPosition", "wrxinr@depth"],
    #)

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()


Note: For more rest apis, you can refer rest/endpoints.py file above and WazirX's official public-endpoints documentation.

Compatibility
    python 3.7 and above.