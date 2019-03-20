# -*- coding: utf-8 -*-
import json


class Message(object):
    """
    Describe message passed between Chariot's components
    """
    def __init__(self, sensor_id, value):
        self.sensor_id = sensor_id
        self.value = value
        self.destination = None
        self.id = None
        self.trace_id = None

    def dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'value': self.value,
            'destination': self.destination,
            'uber-trace-id': self.trace_id
        }

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return json.dumps(self.dict())
