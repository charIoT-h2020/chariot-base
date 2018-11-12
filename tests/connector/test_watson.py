#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from chariot_base.model import DataPointFactory
from chariot_base.connector import WatsonConnector


@pytest.fixture()
async def init_clients():
    options_first = {
        "org": "jv8w5u",
        "type": "gateway",
        "id": "testing",
        "auth-method": "token",
        "auth-token": "Q(lB@aTQ+hm@AVrdw!",
    }

    options_second = {
        "org": "jv8w5u",
        "type": "gateway",
        "id": "5410ec4d1601",
        "auth-method": "token",
        "auth-token": "Mw35yK?VRvsb-Qqjy3"
    }

    yield WatsonConnector(options_first), WatsonConnector(options_second), DataPointFactory('fog_logs', 'message')


def test_error():
    options_first = {
        "org": "jv8w5u",
        "type": "gateway",
        "id": "testing",
        "auth-method": "token",
        "auth-token": "fault",
    }
    WatsonConnector(options_first)


@pytest.mark.asyncio
async def test_basic(init_clients):
    client1, client2, point_factory = init_clients

    point = point_factory.from_json_string('{"d": {"din0": 0, "din1": 1}}', 'd')

    assert client1.publish(point) is True
    assert client2.publish(point) is True
