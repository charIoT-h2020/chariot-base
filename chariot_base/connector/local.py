#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import gmqtt
from gmqtt.mqtt.constants import MQTTv311
import logging
from ..utilities import Traceable


class LocalConnector(Traceable):
    """
    All subscribers/publisers at Chariot project should extend this class
    """
    def __init__(self):
        self.connack = None
        self.client = None
        self.tracer = None

        self.disconnected = False
        self.connected = False

    def clear(self):
        """
        Reinitialize the connector
        """
        self.__init__()

    def subscribe(self, topic, qos=1):
        """
        Subscribe to a topic

        :param topic: Which topic the subscriber should listen for new message.
        :param qos: MQTT broker quality of service
        """
        self.client.subscribe(topic, qos=qos)

    def publish(self, topic, msg, qos=1):
        """
        Publish to a topic

        :param msg: the published message
        :param qos: MQTT broker quality of service
        """
        self.client.publish(topic, msg, qos=qos)

    def on_message(self, client, topic, payload, qos, properties=None):
        """
        Handler for new message

        :param client: the subscribed MQTT client
        :param topic: the MQTT topic
        :param payload: the message
        :param qos: MQTT broker quality of service
        :param properties: Custom properties
        """

    def on_subscribe(self, client, mid, qos, properties=None):
        """
        The handler run when the client subscribed to a new topic

        :param client: the subscribed MQTT client
        :param mid:
        :param qos: MQTT broker quality of service
        """
        # in order to check if all the subscriptions were successful, we should first get all subscriptions with this
        # particular mid (from one subscription request)
        subscriptions = client.get_subscriptions_by_mid(mid)
        for subscription, granted_qos in zip(subscriptions, qos):
            # in case of bad suback code, we can resend  subscription
            if granted_qos >= gmqtt.constants.SubAckReasonCode.UNSPECIFIED_ERROR.value:
                logging.warning('[RETRYING SUB {}] mid {}, reason code: {}, properties {}'.format(
                                client._client_id, mid, granted_qos, properties))
                client.resubscribe(subscription)
            logging.info('[SUBSCRIBED {}] mid {}, QOS: {}, properties {}'.format(
                client._client_id, mid, granted_qos, properties))

    def on_disconnect(self, client, packet):
        """
        The handler run when the connections is fineshed

        :param client: the subscribed MQTT client
        :param packet:
        """
        self.disconnected = True
        logging.info('[DISCONNECTED  {}]'.format(client._client_id))

    def on_connect(self, client, flags, rc, properties=None):
        """
        The handler run when the connections is established

        :param client: the subscribed MQTT client
        :param flags:
        :param rc:
        :param properties: Custom properties
        """
        self.connected = True
        self.connack = (flags, rc, properties)
        logging.info('[CONNECTED {}]'.format(client._client_id))

    def register_for_client(self, client):
        """
        Register handlers to the client.

        :param client: Client to register handlers
        """
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.on_connect = self.on_connect
        client.on_subscribe = self.on_subscribe

        self.client = client


def on_disconnect(client, packet):
    logging.info('[DISCONNECTED  {}]'.format(client._client_id))


def on_connect(client, flags, rc, properties=None):
    logging.info('[CONNECTED {}]'.format(client._client_id))


async def create_client(options, postfix='_client'):
    """
    Create a new GMQTT client

    :param options: Options for client initialization
    :para postfix: Unique postfix for the client
    """
    client_id = '%s%s' % (uuid.uuid4(), postfix)

    client = gmqtt.Client(client_id, session_expiry_interval=60, clean_session=True)
    
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.set_auth_credentials(options.get('username', ''))
    await client.connect(
        host=options['host'],
        port=options['port'],
        keepalive=60,
        version=MQTTv311
    )
    return client
