#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest

from chariot_base.utilities import open_config_file


def test_open_config_file():
    with pytest.raises(Exception):
        opts = open_config_file(['not_found.json'])