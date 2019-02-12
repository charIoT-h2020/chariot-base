import logging
from jaeger_client import Config


class Tracer(object):
    def __init__(self, options):
        self.name = options['service']
        self.host = options['host']
        self.port = options['port']
        self.tracer = None

    def init_tracer(self):
        logging.getLogger('').handlers = []
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)

        config = Config(
            config={
                'sampler': {
                    'type': 'const',
                    'param': 1,
                },
                'local_agent': {
                    'reporting_host': self.host,
                    'reporting_port': self.port
                },
                'logging': True,
            },            
            service_name=self.name,
        )

        self.tracer = config.initialize_tracer()