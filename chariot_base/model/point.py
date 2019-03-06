# -*- coding: utf-8 -*-
import json
import uuid
import datetime
from ..utilities.parsing import try_parse


FIXEDIO = 'fixedIO'
WIFI = 'wifi'
SENSORDATA = 'sensorData'
SENSORVALUES = 'sensorValues'
SENSORNAME = 'sensorName'

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
        messages_parsed = self.from_json_string(msg)

        i = 0
        for message_parsed in messages_parsed:
            messages_parsed[i].topic = message.topic
            i = i + 1

        return messages_parsed

    def from_json_string(self, msg):
        """
        From JSON message payload
        """
        decoded_msg = json.loads(msg)
        messages = []
        for key, message in decoded_msg.items():
            parsed_msg = None
            if FIXEDIO in message:
                parsed_msg = message[FIXEDIO]
            elif WIFI in message:
                obj = {}
                for values in message[WIFI][SENSORDATA][SENSORVALUES]:
                    obj[values['name']] = try_parse(values['value'])
                parsed_msg = obj
                key = '%s_%s' % (key, message[WIFI][SENSORDATA][SENSORNAME])
            else:
                raise Exception('Message format is not recognized')

            point = DataPoint(self.db, self.table, parsed_msg)
            point.sensor_id = key
            messages.append(point)
        return messages

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
