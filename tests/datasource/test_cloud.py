#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import json

from chariot_base.datasource import CloudDataSource
from chariot_base.model import DataPointFactory

OPTS = json.load(open('tests/config.json', 'r'))
options = OPTS['cloudant']


@pytest.fixture(scope='module')
def init_data_source():
    db = CloudDataSource(options)
    point_factory = DataPointFactory('test_db', 'message')
    yield db, point_factory


def test_get_last(init_data_source):
    db, point_factory = init_data_source

    point = db.get_last('chariot-sensor')
    assert point['din0'] == 1.0

    point = db.get_last('chariot-sensor', 'sensor-002')
    assert point['din0'] == 1.0

    point = db.get_last('not_exist')
    assert point is None


def test_get_all_databases(init_data_source):
    db, point_factory = init_data_source

    assert len(db.get_all_database()) > 0
