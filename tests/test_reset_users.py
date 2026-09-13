"""Guard and data-boundary tests for the one-shot user reset."""

import pytest

from otsukare import app, db
from otsukare.models import Modules, Users, Words, Words_Known
from scripts.reset_users import main, reset_user_data


def test_reset_requires_yes_flag():
    """The destructive reset refuses to run without explicit confirmation."""
    with pytest.raises(SystemExit):
        main([])


def test_reset_removes_user_data_but_preserves_study_data():
    """The reset recreates user tables without deleting core curriculum rows."""
    with app.app_context():
        module = Modules("Basics")
        user = Users("subject", "Name", "name@example.com")
        word = Words(english="hello", kana="こんにちは", module="Basics", lesson=1, user="1")
        db.session.add_all([module, user, word])
        db.session.flush()
        db.session.add(Words_Known(user_id=user.id, word_id=word.id, level=1))
        db.session.commit()

    reset_user_data()

    with app.app_context():
        assert Users.query.count() == 0
        assert Words_Known.query.count() == 0
        assert Modules.query.filter_by(modules="Basics").one()
        assert Words.query.filter(Words.user.is_not(None)).count() == 0
