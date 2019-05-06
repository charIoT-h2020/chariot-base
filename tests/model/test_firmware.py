#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chariot_base` package."""

import pytest

from chariot_base.model import FirmwareUpdateStatus, DataPointFactory


fixed_message = '{"NMS_52-80-6c-75-c3-fd": {"fixedIO": {"din0": 1}}}'


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

    # point = point_factory.from_json_string(fixed_good_message)
    # check_point(point[0])
    
    # assert point[0].sensor_id == 'gateway_52806c75c3fd'

    # point = point_factory.from_json_string(wifi_good_message)
    # check_point(point[0])
    # assert point[0].sensor_id == 'device_52806c75c3fd_Sensor01'

    # point = point_factory.from_json_string(ble_good_message)
    # check_point(point[0])
    # assert point[0].message['Temperature'] == 18
    # assert point[0].sensor_id == 'device_52806c75c3fd_Sensor01'

    # with pytest.raises(Exception):
    #     point_factory.from_json_string(bad_message)

    # with pytest.raises(UnAuthenticatedSensor):
    #     point_factory.from_json_string(wifi_un_authenticated_sensor_message)
