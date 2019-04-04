#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import datetime
import json
import pytest

from chariot_base.connector import LocalConnector, create_client
from chariot_base.tests import HealthDigesterTest, Callbacks, cleanup

OPTS = json.load(open('tests/config.json', 'r'))
options = OPTS['mosquitto']

host = options['host']
port = options['port']
username = options['username']


@pytest.fixture()
async def init_clients():
    await cleanup(host, port, username)

    a_client = await create_client(options)
    callback = HealthDigesterTest()
    callback.register_for_client(a_client)

    b_client = await create_client(options)
    callback2 = Callbacks()
    callback2.register_for_client(b_client)

    yield a_client, callback, b_client, callback2

    await a_client.disconnect()
    await b_client.disconnect()


@pytest.mark.asyncio
async def test_basic(init_clients):
    a_client, callback1, b_client, callback2 = init_clients

    callback1.subscribe('_health', qos=2)
    callback2.subscribe('_health/response', qos=2)

    await asyncio.sleep(1)

    callback2.publish('_health', "{\"destination\": \"_health/response\", \"timestamp\": \"%s\"}" % (datetime.datetime.utcnow().isoformat()))

    await asyncio.sleep(1)
    assert len(callback2.messages) == 1

    callback1.clear()
    callback2.clear()
