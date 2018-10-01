# -*- coding: utf-8 -*-
import json
import datetime


class Alert(object):

    def __init__(self, msg=None, severity=100):
        self.timestamp = datetime.datetime.now().isoformat()
        self.message = msg
        self.severity = severity

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        msg = {
            'message': self.message,
            'severity': self.severity
        }

        return json.dumps(msg)
