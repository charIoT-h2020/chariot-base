#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import asyncio
import gmqtt
import logging

from chariot_base.utilities import HealthCheck
from chariot_base.connector import LocalConnector


class HealthDigesterTest(LocalConnector):
    def __init__(self):
        super(LocalConnector, self).__init__()
        self.health = HealthCheck('test_service')
        self.health.inject_connector(self)

    def on_message(self, client, topic, payload, qos, properties):
        self.health.do(payload)


class Callbacks(LocalConnector):

    def __init__(self):
        super().__init__()
        self.messages = []
        self.messagedicts = []
        self.unsubscribeds = []
        self.disconnected = []
        self.publisheds = []
        self.subscribeds = []
        self.connack = None

        self.disconnected = False
        self.connected = False

    def __str__(self):
        return str(self.messages) + str(self.messagedicts) + str(self.publisheds) + \
            str(self.subscribeds) + str(self.unsubscribeds) + \
            str(self.disconnected)

    def on_message(self, client, topic, payload, qos, properties):
        super().on_message(client, topic, payload, qos, properties)
        logging.info('[RECV MSG {}] TOPIC: {} PAYLOAD: {} QOS: {} PROPERTIES: {}'
                     .format(client._client_id, topic, payload, qos, properties))
        self.messages.append((topic, payload, qos, properties))

    def on_subscribe(self, client, mid, qos):
        super().on_subscribe(client, mid, qos)
        logging.info('[SUBSCRIBED {}] QOS: {}'.format(client._client_id, qos))
        self.subscribeds.append(mid)


async def clean_retained(host, port, username, password=None):
    def on_message(client, topic, payload, qos, properties):
        curclient.publish(topic, b"", qos=0, retain=True)

    curclient = gmqtt.Client(
        "clean retained".encode("utf-8"), clean_session=True)

    curclient.set_auth_credentials(username, password)
    curclient.on_message = on_message
    await curclient.connect(host=host, port=port)
    curclient.subscribe("#")
    await asyncio.sleep(10)  # wait for all retained messages to arrive
    await curclient.disconnect()
    time.sleep(.1)


async def cleanup(host, port=1883, username=None, password=None, client_ids=None):
    # clean all client state
    print("clean up starting")
    client_ids = client_ids or ("myclientid", "myclientid2", "myclientid3")

    for clientid in client_ids:
        curclient = gmqtt.Client(clientid.encode("utf-8"), clean_session=True)
        curclient.set_auth_credentials(username=username, password=password)
        await curclient.connect(host=host, port=port)
        time.sleep(.1)
        await curclient.disconnect()
        time.sleep(.1)

    # clean retained messages
    await clean_retained(host, port, username, password=password)
