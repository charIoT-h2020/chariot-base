#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chariot_base` package."""

import pytest

from chariot_base.model import DataPointFactory


fixed_good_message = '{"52-80-6c-75-c3-fd": {"fixedIO": {"din0": 1}}}'
wifi_good_message = '{"52-80-6c-75-c3-fd": {"wifi": {"wifiStatusCode": 0, "wifiStatusText": "Wifi online", "sensorData": {"sensorName": "Sensor01","sensorStatusCode": 0,"sensorStatusText": "Sensor online","sensorValues": [{"name": "din0","value": "1"}]}}}}'
bad_message = '{"52-80-6c-75-c3-fd": {"din0": 1}}'

class MqttMessage:
    def __init__(self, topic, message):
        self.topic = topic
        self.payload = message.encode('utf-8')


@pytest.fixture()
def init_point_factory():
    return DataPointFactory('fog_logs', 'message')


def check_point(point):
    assert point.db == 'fog_logs'
    assert point.table == 'message'
    assert point.timestamp is not None
    assert str(point.message['din0']) == '1'


def test_point(init_point_factory):
    point_factory = init_point_factory

    point = point_factory.from_json_string(fixed_good_message)
    check_point(point)

    point = point_factory.from_json_string(wifi_good_message)
    check_point(point)

    with pytest.raises(Exception):
        point_factory.from_json_string(bad_message)


def test_mqtt_point(init_point_factory):
    point_factory = init_point_factory

    point = point_factory.from_mqtt_message(MqttMessage('abc/def', fixed_good_message))
    check_point(point)
    assert point._event_type() == 'abc.def'

    with pytest.raises(Exception):
        point_factory.from_mqtt_message(MqttMessage('abc/def', bad_message))


def test_point_event_type(init_point_factory):
    point_factory = init_point_factory
    point = point_factory.from_json_string(fixed_good_message)
    check_point(point)

    assert point._event_type() == ''

    point.topic = 'abc/def'
    assert point._event_type() == 'abc.def'
