import json
import datetime
import dateutil.parser

from ..utilities import Traceable


class HealthCheck(Traceable):
    def __init__(self, id):
        self.name = id

    def inject_connector(self, connector):
        self.connector = connector
        return self

    def do(self, message):
        message = json.loads(message)
        span = self.connector.start_span_from_message('health_check', message)
        try:            
            received = datetime.datetime.utcnow().isoformat()
            topic = message['destination']

            result = {
                'id': message['id'],
                'name': self.name,
                'status': self.check(),
                'received': received,
                'sended': message['timestamp']
            }
            self.connector.inject_to_message(span, result)
            self.connector.publish(topic, result)
            self.connector.close_span(span)
        except Exception as ex:
            self.connector.error(span, ex)


    def check(self):
        return {
            'code': 0,
            'message': 'running'
        }
