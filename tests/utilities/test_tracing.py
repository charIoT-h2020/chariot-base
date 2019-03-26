#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import time
import falcon
import falcon.testing as testing

from chariot_base.utilities import open_config_file, Traceable, Tracer

@pytest.fixture(scope='session')
def get_tracer():
    opts = open_config_file()
    service = Traceable()
    options_tracer = opts.tracer

    service.set_up_tracer(options_tracer)

    yield service.tracer
    service.tracer.close()


def test_no_tracer(get_tracer):
    tracer = get_tracer   
    service = Traceable()

    assert service.tracer is None

    span = service.start_span('root')
    assert span is None

    span = service.start_span_from_message('root', {})
    assert span is None

    span = service.start_span_from_request('root', None)
    assert span is None

    span = service.inject_to_request_header(None, None)
    assert span is None

    span = service.inject_to_message(None, None)
    assert span is None

    service.log(None, {'event': 'time to first byte', 'packet.size': 100})
    service.log(None, None)
    service.error(None, None)
    service.set_tag(None, None, None)
    service.close_span(None)


def test_inject_tracer(get_tracer):
    tracer = get_tracer   
    service = Traceable()
    service.inject_tracer(tracer)

    assert service.tracer is not None


def test_open_span(get_tracer):
    tracer = get_tracer
    service = Traceable()
    service.inject_tracer(tracer)
    assert service.tracer is not None

    span = service.start_span('root')
    assert span is not None
    m = service.inject_to_message(span, {})
    service.set_tag(span, 'is_ok', True)
    time.sleep(.500)
    service.close_span(span)

    cs = service.start_span_from_message('stage1', m)
    m = service.inject_to_message(cs, {})
    csin = service.start_span_from_message('stage2', m)
    time.sleep(.300)
    csinchild = service.start_span('stage3', csin)
    service.close_span(csinchild)
    time.sleep(.300)
    service.close_span(csin)
    time.sleep(.100)
    service.close_span(cs)


def test_inject_http_request(get_tracer):

    tracer = get_tracer
    service = Traceable()
    service.inject_tracer(tracer)

    root = service.start_span_from_request('root', None)
    headers = service.inject_to_request_header(root, 'https://api.test.org')
    service.close_span(root)

    env = testing.create_environ(
            protocol='https',
            host='example.org',
            port=9000,
            app='chariot_base',
            path='/hello',
            query_string='q=test',
            headers=headers)

    req = falcon.Request(env)

    stage1 = service.start_span_from_request('root', req)
    service.set_tag(stage1, 'error', True)
    service.log(stage1, {
            'event': 'time to first byte',
            'packet.size': 100})
    service.log(stage1, {
            'event': 'error',
            'packet.size': 100})
    try:
        raise ValueError('test error')
    except ValueError as ex:
        service.error(stage1, ex, False)

    service.close_span(stage1)

    stage2 = service.start_span_from_request('root', req)
    try:
        raise ValueError('test error')
    except ValueError as ex:
        service.error(stage1, ex, True)