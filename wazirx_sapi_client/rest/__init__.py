import sys

python_version = sys.version.split(".")

if int(python_version[0]) < 3 or int(python_version[1]) < 7:
    raise BaseException("Python>=3.7 required")

from wazirx_sapi_client.rest.client import Client
