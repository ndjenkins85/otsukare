import os

class BaseConfig(object):
    """Base configuration."""

    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:shihad@localhost:5432/otsukare'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # main config
    SECRET_KEY = 'my_precious'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    DEBUG = True
    # BCRYPT_LOG_ROUNDS = 13
    # WTF_CSRF_ENABLED = True
    # DEBUG_TB_ENABLED = False
    # DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    # MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    # MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    MAIL_USERNAME = "otsukare.good.work@gmail.com"
    MAIL_PASSWORD = "otsukaresamadeshita"

    # mail accounts
    MAIL_DEFAULT_SENDER = 'otsukare.good.work@gmail.com'