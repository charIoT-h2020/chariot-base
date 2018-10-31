#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

import os
import pytest

from chariot_base.tests import Callbacks, clean_retained, cleanup

host = 'mqtt.flespi.io'
port = 1883
username = os.getenv('USERNAME', 'fake_token')


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
