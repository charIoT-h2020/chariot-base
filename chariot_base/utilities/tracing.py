from jaeger_client import Config
from opentracing import Format
from opentracing.ext import tags

class Tracer(object):
    def __init__(self, options):
        self.name = options['service']
        self.host = options['host']
        self.port = options['port']
        self.tracer = None

    def init_tracer(self):
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

    def close(self):
        self.tracer.close()


class Traceable:
    def __init__(self):
        self.tracer = None

    def inject_tracer(self, tracer):
        self.tracer = tracer

    def set_up_tracer(self, options):
        self.tracer = Tracer(options)
        self.tracer.init_tracer()

    def start_span(self, id, child_span=None):
        if self.tracer is None:
            return

        if child_span is None:
            return self.tracer.tracer.start_span(id)
        else:
            return self.tracer.tracer.start_span(id, child_of=child_span)

    def start_span_from_message(self, id, msg):
        if self.tracer is None:
            return
        d = {
            'uber-trace-id': msg['uber-trace-id']
        }
        span_ctx = self.tracer.tracer.extract(Format.TEXT_MAP, d)
        span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

        return self.tracer.tracer.start_span(id, child_of=span_ctx, tags=span_tags)

    def start_span_from_request(self, id, req):
        if self.tracer is None:
            return

        if req is None:
            return self.start_span()

        span_ctx = self.tracer.tracer.extract(Format.HTTP_HEADERS, req.headers)
        span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

        return self.tracer.tracer.start_span(id, child_of=span_ctx, tags=span_tags)

    def inject_to_request_header(self, span, url):
        if self.tracer is None:
            return

        span.set_tag(tags.HTTP_METHOD, 'GET')
        span.set_tag(tags.HTTP_URL, url)
        span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
        headers = {}
        self.tracer.tracer.inject(span, Format.HTTP_HEADERS, headers)
        return headers

    def inject_to_message(self, span, msg):
        if self.tracer is None:
            return
        carrier = {}
        self.tracer.tracer.inject(span.context, Format.TEXT_MAP, carrier=carrier)
        msg['uber-trace-id'] = carrier['uber-trace-id']
        return msg

    def close_span(self, span):
        if self.tracer is None:
            return
        span.finish()