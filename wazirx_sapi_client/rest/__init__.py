import sys

if int(sys.version[0]) < 3 or int(sys.version[2]) < 7:
    raise BaseException("Python>=3.7 required")

from wazirx_sapi_client.rest.client import Client
