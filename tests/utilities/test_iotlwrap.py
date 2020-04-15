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

    assert client.acl('device_52806c75c3fd_Sensor04')['ALLOW'][0] == 'BMS'

    assert client.acl('NotFound') == None


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
    assert client.is_match(private_schema, '{"val": "0000-0000-0000-0000", "val": "1600-0030-0200-1000" }') == True


def test_params(init_clients):
    client = init_clients

    assert client.params('BMS')['pubkey'] == 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlvpBSa4JE87BgBKixnX5qkiB2XcTsJekD3ubtqaWE5WbakkcIvtuHbD0439SFF9HRrj2migJfzPSeWk74cHrBlVWq9jNAQx4HbH2/I5pvDd6jAB+xKrOZ0iQD7Vc8eN7IZBhLgvwsDKZL0s1s7NtosIzjL8BcHTXOZCsmJuccWKYLVSpZ+ffm926kbD5E0lsWhJgDkZ5vtsIed38cTdMJ3oyx9DJy9Jdx2YECHDmm+uQMRoACoNx5L4RdJA280F0amzIhq33wBIKBdwaqrEDKtkTiefGKZnFIpMFp3JWCkvttG4KBxamjH+26GxUmMMQkkqhKUbCtfRHWmmgo40wrwIDAQAB'

    assert len(client.params('NotFound')) == 0


def test_sensor(init_clients):
    client = init_clients

    assert len(client.sensor()) == 4


def test_sync(init_clients):
    client = init_clients

    status = client.sync()
    if status:
        assert len(client.sensor()) == 40
    else:
        assert len(client.sensor()) == 4


def test_expects(init_clients):
    client = init_clients
    assert client.expects('device_52806c75c3fd_Sensor03')[0] == '\\d{4}-\\d{4}-\\d{4}-\\d{4}'
    assert client.expects('device_52806c75c3fd') == []