#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chariot_base` package."""

import unittest
from chariot_base.model import Subscriber


class AlertTest(unittest.TestCase):

    def test_default(self):
        self.subscriber = Subscriber("subscriber")
        self.assertEqual(self.subscriber.id, "subscriber")

    def test_add_sensor(self):
        self.subscriber = Subscriber("subscriber")
        self.assertEqual(self.subscriber.sensors, set())
        self.subscriber.sensors.add("sensor1")
        self.assertEqual(self.subscriber.sensors, {"sensor1"})

    def test_string(self):
        self.subscriber = Subscriber("subscriber")
        self.assertEqual(str(self.subscriber), '{"id": "subscriber", "sensors": []}')

        self.subscriber.sensors.add("sensor1")
        self.assertEqual(self.subscriber.sensors, {"sensor1"})

        self.assertEqual(str(self.subscriber), '{"id": "subscriber", "sensors": ["sensor1"]}')

    def test_unicode(self):
        self.subscriber = Subscriber("subscriber")
        self.assertEqual(self.subscriber.__unicode__(), '{"id": "subscriber", "sensors": []}')

        self.subscriber.sensors.add("sensor1")
        self.assertEqual(self.subscriber.sensors, {"sensor1"})

        self.assertEqual(str(self.subscriber), '{"id": "subscriber", "sensors": ["sensor1"]}')
