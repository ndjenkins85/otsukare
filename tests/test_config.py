"""Production configuration safety tests."""

import pytest

from otsukare import app
from otsukare.config import _required_env


def test_required_environment_variable_fails_fast(monkeypatch):
    """Missing required configuration stops application startup."""
    monkeypatch.delenv("REQUIRED_TEST_VALUE", raising=False)

    with pytest.raises(RuntimeError, match="REQUIRED_TEST_VALUE must be set"):
        _required_env("REQUIRED_TEST_VALUE")


def test_debug_is_disabled():
    """Production debug mode stays disabled."""
    assert app.config["DEBUG"] is False
