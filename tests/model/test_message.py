#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chariot_base` package."""

from chariot_base.model import Message


def test_message():
    message = Message('temp:001', 10.40)
    assert (message.sensor_id == 'temp:001')
    assert (message.value == 10.40)
    assert (message.destination is None)


def test_severity_string():
    message = Message('temp:001', 10.40)
    assert(str(message) == '{"id": null, "sensor_id": "temp:001", "value": 10.4, "destination": null, "uber-trace-id": null}')


def test_severity_unicode():
    message = Message('temp:001', 10.40)
    assert(message.__unicode__() == '{"id": null, "sensor_id": "temp:001", "value": 10.4, "destination": null, "uber-trace-id": null}')
