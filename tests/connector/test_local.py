#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

import os
import uuid
import pytest

from chariot_base.tests import Callbacks, clean_retained, cleanup

host = 'localhost'
port = 1883
username = ''

TOPICS = ("TopicA", "TopicA/B", "TopicA/C", "TopicA/D", "/TopicA")
WILD_TOPICS = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#")
NO_SUBSCRIBE_TOPICS = ("test/nosubscribe",)


@pytest.fixture()
async def init_clients():
    await cleanup(host, port, username)

    a_client = gmqtt.Client('client_%s' % uuid.uuid4(), clean_session=True)
    a_client.set_auth_credentials(username)
    callback = Callbacks()
    callback.register_for_client(a_client)

    b_client = gmqtt.Client('client_%s' % uuid.uuid4(), clean_session=True)
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
    b_client.subscribe(TOPICS[0])
    await asyncio.sleep(1)

    a_client.publish(TOPICS[0], b"qos 0")
    a_client.publish(TOPICS[0], b"qos 1", 1)
    a_client.publish(TOPICS[0], b"qos 2", 2)
    await asyncio.sleep(1)
    assert len(callback2.messages) == 3
