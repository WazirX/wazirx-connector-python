import hashlib, collections
import hmac
import json
import os
import urllib

import requests

from wazirx_sapi_client.rest.endpoints import ENDPOINTS

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


class BaseClient(object):
    API_URL = 'https://api.wazirx.com/sapi/'

    def __init__(
            self, api_key="", secret_key=""
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_mapper = json.load(open(PROJECT_ROOT + "/api_mapper.json", "r"))


class Client(BaseClient):
    def __init__(
            self, api_key="", secret_key=""
    ):
        super(Client, self).__init__(api_key, secret_key)

    def send(self, name="", kwargs=None):
        if kwargs is None:
            kwargs = {}
        if not all([name, self.api_mapper.get(name, "")]):
            raise BaseException("Valid Api Name Required")

        api_detail = self.api_mapper[name]
        return self._send_request(api_detail, kwargs)

    def _send_request(self, api_detail, kwargs):
        headers = self._get_headers(api_detail)
        if api_detail.get("client", "") == "signed":
            kwargs = collections.OrderedDict(sorted(kwargs.items(), key=lambda x: x[0]))
            kwargs["signature"] = self._get_signature(api_detail, kwargs)

        request_method = api_detail["action"].lower()
        url = self.API_URL + ENDPOINTS[api_detail["endpoint"]]
        response = None
        if request_method == "get":
            response = requests.get(url, params=kwargs, headers=headers)
        elif request_method == "post":
            response = requests.post(url, data=kwargs, headers=headers)
        elif request_method == "delete":
            response = requests.delete(url, data=kwargs, headers=headers)
        if response is not None:
            return response.status_code, response.json()
        raise BaseException("Invalid Request Type")

    def _get_headers(self, api_detail):
        output = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if api_detail.get("client", "") == "signed":
            output["X-Api-Key"] = self.api_key

        return output

    def _get_signature(self, api_detail, kwargs={}):
        sign_payload = urllib.parse.urlencode(kwargs)
        signature = hmac.new(bytes(self.secret_key, 'latin-1'), msg=bytes(sign_payload, 'latin-1'),
                             digestmod=hashlib.sha256).hexdigest()
        return signature
