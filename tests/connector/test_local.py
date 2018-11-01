#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

import os
import gmqtt
import uuid
import pytest

from chariot_base.tests import Callbacks, clean_retained, cleanup

host = 'iot.eclipse.org'
port = 1883
username = ''

TOPICS = ("TopicA", "TopicA/B", "TopicA/C", "TopicA/D", "/TopicA")
WILDTOPICS = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#")
NOSUBSCRIBE_TOPICS = ("test/nosubscribe",)


@pytest.fixture()
async def init_clients():
    await cleanup(host, port, username)

    aclient = gmqtt.Client("myclientid", clean_session=True)
    aclient.set_auth_credentials(username)
    callback = Callbacks()
    callback.register_for_client(aclient)

    bclient = gmqtt.Client("myclientid2", clean_session=True)
    bclient.set_auth_credentials(username)
    callback2 = Callbacks()
    callback2.register_for_client(bclient)

    yield aclient, callback, bclient, callback2

    await aclient.disconnect()
    await bclient.disconnect()


@pytest.mark.asyncio
async def test_basic(init_clients):
    aclient, callback, bclient, callback2 = init_clients

    await aclient.connect(host=host, port=port, version=4)
    await bclient.connect(host=host, port=port, version=4)
    bclient.subscribe(TOPICS[0], qos=2)
    await asyncio.sleep(1)

    aclient.publish(TOPICS[0], b"qos 0")
    aclient.publish(TOPICS[0], b"qos 1", qos=1)
    # aclient.publish(TOPICS[0], b"qos 2", qos=2) # Mosquitto error
    await asyncio.sleep(1)
    assert len(callback2.messages) == 2
