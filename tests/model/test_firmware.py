#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chariot_base` package."""

import pytest

from chariot_base.model import FirmwareUpdateStatus, DataPointFactory, FirmwareUploadException


fixed_message = '{"NMS_52-80-6c-75-c3-fd": {"FirmwareUpload": {"sensorName": "Sensor01", "firmwareStatusCode": 1, "firmwareStatusText": "Firmware Approved"}}}'
fixed_message_rejected = '{"NMS_52-80-6c-75-c3-fd": {"FirmwareUpload": {"sensorName": "Sensor01", "firmwareStatusCode": 0, "firmwareStatusText": "Firmware Rejected"}}}'


@pytest.fixture()
def init_point_factory():
    return DataPointFactory('fog_logs', 'message')


def check_point(point):
    assert point.db == 'fog_logs'
    assert point.table == 'message'
    assert point.timestamp is not None
    assert point.message['sensorName'] == 'Sensor01'
    assert point.message['firmwareStatusCode'] == 1
    assert point.message['firmwareStatusText'] == 'Firmware Approved'


def test_point(init_point_factory):
    point_factory = init_point_factory

    point = point_factory.from_json_string(fixed_message)
    check_point(point[0])

    assert point[0].sensor_id == 'device_52806c75c3fd_Sensor01'

    with pytest.raises(FirmwareUploadException):
        point_factory.from_json_string(fixed_message_rejected)
