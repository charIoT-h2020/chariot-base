# -*- coding: utf-8 -*-
import json


class Subscriber(object):
    def __init__(self, subscriber_id):
        self.id = subscriber_id
        self.sensors = set()

    def dict(self):
        return {
            'id': self.id,
            'sensors': list(self.sensors)
        }

    def __str__(self):
        return json.dumps(self.dict())