import sys

version = sys.version.split(' ')[0].split('.')

if int(version[0]) < 3 or int(version[1]) < 7:
    raise BaseException("Python>=3.7 required")

from wazirx_sapi_client.rest.client import Client
