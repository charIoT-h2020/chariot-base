# -*- coding: utf-8 -*-
import json
import datetime


class Alert(object):
    """
    Describe each alert raised by Chariot
    """
    def __init__(self, msg=None, severity=100):
        self.timestamp = datetime.datetime.now().isoformat()
        self.message = msg
        self.severity = severity

    def dict(self):
        return {
            'message': self.message,
            'severity': self.severity
        }

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return json.dumps(self.dict())
