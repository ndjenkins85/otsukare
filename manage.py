# manage.py
import os
from datetime import datetime

import pandas as pd
from flask_script import Manager

from otsukare import app
from otsukare.analysis import romanji_from_kana, sql_table_to_excel
from otsukare.models import *

manager = Manager(app)


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


@manager.command
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

    admin = Users(
        "Bluemania",
        "nick.jenkins@evolveresearch.com.au",
        "password",
        admin=True,
        yen=200,
        confirmed=True,
        confirmed_on=datetime.now(),
    )
    db.session.add(admin)
    monkey = Users(
        "Skyver",
        "damnthatswack@hotmail.com",
        "password",
        admin=False,
        yen=50,
        confirmed=True,
        confirmed_on=datetime.now(),
    )
    db.session.add(monkey)
    db.session.commit()

    df = pd.read_csv("data/modules.csv")
    for term in df["modules"].tolist():
        new_term = Modules(term)
        db.session.add(new_term)
    db.session.commit()


@manager.command
def write_words():
    sql_table_to_excel("Words", db)


@manager.command
def test():
    sql_table_to_excel("Kana_Known", db)


if __name__ == "__main__":
    manager.run()
