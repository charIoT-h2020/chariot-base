#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chariot_base` package."""

import pytest

from chariot_base.model import DataPoint, DataPointFactory


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


def test_point(init_point_factory):
    point_factory = init_point_factory

    point = point_factory.from_json_string('{"d": {"din0": 0}}')
    check_point(point)

    point = point_factory.from_json_string('{"d": {"din0": 0}}', 'd')
    check_point(point)

    with pytest.raises(KeyError):
        point_factory.from_json_string('{"d": {"din0": 0}}', 'd1')


def test_mqtt_point(init_point_factory):
    point_factory = init_point_factory

    point = point_factory.from_mqtt_message(MqttMessage('abc/def', '{"d": {"din0": 0}}'))
    check_point(point)
    assert point._event_type() == 'abc.def'


def test_point_event_type(init_point_factory):
    point_factory = init_point_factory
    point = point_factory.from_json_string('{"d": {"din0": 0}}')
    check_point(point)

    assert point._event_type() == ''

    point.topic = 'abc/def'
    assert point._event_type() == 'abc.def'
