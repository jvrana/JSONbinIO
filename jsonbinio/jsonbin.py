"""
wrapper for JSONBinIO
"""

import requests
from functools import wraps
import logging
import json

logger = logging.getLogger('JSONBin_logger')
logger.setLevel(logging.INFO)


class RequestDecorator(object):
    """
    Wraps a function to raise error with unexpected request status codes
    """
    def __init__(self, status_codes):
        if not isinstance(status_codes, list):
            status_codes = [status_codes]
        self.code = status_codes

    def __call__(self, f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            r = f(*args, **kwargs)
            if r.status_code not in self.code:
                http_codes = {
                    400: "BAD REQUEST",
                    403: "FORBIDDEN",
                    404: "NOT FOUND",
                    500: "INTERNAL SERVER ERROR",
                    503: "SERVICE UNAVAILABLE",
                    504: "SERVER TIMEOUT"}
                msg = ""
                if r.status_code in http_codes:
                    msg = http_codes[r.status_code]
                    msg += f"\nrequest: {r.request}"
                    msg += f"\nurl: {r.request.path_url}"
                    msg += f"\nresponse: {r.text}"
                raise Exception("HTTP Response Failed {} {}".format(
                    r.status_code, msg))
            return r.json()

        return wrapped_f


class JSONBin(object):

    def __init__(self, bin_id, binio):
        self.bin_id = bin_id
        self.jsonbinio = binio

    def read(self):
        return self.jsonbinio.read(self.bin_id)

    def update(self, data):
        return self.jsonbinio.update(self.bin_id, data)

    def delete(self):
        return self.jsonbinio.delete(self.bin_id)

    def merge(self, data):
        return self.jsonbinio.merge(self.bin_id, data)

    def update_from_json(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return self.update(data)

    def merge_from_json(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return self.merge(data)


class JSONBinIO(object):

    home = "https://api.jsonbin.io"

    def __init__(self, secret_key):
        self.headers = {
            'secret-key': secret_key
        }
        self.bin_ids = []

    @staticmethod
    def to_json(data):
        if isinstance(data, str):
            return json.loads(data)
        elif isinstance(data, list) or isinstance(data, dict):
            return data
        else:
            raise ValueError("Data must be a json serializable object,"
                             " but found a {}".format(data.__class__.__name__))

    @RequestDecorator([200])
    def create(self, data, collection_id=None, private=None):
        data = self.to_json(data)
        headers = dict(self.headers)
        headers['Content-Type'] = 'application/json'
        if collection_id is not None:
            headers['collection-id'] = collection_id
        if private is not None:
            headers['private'] = private
        route = self.home + "/b"
        print("CREATE {}".format(route))
        return requests.post(route, json=data, headers=headers)

    @RequestDecorator([200])
    def read(self, bin_id, bin_version=None):
        route = self.home + "/b/{}/latest".format(bin_id)
        if bin_version is not None:
            route += "/{}/latest".format(bin_version)
        print("READ {}".format(route))
        return requests.get(route, headers=self.headers)

    @RequestDecorator([200])
    def update(self, bin_id, data):
        data = self.to_json(data)
        headers = dict(self.headers)
        headers['Content-Type'] = 'application/json'
        headers['versioning'] = "false"
        route = "{}/b/{}".format(self.home, bin_id)
        print("PUT {}".format(route))
        return requests.put(route, json=data, headers=headers)

    def merge(self, bin_id, data):
        data = self.to_json(data)
        new_data = self.read(bin_id)
        new_data.update(data)
        return self.update(bin_id, new_data)

    @RequestDecorator([200])
    def delete(self, bin_id):
        route = "{}/b/{}".format(self.home, bin_id)
        print("DELETE {}".format(route))
        return requests.delete(route, json=None, headers=self.headers)

    def bin(self, bin_id):
        return JSONBin(bin_id, self)

    def create_bin(self, data, collection_id=None, private=None):
        result = self.create(data, collection_id=collection_id, private=private)
        return self.bin(result['id'])


