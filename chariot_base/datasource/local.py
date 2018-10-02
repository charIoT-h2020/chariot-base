# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient


class LocalDataSource(object):

    def __init__(self):
        self.db = InfluxDBClient('172.18.1.4', 8086, 'root', 'root', 'fog_logs')

    def publish(self, point):
        json_body = [
            {
                'measurement': point.table,
                'tags': {
                    'topic': point.topic,
                    'id': 'gateway_5410ec4d1601'
                },
                'time': point.timestamp,
                'fields': point.message
            }
        ]
        self.db.write_points(json_body, database=point.db, protocol='json')
