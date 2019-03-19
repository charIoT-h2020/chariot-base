#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import time

from chariot_base.utilities import open_config_file, Traceable, Tracer

@pytest.fixture(scope="session")
def get_tracer():
    opts = open_config_file()
    alerts = Traceable()
    options_tracer = opts.tracer

    alerts.set_up_tracer(options_tracer)

    yield alerts.tracer
    alerts.tracer.close()


def test_no_tracer(get_tracer):
    tracer = get_tracer   
    alerts = Traceable()

    assert alerts.tracer is None

    span = alerts.start_span('root')
    assert span is None

    span = alerts.start_span_from_message('root', {})
    assert span is None

    span = alerts.start_span_from_request('root', None)
    assert span is None

    span = alerts.inject_to_request_header(None, None)
    assert span is None

    span = alerts.inject_to_message(None, None)
    assert span is None

    alerts.close_span(None)


def test_inject_tracer(get_tracer):
    tracer = get_tracer   
    alerts = Traceable()
    alerts.inject_tracer(tracer)

    assert alerts.tracer is not None


def test_open_span(get_tracer):
    tracer = get_tracer
    alerts = Traceable()
    alerts.inject_tracer(tracer)
    assert alerts.tracer is not None

    span = alerts.start_span('root')
    assert span is not None
    m = alerts.inject_to_message(span, {})
    time.sleep(.500)
    alerts.close_span(span)

    cs = alerts.start_span_from_message('stage1', m)
    m = alerts.inject_to_message(cs, {})
    csin = alerts.start_span_from_message('stage2', m)
    time.sleep(.300)
    csinchild = alerts.start_span('stage3', csin)
    alerts.close_span(csinchild)
    time.sleep(.300)
    alerts.close_span(csin)
    time.sleep(.100)
    alerts.close_span(cs)