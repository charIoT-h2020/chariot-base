#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest

from chariot_base.datasource import LocalDataSource
from chariot_base.model import DataPointFactory

from ..model.test_point import MqttMessage

OPTS = json.load(open('tests/config.json', 'r'))
options = OPTS['local_storage']
fixed_good_message = '{"52-80-6c-75-c3-fd": {"fixedIO": {"din0": 1}}}'


@pytest.fixture(scope='module')
def init_data_source():
    options['database'] = 'test_db'
    db = LocalDataSource(**options)
    point_factory = DataPointFactory('test_db', 'message')
    yield db,  point_factory
    db.db.drop_database('test_db')


def test_q_write(init_data_source):
    data_source, point_factory = init_data_source

    point = point_factory.from_mqtt_message(MqttMessage('abc/def', fixed_good_message))
    assert data_source.publish(point[0]) is True

    point = point_factory.from_mqtt_message(MqttMessage('abc/def', fixed_good_message))
    assert data_source.publish(point[0]) is True

    logs = data_source.query('SELECT * FROM message', None).get_points('message')

    count = 0
    for item in logs:
        assert item['topic'] == 'abc/def'
        assert item['time'] is not None
        assert item['din0'] in [0, 1]

        count += 1

    assert count == 2
