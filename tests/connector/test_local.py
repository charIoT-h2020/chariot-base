#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import gmqtt
import pytest

from chariot_base.connector import create_client
from chariot_base.tests import Callbacks, cleanup

OPTS = json.load(open('tests/config.json', 'r'))
options = OPTS['mosquitto']

host = options['host']
port = options['port']
username = options['username']

TOPICS = ("TopicA", "TopicA/B", "TopicA/C", "TopicA/D", "/TopicA")
WILDTOPICS = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#")
NOSUBSCRIBE_TOPICS = ("test/nosubscribe",)


@pytest.fixture()
async def init_clients():
    await cleanup(host, port, username)

    a_client = gmqtt.Client("myclientid", clean_session=True)
    a_client.set_auth_credentials(username)
    callback = Callbacks()
    callback.register_for_client(a_client)

    b_client = gmqtt.Client("myclientid2", clean_session=True)
    b_client.set_auth_credentials(username)
    callback2 = Callbacks()
    callback2.register_for_client(b_client)

    yield a_client, callback, b_client, callback2

    await a_client.disconnect()
    await b_client.disconnect()


@pytest.mark.asyncio
async def test_basic(init_clients):
    a_client, callback, b_client, callback2 = init_clients

    await a_client.connect(host=host, port=port, version=4)
    await b_client.connect(host=host, port=port, version=4)

    c_client = await create_client(options)

    callback2.subscribe(TOPICS[0], qos=2)

    await asyncio.sleep(1)

    callback.publish(TOPICS[0], b"qos 0")
    callback.publish(TOPICS[0], b"qos 1", qos=1)
    # a_client.publish(TOPICS[0], b"qos 2", qos=2) # Mosquitto error
    await asyncio.sleep(1)
    assert len(callback2.messages) == 2

    callback.clear()
    callback2.clear()
