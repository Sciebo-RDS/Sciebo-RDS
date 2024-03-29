from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import multiprocessing

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = "debug"
capture_output = True
worker_class = "eventlet"
reload = True

def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(9999)


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
