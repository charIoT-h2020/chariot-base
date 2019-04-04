import json
import datetime
import dateutil.parser

from ..utilities import Traceable


class HealthCheck(Traceable):
    def __init__(self, id):
        self.id = id

    def inject_connector(self, connector):
        self.connector = connector
        return self

    def do(self, message):
        message = json.loads(message)
        
        received = datetime.datetime.utcnow().isoformat()
        topic = message['destination']

        result = {
            'id': self.id,
            'status': self.check(),
            'received': received,
            'sended': message['timestamp']
        }

        self.connector.publish(topic, result)

    def check(self):
        return {
            'code': 0,
            'message': 'running'
        }
