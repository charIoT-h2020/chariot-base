#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import gmqtt


class LocalConnector(object):
    def __init__(self):
        self.connack = None
        self.client = None

        self.disconnected = False
        self.connected = False

    def clear(self):
        self.__init__()

    def subscribe(self, topic, qos=1):
        self.client.subscribe(topic, qos=qos)

    def publish(self, topic, msg, qos=1):
        self.client.publish(topic, msg, qos=qos)

    def on_message(self, client, topic, payload, qos, properties):
        pass

    def on_subscribe(self, client, mid, qos):
        pass

    def on_disconnect(self, client, packet):
        self.disconnected = True

    def on_connect(self, client, flags, rc, properties):
        self.connected = True
        self.connack = (flags, rc, properties)

    def register_for_client(self, client):
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.on_connect = self.on_connect
        client.on_subscribe = self.on_subscribe

        self.client = client


async def create_client(options, postfix='_client'):
    client_id = '%s%s' % (uuid.uuid4(), postfix)
  
    client = gmqtt.Client(client_id, clean_session=True)
    await client.connect(host=options['host'], port=options['port'], version=4)

    return client