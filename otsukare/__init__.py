"""Flask init for Otsukare app."""

# Copyright © 2021 by Nick Jenkins. All rights reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from otsukare.prefix import ForwardedPrefixMiddleware


def create_app() -> Flask:
    """Creates the primary Flask app with config.

    Returns:
        Flask: returns flask app.
    """
    app = Flask(__name__)
    app.config.from_object("otsukare.config.BaseConfig")
    return app


app = create_app()
db = SQLAlchemy(app)
app.wsgi_app = ProxyFix(  # type: ignore[method-assign]
    ForwardedPrefixMiddleware(app.wsgi_app), x_for=1, x_proto=1, x_host=1, x_prefix=1
)

from otsukare.gateway_identity import init_app as init_gateway_identity  # noqa: E402

init_gateway_identity(app)

import otsukare.views  # noqa: E402

# Program version and changelog. __version__ is used in setup.py
# Poetry attaches to this version via poetry-version-plugin
# Git tagging is required in addition to these changes
# See CONTRIBUTING.md for more info

__version__ = "0.2.0"  # Upgrade infra files
