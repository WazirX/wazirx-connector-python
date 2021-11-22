import sys

if int(sys.version[0]) < 3 or int(sys.version[2]) < 7:
    raise BaseException("Python>=3.7 required")

from .websocket_client import WebsocketClient
