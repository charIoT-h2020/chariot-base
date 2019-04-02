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

    assert client.isSensitive("device_52806c75c3fd_Sensor04") == True
    assert client.isSensitive("device_52806c75c3fd_Sensor01") == False
    assert client.isSensitive("NotFound") == False

    print(client.IoTState.system['ZONE'])


def test_pad(init_clients):
    client = init_clients

    assert client.acl("device_52806c75c3fd_Sensor04")[0][0] == 'BMS'

    assert len(client.acl("NotFound")) == 0
