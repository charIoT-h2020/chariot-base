#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from chariot_base.utilities.parsing import try_parse, normalize_mac_address


def test_try_parse():
    assert try_parse(4) == 4
    assert try_parse('4') == 4
    assert try_parse('4.2') == 4.2
    assert try_parse('test') == 'test'
    assert try_parse('4e1') == 40.0


def test_normalize_mac_address():
    test_macs = ['52:80:6c:75:c3:fd', '52_80_6c_75_c3_fd', '52-80-6c-75-c3-fd']

    for mac in test_macs:
        assert normalize_mac_address(mac) == '52806c75c3fd'