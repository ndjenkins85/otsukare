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

import os


class BaseConfig(object):
    """Base configuration."""

    if os.environ.get("DATABASE_URL") is None:
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:shihad@localhost:5432/otsukare"
    else:
        SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

    # main config
    SECRET_KEY = "my_precious"
    SECURITY_PASSWORD_SALT = "my_precious_two"
    DEBUG = True
    # BCRYPT_LOG_ROUNDS = 13
    # WTF_CSRF_ENABLED = True
    # DEBUG_TB_ENABLED = False
    # DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    # MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    # MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    MAIL_USERNAME = "otsukare.good.work@gmail.com"
    MAIL_PASSWORD = "otsukaresamadeshita"

    # mail accounts
    MAIL_DEFAULT_SENDER = "otsukare.good.work@gmail.com"
