#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chariot_base.model import Alert


def test_default():
    alert = Alert('topology')
    assert alert.message is None
    assert alert.sensor_id is None
    assert alert.timestamp is not None
    assert alert.severity == 100


def test_message():
    alert = Alert('topology', 'Message')
    assert(alert.message == 'Message')
    assert(alert.timestamp is not None)
    assert(alert.severity == 100)


def test_severity():
    alert = Alert('topology', 'Message', 70)
    assert(alert.message == 'Message')
    assert(alert.timestamp is not None)
    assert(alert.severity == 70)
    
    alert.sensor_id = "SmartCard"
    assert alert.sensor_id == "SmartCard"


def test_severity_string():
    alert = Alert('topology', 'Message', 70)
    alert.timestamp = '2019-02-25T16:03:33.474156'
    assert(str(alert) == '{"name": "topology", "sensor_id": null, "message": "Message", "severity": 70, "timestamp": "2019-02-25T16:03:33.474156"}')


def test_severity_unicode():
    alert = Alert('topology', 'Message', 70)
    alert.timestamp = '2019-02-25T16:03:33.474156'
    assert(alert.__unicode__() == '{"name": "topology", "sensor_id": null, "message": "Message", "severity": 70, "timestamp": "2019-02-25T16:03:33.474156"}')
