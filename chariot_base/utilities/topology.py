# -*- coding: utf-8 -*-
import re 

import requests
import logging

from .tracing import Traceable
from ..model import DataPoint

from iotl import interpreter

class Topology(Traceable):

    def __init__(self, url, tracer):
        self.url = url
        self.tracer = tracer

    def sensor(self, point: DataPoint, span: object):
        url = f"{self.url}/devices/sensor/{point.sensor_id}"
        headers = self.inject_to_request_header(span, url)
        result = requests.get(url, headers=headers)

        if result.status_code == 404:
            logging.debug(f'Sensor "{point.sensor_id}" is not found')
            return None
        else:
            logging.debug(f'Sensor "{point.sensor_id}" found')
            return result.json()

    def report_new_sensor(self, point: DataPoint, span: object):
        if self.sensor(point, span) is None:
            url = f"{self.url}/iotl/command"
            
            headers = self.inject_to_request_header(span, url)
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'application/json'

            statement = f"define SENSOR {point.sensor_id} --params {{ \"detected\": \"{point.timestamp}\" }}\n"
            if point.gateway is not None:
                statement += f"define GATEWAY gateway_{point.gateway} --params {{ \"detected\": \"{point.timestamp}\", \"pubkey_type\": \"None\" }}\n"
                statement += f"register {point.sensor_id} -> gateway_{point.gateway}\n"
            logging.debug(statement)
            payload = {
                "command_text": statement
            }

            result = requests.post(url, json=payload, headers=headers)
            logging.debug(f'Add new sensor returns: {result.json()["result"]}')