# -*- coding: utf-8 -*-
import logging
from influxdb import InfluxDBClient


def open_datasource(options):
    return LocalDataSource(
        **options
    )


class LocalDataSource(object):

    def __init__(self, host, port, username, password, database, path, duration='4w'):
        logging.debug(f'{host}/{path}:{port} <{username}> ({database})')
        self.db = InfluxDBClient(host=host, port=port, username=username, password=password, database=database, path=path)

        self.db.create_database(database)
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

    def publish_dict(self, point_dict):
        json_body = [
            {
                'measurement': point_dict['table'],
                'tags': point_dict['tags'],
                'time': point_dict['timestamp'],
                'fields': point_dict['message']
            }
        ]
        return self.db.write_points(json_body, protocol='json', retention_policy='awesome_policy')

    def query(self, q, db_name):
        return self.db.query(q, database=db_name)
