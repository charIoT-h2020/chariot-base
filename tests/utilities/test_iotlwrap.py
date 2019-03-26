#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest

from chariot_base.utilities.iotlwrap import IoTLWrapper


@pytest.fixture()
async def init_clients():
    OPTS = json.load(open('tests/config.json', 'r'))
    options = OPTS['topology']
    client = IoTLWrapper(options)
    client.load()
    yield client

def test_isSensitive(init_clients):
    client = init_clients

    assert client.isSensitive("CardReader") == True
    assert client.isSensitive("TemperatureSensor1") == False
    assert client.isSensitive("NotFound") == False


def test_pad(init_clients):
    client = init_clients

    assert client.acl("CardReader")[0][0] == 'BMS'

    assert len(client.acl("NotFound")) == 0
