# -*- coding: utf-8 -*-
import json
import datetime


class DataPoint(object):
    def __init__(self, db, table, message, attribute_name=None):
        self.db = db
        self.table = table

        msg = message.payload.decode('utf-8')
        decoded_msg = json.loads(msg)

        self.topic = message.topic
        if attribute_name is None:
            self.message = decoded_msg
        else:
            self.message = decoded_msg[attribute_name]
        self.timestamp = datetime.datetime.now().isoformat()

    def _event_type(self):
        return self.topic.replace('/', '.')
