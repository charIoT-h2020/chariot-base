# -*- coding: utf-8 -*-

import os
import json
import logging
import logging.config


default_logging = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console"
        }
    },
    "loggers": {
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    },
    "formatters": {
        "console": {
            "format": "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
        }
    }
}


class Brokers(object):
    def __init__(self, options):
        self.southbound = options.get('southbound', {})
        self.northbound = options.get('northbound', {})


class Configuration(object):
    def __init__(self, options):
        self.cloudant = options.get('cloudant', {"enabled": False})
        self.watson_iot = options.get('watson_iot', {"enabled": False})
        self.local_storage = options.get('local_storage', {"enabled": False})
        self.brokers = Brokers(options.get('brokers', {}))
        self.tracer = options.get('tracer', {"enabled": False})
        self.privacy_engine = options.get('privacy_engine', None)
        self.alert_digester = options.get('alert_digester', None)
        self.dispatcher = options.get('dispatcher', None)
        self.northbound_dispatcher = options.get('northbound_dispatcher', None)
        self.topology = options.get('topology', None)
        self.database = options.get('database', None)
        self.set_logging(options.get('logging', default_logging))

    def set_logging(self, options):
        self.logging = options
        logging.config.dictConfig(self.logging)


def open_config_file(files=['./config.json', './tests/config.json']):
    filename = None
    for name in files:
        if os.path.isfile(name):
            filename = name

    if filename is None:
        raise Exception('Configuration file is not exists')

    with open(filename, 'r') as read_file:
        opts = json.load(read_file)

    return Configuration(opts)
