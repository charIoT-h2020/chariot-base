#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from chariot_base.utilities.parsing import try_parse


def test_try_parse():
    assert try_parse(4) == 4
    assert try_parse("4") == 4
    assert try_parse("4.2") == 4.2
    assert try_parse("test") == "test"
    assert try_parse("4e1") == 40.0
