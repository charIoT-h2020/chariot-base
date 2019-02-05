# -*- coding: utf-8 -*-

import os
import json


def open_config_file(files = ['./config.json', './tests/config.json']):
    filename = None
    for name in files:
        if os.path.isfile(name):
            filename = name

    if filename is None:
        raise Exception('Configuration file is not exists')

    with open(filename, 'r') as read_file:
        opts = json.load(read_file)

    return opts