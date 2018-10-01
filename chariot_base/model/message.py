# -*- coding: utf-8 -*-
import json


class Message(object):
    def __init__(self, sensor_id, value):
        self.sensor_id = sensor_id
        self.value = value
        self.destination = None

    def __str__(self):
        return json.dumps({
            'sensor_id': self.sensor_id,
            'value': self.value
        })
