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


def test_load(init_clients):
    client = init_clients
    client.load('define SENSOR device_52806c75c3fd_Sensor06 --params { "privacySensitive": 1 }')
    client.load('define SENSOR device_52806c75c3fd_Sensor06 --params { "privacySensitive": 1 }')
    assert client.isSensitive('device_52806c75c3fd_Sensor06') == True


def test_isSensitive(init_clients):
    client = init_clients

    assert client.isSensitive('device_52806c75c3fd_Sensor04') == True
    assert client.isSensitive('device_52806c75c3fd_Sensor01') == False
    assert client.isSensitive('NotFound') == False

    print(client.IoTState.system['ZONE'])


def test_acl(init_clients):
    client = init_clients

    assert client.acl('device_52806c75c3fd_Sensor04')[0][0] == 'BMS'

    assert len(client.acl('NotFound')) == 0


def test_schema(init_clients):
    client = init_clients

    assert len(client.schema()) == 2
    assert len(client.schema(True)) == 1

    assert client.schema(True)[0]["pattern"] == '\\d{4}-\\d{4}-\\d{4}-\\d{4}'


def test_is_match(init_clients):
    client = init_clients

    private_schema = client.schema(True)[0]

    assert client.is_match(private_schema, '0000') == False
    assert client.is_match(private_schema, '0000-0000-0000-0000') == True


def test_params(init_clients):
    client = init_clients

    assert client.params('BMS')['pubkey'] == '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCwusoeNOkZh8gvX7BGEy+rhRxV\nF/ZD11xm0UpzfTR5k/VTasjSyY1yzs2P0BePMUM78cJF21hEBL5fAFCqKpH7zhAj\nl5fFcQd/kZuIlB5ijJAjJhCKV8SK2rwXQXemo9Gc2PHdSg63qjYhEB55dPcClfNw\nCoWsKkKI55WtVjKsDQIDAQAB\n-----END PUBLIC KEY-----'

    assert len(client.params('NotFound')) == 0