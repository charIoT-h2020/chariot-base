# -*- coding: utf-8 -*-
import re 

import requests
import logging

from iotl import interpreter

class IoTLWrapper(object):
    
    def __init__(self, options):
        self.filepath = options['filepath']
        if 'iotl_url' in options:
            self.url = options['iotl_url']
        else:
            self.url = None
        self.IoTState = interpreter.IoTState()
        self.session = requests.Session()
        self.session.trust_env = False

    def sync(self, headers=None):
        if self.url is not None:
            url = self.url
            result = self.session.get(url, headers=headers)
            current_iotl = result.json()
            self.load(current_iotl['code'])
            self.schema = self.schema(True)
            logging.debug('Topology is updated')
            return True
        return False

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

    def sensor(self):
        return self.IoTState.system['SENSOR']

    def expects(self, name):
        keys = self.IoTState.expects(name)
        return [self.IoTState.schema[key]['pattern'] for key in keys]

    def schema(self, only_private=False):
        if only_private:
            return [self.IoTState.schema[key] for key in self.IoTState.schema if self.IoTState.schema[key]['is_private'] == True]
        return self.IoTState.schema

    def is_match(self, schema, msg):
        return re.search(schema["pattern"], msg) is not None