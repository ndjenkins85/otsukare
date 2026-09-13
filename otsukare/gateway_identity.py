"""Verify identity asserted by the ndjenkins.com gateway."""

import os
from typing import Any, Dict

from flask import Flask, abort, g, request
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from werkzeug.local import LocalProxy

from otsukare.prefix import EXPECTED_PREFIX


REQUIRED_CLAIMS = {"sub", "email", "name", "iat", "exp", "prefix"}
current_user = LocalProxy(lambda: g.user)


def gateway_identity() -> Dict[str, Any]:
    """Verify and return the current gateway identity.

    Returns:
        Authenticated gateway claims.
    """
    token = request.headers.get("X-Gateway-Auth", "")
    secret = os.environ.get("GATEWAY_AUTH_SECRET", "")
    if not token or not secret:
        abort(401)

    try:
        claims = jwt.decode(token, secret, algorithms=["HS256"])
    except JWTError:
        abort(401)

    if claims.get("prefix") != EXPECTED_PREFIX or not REQUIRED_CLAIMS <= claims.keys():
        abort(401)
    if not all(isinstance(claims[name], str) for name in ("sub", "email", "name")):
        abort(401)
    return claims


def _load_or_create_user(claims: Dict[str, Any]):
    """Resolve the local profile using the immutable Logto subject."""
    from otsukare import db
    from otsukare.models import Users

    user = Users.query.filter_by(logto_sub=claims["sub"]).first()
    if user is None:
        user = Users(logto_sub=claims["sub"], username=claims["name"], email=claims["email"])
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            user = Users.query.filter_by(logto_sub=claims["sub"]).one()
        return user

    changed = user.username != claims["name"] or user.email != claims["email"]
    if changed:
        user.username = claims["name"]
        user.email = claims["email"]
        db.session.commit()
    return user


def init_app(app: Flask) -> None:
    """Install gateway authentication and the compatibility user proxy."""

    @app.before_request
    def load_gateway_user() -> None:
        """Require identity and load its per-application user profile."""
        if request.endpoint == "healthz":
            return

        claims = gateway_identity()
        g.identity = claims
        g.user = _load_or_create_user(claims)

    @app.context_processor
    def current_user_context() -> Dict[str, Any]:
        """Expose the Flask-g-backed compatibility user to templates."""
        return {"current_user": current_user}
