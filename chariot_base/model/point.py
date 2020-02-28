# -*- coding: utf-8 -*-
import json
import uuid
import datetime
import logging
from ..utilities.parsing import try_parse, normalize_mac_address


FIXEDIO = 'fixedIO'
FIRMWARE_UPLOAD = 'ftpFwUpd'
FIRMWARE_STATUS = 'ftpFwUpdEventCode'
WIFI = 'wifi'
BLE = 'ble'
SENSORDATA = 'sensorData'
SENSORSECURITYEVENT = 'sensorSecurityEvent'
SENSORSECURITYEVENTCODE = 'sensorSecurityEventCode'
SENSORVALUES = 'sensorValues'
SENSORNAME = 'sensorName'
SENSORSTATUSCODE = 'sensorStatusCode'


class UnAuthenticatedSensor(Exception):
    def __init__(self, id):
        super(Exception, self).__init__()
        self.id = id


class FirmwareUploadException(Exception):
    def __init__(self, key, point, gateway_name):
        super(Exception, self).__init__()
        self.key = key
        self.point = point
        self.gateway = gateway_name


class DataPointFactory(object):
    """
    Converts to a new point
    """
    def __init__(self, db, table):
        self.db = db
        self.table = table
        self.firmware_upload_table = table

    def set_firmware_upload_table(self, table):
        self.firmware_upload_table = table

    def from_mqtt_message(self, message):
        """
        From mosquitto message payload
        """
        msg = message.payload.decode('utf-8')
        messages_parsed = self.from_json_string(msg)

        for i in range(len(messages_parsed)):
            messages_parsed[i].topic = message.topic

        return messages_parsed

    def from_json_string(self, msg):
        """
        From JSON message payload
        """
        decoded_msg = json.loads(msg)
        messages = []
        for key, message in decoded_msg.items():
            key = normalize_mac_address(key.replace('NMS_', ''))
            gateway_name = key            
            logging.debug(f'key: {key} message: {message}')
            parsed_msg = None
            if FIXEDIO in message:
                parsed_msg = message[FIXEDIO]
                key = 'gateway_%s' % key
            elif WIFI in message:
                parsed_msg, key = self.parse_json_from_smart_sensor(WIFI, message, key)
            elif BLE in message:
                parsed_msg, key = self.parse_json_from_smart_sensor(BLE, message, key)
            elif FIRMWARE_UPLOAD in message:
                parsed_msg, key = self.parse_json_from_firmware(message, key, gateway_name)
            else:
                raise Exception('Message format is not recognized')

            if FIRMWARE_UPLOAD in message:
                point = FirmwareUpdateStatus(self.db, self.firmware_upload_table, parsed_msg)                
                point.gateway = gateway_name
                point.sensor_id = key
            else:
                point = DataPoint(self.db, self.table, parsed_msg)
                point.gateway = gateway_name
                point.sensor_id = key
            messages.append(point)
        return messages

    def parse_json_from_firmware(self, message, key, gateway_name):
        obj = message[FIRMWARE_UPLOAD]
        if SENSORNAME in obj:
            key = 'device_%s_%s' % (key, obj[SENSORNAME])
        else:
            key = 'gateway_%s' % key

        if obj[FIRMWARE_STATUS] == 1 or obj[FIRMWARE_STATUS] == 2:
            return obj, key
        else:
            logging.debug(f'Firmware error for "{gateway_name}"."{key}"')
            raise FirmwareUploadException(key, obj, gateway_name)

    def parse_json_from_smart_sensor(self, connection_type, message, key):
        if SENSORSECURITYEVENT in message[connection_type]:
            key = 'device_%s_%s' % (key, message[connection_type][SENSORSECURITYEVENT][SENSORNAME])
            if message[connection_type][SENSORSECURITYEVENT][SENSORSECURITYEVENTCODE] == 1:
                raise UnAuthenticatedSensor(key)
        else:
            key = 'device_%s_%s' % (key, message[connection_type][SENSORDATA][SENSORNAME])

            if message[connection_type][SENSORDATA][SENSORSTATUSCODE] == 2:
                raise UnAuthenticatedSensor(key)

            obj = {}
            for values in message[connection_type][SENSORDATA][SENSORVALUES]:
                obj[values['name']] = try_parse(values['value'])
            return obj, key

class DataPoint:
    def __init__(self, db, table, message):
        self.id = uuid.uuid4()
        self.db = db
        self.table = table
        self.message = message
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.gateway = None
        self.topic = None
        self.sensor_id = None

    def _event_type(self):
        if self.topic is None:
            return ''
        return self.topic.replace('/', '.')


class FirmwareUpdateStatus(DataPoint):
    def __init__(self, db, table, message):
        super().__init__(db, table, message)
