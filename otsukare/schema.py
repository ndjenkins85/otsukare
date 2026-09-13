"""Create any missing Otsukare database tables at container startup."""

import logging

from otsukare import app, db


LOGGER = logging.getLogger(__name__)


def ensure_schema() -> None:
    """Create missing tables without changing or deleting existing data."""
    with app.app_context():
        db.create_all()
    LOGGER.info("schema ensured")


def main() -> None:
    """Run the idempotent schema bootstrap as a module command."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    ensure_schema()


if __name__ == "__main__":
    main()
