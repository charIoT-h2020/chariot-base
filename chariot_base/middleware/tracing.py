from werkzeug.wrappers import Request, Response, ResponseStream
from chariot_base.utilities.tracing import Tracer, Traceable

class TracingMiddleware(Traceable):
    '''
    Jaeger Tracing middleware
    '''

    def __init__(self, app, options):
        self.app = app
        self.tracer = None
        self.set_up_tracer(options)

    def __call__(self, environ, start_response):
        request = Request(environ)
        
        span = self.start_span_from_request('request', request)
        self.set_tag(span, 'path', request.path)
        environ['span'] = span
        environ['trace'] = self
        result = self.app(environ, start_response)
        self.close_span(span)
        return result