#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chariot_base.model import Alert


def test_default():
    alert = Alert()
    assert alert.message is None
    assert alert.timestamp is not None
    assert alert.severity == 100


def test_message():
    alert = Alert('Message')
    assert(alert.message == 'Message')
    assert(alert.timestamp is not None)
    assert(alert.severity == 100)


def test_severity():
    alert = Alert('Message', 70)
    assert(alert.message == 'Message')
    assert(alert.timestamp is not None)
    assert(alert.severity == 70)


def test_severity_string():
    alert = Alert('Message', 70)
    assert(str(alert) == '{"message": "Message", "severity": 70}')


def test_severity_unicode():
    alert = Alert('Message', 70)
    assert(alert.__unicode__() == '{"message": "Message", "severity": 70}')
