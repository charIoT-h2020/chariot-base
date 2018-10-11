#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chariot_base` package."""

import unittest
from chariot_base.model import Alert


class AlertTest(unittest.TestCase):

    def test_default(self):
        self.alert = Alert()
        self.assertEqual(self.alert.message, None)
        self.assertNotEqual(self.alert.timestamp, None)
        self.assertEqual(self.alert.severity, 100)

    def test_message(self):
        self.alert = Alert('Message')
        self.assertEqual(self.alert.message, 'Message')
        self.assertNotEqual(self.alert.timestamp, None)
        self.assertEqual(self.alert.severity, 100)

    def test_severity(self):
        self.alert = Alert('Message', 70)
        self.assertEqual(self.alert.message, 'Message')
        self.assertNotEqual(self.alert.timestamp, None)
        self.assertEqual(self.alert.severity, 70)

    def test_severity_string(self):
        self.alert = Alert('Message', 70)
        self.assertEqual(str(self.alert), '{"message": "Message", "severity": 70}')

    def test_severity_unicode(self):
        self.alert = Alert('Message', 70)
        self.assertEqual(self.alert.__unicode__(), '{"message": "Message", "severity": 70}')
