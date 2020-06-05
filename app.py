#!/usr/bin/env python3

import time
import requests
import os

from requests.exceptions import RequestException
from subprocess import check_output, CalledProcessError
from prometheus_client import start_http_server, Counter

METRICS_PORT = int(os.environ.get("METRICS_PORT", "9000"))
HTTP_TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "5"))
GETENT_TIMEOUT = int(os.environ.get("GETENT_TIMEOUT", "5"))
HTTP_URL = os.environ["HTTP_URL"]
GETENT_HOST = os.environ["GETENT_HOST"]

getent_total = Counter("netcheck_getent_total", "Total getent calls", ["host"])
getent_failures = Counter("netcheck_getent_failures", "Failed getent calls", ["host"])
http_total = Counter("netcheck_http_total", "Total http calls", ["url"])
http_failures = Counter("netcheck_http_failures", "Failed http calls", ["url"])

getent_failures.labels(GETENT_HOST).inc(0)
http_failures.labels(HTTP_URL).inc(0)


def test_getent():
    try:
        check_output(["getent", "hosts", GETENT_HOST], timeout=GETENT_TIMEOUT)
    except CalledProcessError:
        getent_failures.labels(GETENT_HOST).inc()
    finally:
        getent_total.labels(GETENT_HOST).inc()


def test_http_get():
    try:
        requests.get(HTTP_URL, timeout=HTTP_TIMEOUT)
    except RequestException:
        http_failures.labels(HTTP_URL).inc()
    finally:
        http_total.labels(HTTP_URL).inc()


if __name__ == "__main__":
    start_http_server(METRICS_PORT)
    while True:
        test_getent()
        test_http_get()
        time.sleep(5)
