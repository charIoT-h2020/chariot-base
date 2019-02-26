# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient


class LocalDataSource(object):

    def __init__(self, hostname, port, username, password, db_name, duration='4w'):
        self.db = InfluxDBClient(hostname, port, username, password, db_name)
        self.db.create_database(db_name)
        self.db.create_retention_policy('awesome_policy', duration, 3, default=True)

    def publish(self, point):
        json_body = [
            {
                'measurement': point.table,
                'tags': {
                    'topic': point.topic,
                    'sensor_id': point.sensor_id
                },
                'time': point.timestamp,
                'fields': point.message
            }
        ]
        return self.db.write_points(json_body, protocol='json', retention_policy='awesome_policy')

    def query(self, q, db_name):
        return self.db.query(q, database=db_name)
