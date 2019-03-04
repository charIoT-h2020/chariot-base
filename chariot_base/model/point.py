# -*- coding: utf-8 -*-
import json
import uuid
import datetime


FIXEDIO = 'fixedIO'
WIFI = 'wifi'
SENSORDATA = 'sensorData'
SENSORVALUES = 'sensorValues'

class DataPointFactory(object):
    """
    Converts to a new point
    """
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def from_mqtt_message(self, message):
        """
        From mosquitto message payload
        """
        msg = message.payload.decode('utf-8')
        message_parsed = self.from_json_string(msg)
        message_parsed.topic = message.topic
        return message_parsed

    def from_json_string(self, msg):
        """
        From JSON message payload
        """
        decoded_msg = json.loads(msg)
        for key, message in decoded_msg.items():
            if FIXEDIO in message:
                decoded_msg = message[FIXEDIO]
            elif WIFI in message:
                obj = {}
                for values in message[WIFI][SENSORDATA][SENSORVALUES]:
                    obj[values['name']] = values['value']
                decoded_msg = obj
            else:
                raise Exception('Message format is not recognized')
        return DataPoint(self.db, self.table, decoded_msg)


class DataPoint(object):
    def __init__(self, db, table, message):
        self.id = uuid.uuid4()
        self.db = db
        self.table = table
        self.message = message
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.topic = None
        self.sensor_id = None

    def _event_type(self):
        if self.topic is None:
            return ''
        return self.topic.replace('/', '.')
