#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from chariot_base.datasource import CloudDataSource
from chariot_base.model import DataPointFactory

options = {
    "apikey": "vjg5C8qxZGMooDKoWF68u5omPT5rYEGfOSc91aCoZXjC",
    "username": "56aa8c21-34f5-4e63-bf88-cf1ed1f94442-bluemix",
    "orgId": "jv8w5u"
}


@pytest.fixture(scope='module')
def init_data_source():
    db = CloudDataSource(options)
    point_factory = DataPointFactory('test_db', 'message')
    yield db, point_factory


def test_get_last(init_data_source):
    db, point_factory = init_data_source

    point = db.get_last('gateway')
    assert point['din0'] == 0.0
    assert point['din1'] == 1.0

    point = db.get_last('gateway', '5410ec4d1601')
    assert point['din0'] == 0.0
    assert point['din1'] == 1.0

    point = db.get_last('not_exist')
    assert point is None
