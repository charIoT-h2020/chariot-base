#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import time

from chariot_base.utilities import open_config_file, Traceable, Tracer

@pytest.fixture(scope="session")
def get_tracer():
    opts = open_config_file()
    options_tracer = opts.tracer
    tracer = Tracer(options_tracer)
    tracer.init_tracer()
    yield tracer
    tracer.close()

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
    alerts.close_span(csin)
    time.sleep(.100)
    alerts.close_span(cs)