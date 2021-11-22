import sys

version = sys.version.split(' ')[0]
py_mode, py_version, py_sub_version = version.split('.')
if int(py_mode) < 3 or int(py_version) < 7:
    raise BaseException("Python>=3.7 required")

from .client import Client
