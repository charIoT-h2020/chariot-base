# -*- coding: utf-8 -*-
import re 

from iotl import interpreter

class IoTLWrapper(object):
    
    def __init__(self, options):
        self.filepath = options['filepath']
        self.IoTState = interpreter.IoTState()

    def load(self, data=None):
        if data is None:
            with open(self.filepath, 'r') as f:
                self.IoTState.parse(f.read())
        else:
            self.IoTState.parse(data)
        return True

    def isSensitive(self, sensor_id):
        try:
            return self.IoTState.params[sensor_id]['privacySensitive'] == 1
        except KeyError:
            return False

    def params(self, id):
        try:
            return self.IoTState.params[id]
        except KeyError:
            return {}

    def acl(self, sensor_id):
        try:
            return self.IoTState.acl[sensor_id]
        except KeyError:
            return []

    def schema(self, only_private=False):
        if only_private:
            return [self.IoTState.schema[key] for key in self.IoTState.schema if self.IoTState.schema[key]['is_private'] == True]
        return self.IoTState.schema

    def is_match(self, schema, msg):
        return re.search(schema["pattern"], msg) is not None