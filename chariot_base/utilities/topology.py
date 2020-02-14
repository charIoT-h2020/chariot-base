# -*- coding: utf-8 -*-
import re 
import json
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

    def gateway(self, point: DataPoint, span: object):
        url = f"{self.url}/devices/gateway/{point.gateway}"
        headers = self.inject_to_request_header(span, url)
        result = requests.get(url, headers=headers)

        if result.status_code == 404:
            logging.debug(f'Sensor "{point.gateway}" is not found')
            return None
        else:
            logging.debug(f'Sensor "{point.gateway}" found')
            return result.json()

    def report_new_sensor(self, point: DataPoint, span: object):
        if self.sensor(point, span) is None:
            url = f"{self.url}/iotl/command"
            
            headers = self.inject_to_request_header(span, url)
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'application/json'

            statement = f"define SENSOR {point.sensor_id} --params {{ \"detected\": \"{point.timestamp}\" }}\n"
            if point.gateway is not None:
                point.gateway = f'gateway_{point.gateway}'
                old_gateway = self.gateway(point, span)
                if old_gateway is None:
                    statement += f"define GATEWAY {point.gateway} --params {{ \"detected\": \"{point.timestamp}\", \"pubkey_type\": \"None\" }}\n"
                else:
                    del old_gateway['name']
                    old_gateway['detected'] = point.timestamp
                    statement += f"define GATEWAY {point.gateway} --params {json.dumps(old_gateway)}\n"
                statement += f"register {point.sensor_id} -> {point.gateway}\n"
            logging.debug(statement)
            payload = {
                "command_text": statement
            }

            result = requests.post(url, json=payload, headers=headers)
            logging.debug(f'Add new sensor returns: {result.json()["result"]}')