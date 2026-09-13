"""WSGI support for Otsukare's gateway-mounted URL prefix."""

EXPECTED_PREFIX = "/projects/otsukare"


class ForwardedPrefixMiddleware:
    """Set ``SCRIPT_NAME`` from the gateway's validated application prefix."""

    def __init__(self, app):
        """Wrap a WSGI application."""
        self.app = app

    def __call__(self, environ, start_response):
        """Apply the expected forwarded prefix before Flask builds URLs."""
        forwarded_prefix = environ.get("HTTP_X_FORWARDED_PREFIX", "").rstrip("/")
        environ["SCRIPT_NAME"] = EXPECTED_PREFIX if forwarded_prefix == EXPECTED_PREFIX else ""
        return self.app(environ, start_response)
