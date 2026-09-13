"""Gateway identity, authorization, and prefix behavior tests."""

import os
from datetime import datetime, timedelta, timezone

from jose import jwt

from otsukare import app
from otsukare.models import Users


PREFIX = "/projects/otsukare"


def _token(subject="user-sub", prefix=PREFIX):
    """Mint a representative signed gateway identity."""
    now = datetime.now(timezone.utc)
    claims = {
        "sub": subject,
        "email": f"{subject}@example.com",
        "name": f"Name {subject}",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=5)).timestamp()),
        "prefix": prefix,
    }
    return jwt.encode(claims, os.environ["GATEWAY_AUTH_SECRET"], algorithm="HS256")


def _headers(token):
    """Build the headers supplied by the production gateway."""
    return {
        "X-Gateway-Auth": token,
        "X-Forwarded-For": "203.0.113.10",
        "X-Forwarded-Host": "www.ndjenkins.com",
        "X-Forwarded-Prefix": PREFIX,
        "X-Forwarded-Proto": "https",
    }


def test_missing_token_is_unauthorized(client):
    """Every application route requires a gateway identity."""
    assert client.get("/").status_code == 401


def test_wrong_prefix_is_unauthorized(client):
    """A token minted for another sub-site cannot enter Otsukare."""
    response = client.get("/play", headers=_headers(_token(prefix="/projects/storymaker")))
    assert response.status_code == 401


def test_expired_token_is_unauthorized(client):
    """An expired gateway assertion cannot enter Otsukare."""
    now = datetime.now(timezone.utc)
    claims = {
        "sub": "user-sub",
        "email": "user@example.com",
        "name": "User",
        "iat": int((now - timedelta(minutes=10)).timestamp()),
        "exp": int((now - timedelta(minutes=5)).timestamp()),
        "prefix": PREFIX,
    }
    token = jwt.encode(claims, os.environ["GATEWAY_AUTH_SECRET"], algorithm="HS256")

    assert client.get("/play", headers=_headers(token)).status_code == 401


def test_valid_token_creates_local_user(client):
    """The first valid request creates a profile keyed by Logto subject."""
    response = client.get("/play", headers=_headers(_token()))

    assert response.status_code == 200
    with app.app_context():
        user = Users.query.filter_by(logto_sub="user-sub").one()
        assert user.username == "Name user-sub"
        assert user.email == "user-sub@example.com"


def test_static_urls_include_forwarded_prefix(client):
    """Flask-generated static URLs remain inside the gateway mount."""
    response = client.get("/play", headers=_headers(_token()))

    assert b'href="/projects/otsukare/static/styles/main.css"' in response.data
    assert b'href="/projects/otsukare/"' in response.data


def test_recorder_urls_include_forwarded_prefix(client):
    """Recorder JavaScript receives application-prefixed endpoint URLs."""
    response = client.get("/record", headers=_headers(_token()))

    assert b'window.OTSUKARE_RECORD_URL = "/projects/otsukare/record"' in response.data
    assert b'window.OTSUKARE_RECORDER_WORKER_URL = "/projects/otsukare/static/js/recorderWorker.js"' in response.data


def test_admin_gate_uses_configured_logto_subject(client):
    """Only the configured Logto subject can open admin routes."""
    denied = client.get("/add_word", headers=_headers(_token(subject="ordinary-sub")))
    allowed = client.get("/add_word", headers=_headers(_token(subject="admin-sub")))

    assert denied.status_code == 403
    assert allowed.status_code == 200


def test_healthz_is_open(client):
    """Railway can check liveness without gateway identity."""
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_session_cookie_configuration():
    """The session cookie cannot collide with another sub-site."""
    assert app.config["SESSION_COOKIE_NAME"] == "otsukare_session"
    assert app.config["SESSION_COOKIE_PATH"] == PREFIX
    assert app.config["SESSION_COOKIE_SECURE"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
