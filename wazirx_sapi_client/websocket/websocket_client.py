"""WazirX websockets"""
import asyncio
import json, sys, os, time
import socket, threading

import websockets

PATH_TO_ADD = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if PATH_TO_ADD not in sys.path:
    sys.path.append(PATH_TO_ADD)
from wazirx_sapi_client.rest import Client


class BaseWebsocketClient:
    """Wazirx Websocket client implementation"""

    def __init__(self, api_key="", secret_key=""):
        """
        Initialize the object.
        Arguments:
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.auth_key = ""
        self.connections = {"websocket": None}
        self.ping_started = False


class WebsocketClient(BaseWebsocketClient):
    def __init__(self, api_key="", secret_key=""):
        super(WebsocketClient, self).__init__(api_key, secret_key)

    def get_auth_token(self):
        rest_client = Client(self.api_key, self.secret_key)
        status_code, response = rest_client.send("create_auth_token",
                                                 {"recvWindow": 10000, "timestamp": int(time.time() * 1000)})
        if status_code == 200:
            self.auth_key = response["auth_key"]
        return self.auth_key

    async def connect(self, uri="wss://stream.wazirx.com/stream"):
        websocket = await websockets.connect(uri=uri)
        self.connections = dict()
        self.connections["websocket"] = websocket
        self.connections["subscriptions"] = []
        _thread = threading.Thread(target=asyncio.run, args=(self.send_heartbeat(),))
        _thread.start()
        while True:
            try:
                message = await websocket.recv()
                if "errorMessage" in message:
                    error = json.loads(message)
                    print(error)
                else:
                    data = json.loads(message)
                    print(data)
            except socket.gaierror:
                print("Socket gaia error")
                return
            except websockets.ConnectionClosedError:
                print("WebSockets connection closed error")
                return
            except websockets.ConnectionClosedOK:
                print("WebSockets connection closed")
                return
            except ConnectionResetError:
                print("Connection reset error")
                return

    async def send_heartbeat(self, *args):
        while True:
            await self.connections["websocket"].send(json.dumps({'event': 'ping'}))
            time.sleep(15 * 60)

    async def disconnect(self):
        if self.connections["websocket"] is not None:
            try:
                await self.connections["websocket"].close()
            except socket.gaierror:
                print("Socket gaia error, let's disconnect anyway...")
            except websockets.ConnectionClosedError:
                print("WebSockets connection closed error, let's disconnect anyway...")
            except websockets.ConnectionClosedOK:
                print("WebSockets connection closed ok, let's disconnect anyway...")
            except ConnectionResetError:
                print("Connection reset error, let's disconnect anyway...")
            del self.connections

    async def _send(self, data: dict) -> None:
        while not self.connections["websocket"]:
            await asyncio.sleep(0.1)
        try:
            await self.connections["websocket"].send(json.dumps(data))
        except socket.gaierror:
            print("Socket gaia error, message not sent...")
        except websockets.ConnectionClosedError:
            print("WebSockets connection closed error, message not sent...")
        except websockets.ConnectionClosedOK:
            print("WebSockets connection closed ok, message not sent...")
        except ConnectionResetError:
            print("Connection reset error, message not sent...")

    async def _sub_unsub(
            self,
            event,
            subscription,
            id=0
    ):
        data = {
            "event": event,
            "streams": subscription,
        }
        if self.auth_key:
            data["auth_key"] = self.auth_key
        if id:
            data["id"] = id

        await self._send(data=data)

    async def subscribe(
            self,
            events=None,
            id=0
    ):
        if events is None:
            events = []
        if all([self.api_key, self.secret_key]) and (not self.auth_key):
            self.get_auth_token()
        await self._sub_unsub(
            event="subscribe",
            subscription=events,
            id=id
        )

    async def unsubscribe(
            self,
            events=[]

    ):
        await self._sub_unsub(
            event="unsubscribe",
            subscription=events,

        )
