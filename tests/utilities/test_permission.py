#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chariot_base.utilities import has_write_right, has_read_right


def test_has_write_right():
    assert has_read_right(4) is False
    assert has_read_right(3) is True
    assert has_read_right(2) is True
    assert has_read_right(1) is False


def test_has_read_right():
    assert has_write_right(4) is False
    assert has_write_right(3) is True
    assert has_write_right(2) is False
    assert has_write_right(1) is True
