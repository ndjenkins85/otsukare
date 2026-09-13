"""Destructively reset Otsukare's per-user data for the Logto cut-over."""

import argparse
from typing import List, Optional

from sqlalchemy import inspect

from otsukare import app, db
from otsukare.models import Kana_Known, Needs_Known, Tasks, Users, Words, Words_Known


USER_TABLES = (Tasks, Needs_Known, Kana_Known, Words_Known, Users)


def reset_user_data() -> None:
    """Drop user-owned tables and recreate them without touching core study data."""
    with app.app_context():
        existing_tables = set(inspect(db.engine).get_table_names())
        if Words.__tablename__ in existing_tables:
            db.session.execute(db.delete(Words).where(Words.user.is_not(None)))
            db.session.commit()

        db.session.remove()
        for model in USER_TABLES:
            model.__table__.drop(db.engine, checkfirst=True)
        db.create_all()


def main(argv: Optional[List[str]] = None) -> None:
    """Require explicit confirmation before resetting all user data."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yes", action="store_true", help="confirm the irreversible user-data reset")
    args = parser.parse_args(argv)
    if not args.yes:
        parser.error("refusing to reset user data without --yes")

    reset_user_data()
    print("Otsukare user profiles and dependent progress were reset.")


if __name__ == "__main__":
    main()
