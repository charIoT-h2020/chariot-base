from jaeger_client import Config
from opentracing import Format
from opentracing.ext import tags
import traceback


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
    """All utilities methods to send logs to jaeger
    """

    def __init__(self):
        self.tracer = None

    def inject_tracer(self, tracer):
        """Inject an opentracing client

        :param tracer: the opentracing client
        """
        self.tracer = tracer

    def set_up_tracer(self, options):
        """Configure a new opentracing client

        :param options: options to configure the new client
        """
        self.tracer = Tracer(options)
        self.tracer.init_tracer()

    def start_span(self, id, child_span=None):
        """Start a new logging span

        :param span_id: identifier of a new logging span
        :param child_span: parent span
        """
        if self.tracer is None:
            return None

        if child_span is None:
            return self.tracer.tracer.start_span(id)
        else:
            return self.tracer.tracer.start_span(id, child_of=child_span)

    def start_span_from_message(self, id, msg):
        if self.tracer is None:
            return None
        d = {
            'uber-trace-id': msg['uber-trace-id']
        }
        span_ctx = self.tracer.tracer.extract(Format.TEXT_MAP, d)
        span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

        return self.tracer.tracer.start_span(id, child_of=span_ctx, tags=span_tags)

    def start_span_from_request(self, id, req):
        if self.tracer is None:
            return None

        if req is None:
            return self.start_span(id)

        span_ctx = self.tracer.tracer.extract(Format.HTTP_HEADERS, req.headers)
        span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

        return self.tracer.tracer.start_span(id, child_of=span_ctx, tags=span_tags)

    def inject_to_request_header(self, span, url):
        """Inject tracing id to http header.
        :param span: specified span.
        :type span: Span

        :param url: Service URL,
        :type url: string
        """

        if self.tracer is None:
            return None

        span.set_tag(tags.HTTP_METHOD, 'GET')
        span.set_tag(tags.HTTP_URL, url)
        span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
        headers = {}
        self.tracer.tracer.inject(span, Format.HTTP_HEADERS, headers)
        return headers

    def inject_to_message(self, span, msg):
        """Inject tracing id to the message.
        :param span: specified span.
        :type span: Span

        :param msg: Message dictionary.
        :type msg: dict
        """
        if self.tracer is None:
            return None
        carrier = {}
        self.tracer.tracer.inject(span.context, Format.TEXT_MAP, carrier=carrier)
        msg['uber-trace-id'] = carrier['uber-trace-id']
        return msg

    def set_tag(self, span, id, value):
        """Attaches a key/value pair to the span.

        The value must be a string, a bool, or a numeric type.

        :param span: specified span.
        :type span: Span

        :param id: key or name of the tag. Must be a string.
        :type id: str

        :param value: value of the tag.
        :type value: string or bool or int or float
        """
        if self.tracer is None:
            return None
        span.set_tag(id, value)

    def log(self, span, values):
        """Adds a log record to the Span.

        :param span: specified span.
        :type span: Span

        :param key_values: A dict of string keys and values of any type
        :type key_values: dict
        """
        if self.tracer is None:
            return None
        span.log_kv(values)

    def error(self, span, ex, close_span=True):
        """Adds a error record to the Span.

        :param span: specified span.
        :type span: Span

        :param ex: the exception object
        :type ex: Exception

        :param close_span: close the span
        :type close_span: bool
        """
        if self.tracer is None:
            return None
        self.set_tag(span, 'error', True)
        tb = traceback.format_exc()
        span.log_kv({
            'event': 'error',
            'message': str(ex),
            'stack': tb
        })
        if close_span:
            self.close_span(span)

    def close_span(self, span):
        """Close a logging span

        :param span: Span to close
        """
        if self.tracer is None:
            return
        span.finish()