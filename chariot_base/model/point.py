# -*- coding: utf-8 -*-
import json
import uuid
import datetime


class DataPointFactory(object):
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def from_mqtt_message(self, message, attribute_name=None):
        msg = message.payload.decode('utf-8')
        message_parsed = self.from_json_string(msg, attribute_name)
        message_parsed.topic = message.topic
        return message_parsed

    def from_json_string(self, msg, attribute_name=None):
        decoded_msg = json.loads(msg)
        if attribute_name is None:
            message_payload = decoded_msg
        else:
            message_payload = decoded_msg[attribute_name]
        return DataPoint(self.db, self.table, message_payload)


class DataPoint(object):
    def __init__(self, db, table, message):
        self.id = uuid.uuid4()
        self.db = db
        self.table = table
        self.message = message
        self.timestamp = datetime.datetime.now().isoformat()
        self.topic = None
        self.sensor_id = None

    def _event_type(self):
        if self.topic is None:
            return ''
        return self.topic.replace('/', '.')
