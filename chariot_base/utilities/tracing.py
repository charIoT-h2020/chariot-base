import logging
from jaeger_client import Config
from opentracing import Format


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
                'logging': False,
            },            
            service_name=self.name,
        )

        self.tracer = config.initialize_tracer()

    def inject(self, span, msg):
        d = {}
        self.tracer.inject(span.context, Format.TEXT_MAP, d)
        msg['uber-trace-id'] = d['uber-trace-id']
        return msg

    def extract(self, msg):
        d = {
            'uber-trace-id': msg['uber-trace-id']
        }
        return self.tracer.extract(Format.TEXT_MAP, d)

    def close(self):
        self.tracer.close()