#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chariot_base` package."""

import pytest

from chariot_base.model import DataPointFactory, UnAuthenticatedSensor


fixed_good_message = '{"52-80-6c-75-c3-fd": {"fixedIO": {"din0": 1}}}'
wifi_good_message = '{"52-80-6c-75-c3-fd": {"wifi": {"wifiStatusCode": 0, "wifiStatusText": "Wifi online", "sensorData": {"sensorName": "Sensor01","sensorStatusCode": 0,"sensorStatusText": "Sensor online","sensorValues": [{"name": "din0","value": "1"}]}}}}'
wifi_un_authenticated_sensor_message = '{"52-80-6c-75-c3-fd": {"wifi": {"wifiStatusCode": 0, "wifiStatusText": "Wifi online", "sensorData": {"sensorName": "Sensor01","sensorStatusCode": 2,"sensorStatusText": "Sensor without authentication"}}}}'
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
    assert point.message['din0'] == 1


def test_point(init_point_factory):
    point_factory = init_point_factory

    point = point_factory.from_json_string(fixed_good_message)
    check_point(point[0])
    
    assert point[0].sensor_id == 'gateway_52806c75c3fd'

    point = point_factory.from_json_string(wifi_good_message)
    check_point(point[0])
    assert point[0].sensor_id == 'device_52806c75c3fd_Sensor01'

    with pytest.raises(Exception):
        point_factory.from_json_string(bad_message)

    with pytest.raises(UnAuthenticatedSensor):
        point_factory.from_json_string(wifi_un_authenticated_sensor_message)


def test_mqtt_point(init_point_factory):
    point_factory = init_point_factory

    point = point_factory.from_mqtt_message(MqttMessage('abc/def', fixed_good_message))
    check_point(point[0])
    assert point[0]._event_type() == 'abc.def'

    with pytest.raises(Exception):
        point_factory.from_mqtt_message(MqttMessage('abc/def', bad_message))


def test_point_event_type(init_point_factory):
    point_factory = init_point_factory
    point = point_factory.from_json_string(fixed_good_message)
    check_point(point[0])

    assert point[0]._event_type() == ''

    point[0].topic = 'abc/def'
    assert point[0]._event_type() == 'abc.def'
