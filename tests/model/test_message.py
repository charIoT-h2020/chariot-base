#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chariot_base` package."""

import unittest
from chariot_base.model import Message


class MessageTest(unittest.TestCase):

    def test_message(self):
        self.message = Message('temp:001', 10.40)
        self.assertEqual(self.message.sensor_id, 'temp:001')
        self.assertEqual(self.message.value, 10.40)
        self.assertEqual(self.message.destination, None)

    def test_severity_string(self):
        self.message = Message('temp:001', 10.40)
        self.assertEqual(str(self.message), '{"sensor_id": "temp:001", "value": 10.4, "destination": null}')

    def test_severity_unicode(self):
        self.message = Message('temp:001', 10.40)
        self.assertEqual(self.message.__unicode__(), '{"sensor_id": "temp:001", "value": 10.4, "destination": null}')
