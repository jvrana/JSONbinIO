import pytest

from jsonbinio import JSONbinIO
from uuid import uuid4
import os
import json


here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, '.secret_key.json')) as f:
    secret = json.load(f)
    jsonbin = JSONbinIO(secret['secret_key'])
    API_TEST_COLLECTION_ID = secret['collection_id']
    BIN_ID = secret['bin_id']


def test_jsonbin_create_then_delete():

    v = str(uuid4())
    r = jsonbin.create({"test": v}, collection_id=API_TEST_COLLECTION_ID)
    rid = r['id']

    d = jsonbin.read(rid)
    assert d == {"test": v}

    d = jsonbin.delete(rid)
    assert d['success']


def test_jsonbin_update():

    v1 = str(uuid4())
    v2 = str(uuid4())
    r = jsonbin.update(BIN_ID, {"test": v1})
    rid = r['id']

    jsonbin.update(rid, {"test2": "ok", "test": v2})

    d = jsonbin.read(rid)
    assert d == {"test2": "ok", "test": v2}


def test_update_with_string():
    v1 = str(uuid4())
    v2 = str(uuid4())
    r = jsonbin.update(BIN_ID, json.dumps({"test": v1}))
    rid = r['id']

    jsonbin.update(rid, {"test2": "ok", "test": v2})

    d = jsonbin.read(rid)
    assert d == {"test2": "ok", "test": v2}


def test_jsonbin_merge():
    v1 = str(uuid4())
    v2 = str(uuid4())
    r = jsonbin.update(BIN_ID, {"test": v1})
    rid = r['id']

    jsonbin.merge(rid, {"foo": v2})

    assert jsonbin.read(rid) == {"foo": v2, "test": v1}


def test_bin():

    v1 = str(uuid4())
    v2 = str(uuid4())
    bin = jsonbin.create_bin({"test": v1}, collection_id=API_TEST_COLLECTION_ID)

    assert bin.read() == {"test": v1}
    bin.update({"test": v2})
    assert bin.read() == {"test": v2}

    bin.delete()


def test_should_raise_ValueError():

    with pytest.raises(ValueError):
        jsonbin.create_bin("this is not a json")