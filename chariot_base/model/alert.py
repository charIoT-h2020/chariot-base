# -*- coding: utf-8 -*-
import json
import datetime


class Alert(object):
    """
    Describe each alert raised by Chariot
    """
    def __init__(self, name, msg=None, severity=100):
        self.timestamp = datetime.datetime.now().isoformat()
        self.name = name
        self.message = msg
        self.severity = severity

    def dict(self):
        return {
            'name': self.name,
            'message': self.message,
            'severity': self.severity,
            'timestamp': self.timestamp
        }

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return json.dumps(self.dict())
