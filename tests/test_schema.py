"""Schema bootstrap tests."""

import logging

from sqlalchemy import event, inspect

from otsukare import app, db
from otsukare.schema import ensure_schema


def test_fresh_database_gets_every_table(caplog):
    """A fresh database receives the complete SQLAlchemy schema."""
    with app.app_context():
        db.drop_all()

    with caplog.at_level(logging.INFO):
        ensure_schema()

    with app.app_context():
        assert set(db.metadata.tables) == set(inspect(db.engine).get_table_names())
    assert "schema ensured" in caplog.messages


def test_second_schema_ensure_emits_no_ddl():
    """A second bootstrap observes the existing schema without changing it."""
    ensure_schema()
    statements = []

    with app.app_context():
        engine = db.engine

        def capture_statement(conn, cursor, statement, parameters, context, executemany):
            statements.append(statement.strip().upper())

        event.listen(engine, "before_cursor_execute", capture_statement)
        try:
            ensure_schema()
        finally:
            event.remove(engine, "before_cursor_execute", capture_statement)

    assert not [statement for statement in statements if statement.startswith(("CREATE", "ALTER", "DROP"))]
