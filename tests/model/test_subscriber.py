#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chariot_base.model import Subscriber


def test_default():
    subscriber = Subscriber("subscriber")
    assert(subscriber.id == "subscriber")


def test_add_sensor():
    subscriber = Subscriber("subscriber")
    assert(subscriber.sensors == set())
    subscriber.sensors.add("sensor1")
    assert(subscriber.sensors == {"sensor1"})


def test_string():
    subscriber = Subscriber("subscriber")
    assert(str(subscriber) == '{"id": "subscriber", "sensors": []}')

    subscriber.sensors.add("sensor1")
    assert(subscriber.sensors == {"sensor1"})

    assert(str(subscriber) == '{"id": "subscriber", "sensors": ["sensor1"]}')


def test_unicode():
    subscriber = Subscriber("subscriber")
    assert(subscriber.__unicode__() == '{"id": "subscriber", "sensors": []}')

    subscriber.sensors.add("sensor1")
    assert(subscriber.sensors == {"sensor1"})

    assert(str(subscriber) == '{"id": "subscriber", "sensors": ["sensor1"]}')
