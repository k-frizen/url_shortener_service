from datetime import datetime

from flask import request
import logging

logger = logging.getLogger(__name__)


class RequestLoggerMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request_timestamp = datetime.utcnow()

        def custom_start_response(status, headers, *args, **kwargs):
            self.log_request(request_timestamp, status)
            return start_response(status, headers, *args, **kwargs)

        return self.app(environ, custom_start_response)

    def log_request(self, timestamp, status):
        log_data = {
            "timestamp": timestamp.isoformat(),
            "method": request.method,
            "path": request.path,
            "ip": request.remote_addr,
            "status": status
        }
        logger.info(log_data)


def setup_request_logger(app):
    app.wsgi_app = RequestLoggerMiddleware(app.wsgi_app)
