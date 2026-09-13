# manage.py
import argparse

import pandas as pd

from otsukare import app
from otsukare.analysis import romanji_from_kana, sql_table_to_excel
from otsukare.models import *


def create_db():
    db.create_all()


def drop_db():
    db.drop_all()


def add_db():

    df = pd.read_excel("data/hiragana.xlsx")
    for index, row in df.iterrows():
        new_term = Kana(type="Hiragana", kana=row["kana"], romanji=row["romanji"], tags=row["tags"])
        db.session.add(new_term)
    df = pd.read_excel("data/katakana.xlsx")
    for index, row in df.iterrows():
        new_term = Kana(type="Katakana", kana=row["kana"], romanji=row["romanji"], tags=row["tags"])
        db.session.add(new_term)

    kanas = Kana.query.with_entities(Kana.kana).all()
    double_kanas = [x[0] for x in kanas if len(x[0]) > 1]

    df = pd.read_excel("data/Words.xlsx")
    for index, row in df.iterrows():
        romanji_build = romanji_from_kana(row["kana"].strip())

        new_term = Words(
            english=row["english"].strip(),
            kana=row["kana"].strip(),
            kanji=row["kanji"],
            romanji=romanji_build,
            module=row["module"].strip(),
            lesson=row["lesson"],
            tags=row["tags"],
        )
        db.session.add(new_term)

    df = pd.read_excel("data/Needs.xlsx")
    for index, row in df.iterrows():
        new_term = Needs(english=row["english"], japanese=row["japanese"], tags=row["tags"])
        db.session.add(new_term)

    db.session.commit()

    df = pd.read_excel("data/Task_Master.xlsx")
    for index, row in df.iterrows():
        new_task = Task_Master(
            task_type=row["task_type"],
            input=row["input"],
            in_ja=row["in_ja"],
            output=row["output"],
            out_ja=row["out_ja"],
            difficulty=row["difficulty"],
        )
        db.session.add(new_task)
    db.session.commit()

    df = pd.read_csv("data/modules.csv")
    for term in df["modules"].tolist():
        new_term = Modules(term)
        db.session.add(new_term)
    db.session.commit()


def write_words():
    sql_table_to_excel("Words", db)


def test():
    sql_table_to_excel("Kana_Known", db)


def main():
    """Run a legacy database maintenance command."""
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["create_db", "drop_db", "add_db", "write_words", "test"])
    args = parser.parse_args()
    commands = {
        "create_db": create_db,
        "drop_db": drop_db,
        "add_db": add_db,
        "write_words": write_words,
        "test": test,
    }
    with app.app_context():
        commands[args.command]()


if __name__ == "__main__":
    main()
