from opentracing_instrumentation import request_context
import logging


class TracingHandler(logging.StreamHandler):
    def __init__(self, use_tracer):
        logging.StreamHandler.__init__(self)
        self.tracer = use_tracer

    def emit(self, record):
        span = request_context.get_current_span()

        if span is not None:
            msg = self.format(record)
            span.log_kv({logging.getLevelName(record.levelno): msg})
