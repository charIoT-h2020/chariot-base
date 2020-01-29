#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest

from chariot_base.model import DataPointFactory
from chariot_base.connector import WatsonConnector

OPTS = json.load(open('tests/config.json', 'r'))
options = OPTS['iot']
fixed_good_message = '{"52-80-6c-75-c3-fd": {"fixedIO": {"din0": 1, "din1": 0}}}'


@pytest.fixture()
async def init_clients():
    options_first = options['client1']

    options_second = options['client2']

    yield WatsonConnector(options_first), WatsonConnector(options_second), DataPointFactory('fog_logs', 'message')


def test_error():
    options_first = {
        "org": "jv8w5u",
        "type": "gateway",
        "id": "fault",
        "auth-method": "token",
        "auth-token": "fault",
    }
    WatsonConnector(options_first)


@pytest.mark.asyncio
async def test_basic(init_clients):
    client1, client2, point_factory = init_clients

    point = point_factory.from_json_string(fixed_good_message)

    assert client1.publish(point[0]) is True
    assert client2.publish(point[0]) is True
