import asyncio
import sys, os

PATH_TO_ADD = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if PATH_TO_ADD not in sys.path:
    sys.path.append(PATH_TO_ADD)

from wazirx_sapi_client.websocket import WebsocketClient


async def main():
    """
    For public streams, api_key,secret_key is not required i.e.
        ws_client = WebsocketClient()
    For private streams, api_key, secret_key are required while initialising WebsocketClient i.e.
        ws_client = WebsocketClient(api_key=api_key, secret_key=secret_key)

    """
    # Keys for private events
    api_key = "test_api_key"
    secret_key = "test_secret_key"

    ws_client = WebsocketClient(api_key=api_key, secret_key=secret_key)

    asyncio.create_task(
        ws_client.connect(
        )
    )

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
    # await ws_client.unsubscribe(
    #     events=["outboundAccountPosition", "wrxinr@depth"],
    # )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
