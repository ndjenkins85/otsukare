# Copyright © 2021 by Nick Jenkins. All rights reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from datetime import datetime

import pandas as pd

from otsukare.models import *
from otsukare.my_forms import Multichoice, WrittenResponse


def sql_table_to_excel(table, db):

    df = pd.read_sql('SELECT * from "' + table + '"', db.engine.connect().connection)

    for col in df.columns.tolist():
        df[col] = df[col].replace("NaN", "")

    df.to_excel("data/" + table + ".xlsx", index=False)


def romanji_from_kana(kana):

    kanas = Kana.query.with_entities(Kana.kana).all()
    double_kanas = [x[0] for x in kanas if len(x[0]) > 1]

    romanji_build = ""
    for i in range(len(kana)):
        kana_entry = Kana.query.filter_by(kana=kana[i]).first()
        if kana_entry:
            # handle small tsu rule; gakkou
            if kana[i] == u"\u3063" or kana[i] == u"\u30c3":
                kana_entry = Kana.query.filter_by(kana=kana[i + 1]).first()
                romanji = kana_entry.romanji[0]
            else:
                # handle kana case
                romanji = kana_entry.romanji

                # Handle double case; kyo, chu etc.
                if i < len(kana) - 1:
                    if kana[i] + kana[i + 1] in double_kanas:
                        kana_entry = Kana.query.filter_by(kana=kana[i] + kana[i + 1]).first()
                        romanji = kana_entry.romanji

            romanji_build += romanji

    return romanji_build


def get_stats(current_user):
    stats = {}
    stats["kana_parts"] = 0
    stats["words_known"] = 0
    stats["needs_percent"] = 0
    stats["yen"] = 0
    if current_user.is_authenticated:
        kana_parts = Kana_Known.query.filter_by(user_id=current_user.id).all()
        stats["kana_parts"] = sum([x.tokens for x in kana_parts])

        word_parts = Words_Known.query.filter_by(user_id=current_user.id).all()
        stats["words_known"] = sum([x.tokens for x in word_parts])

        needs_parts = Needs_Known.query.filter_by(user_id=current_user.id).all()
        stats["needs_percent"] = sum([x.tokens for x in needs_parts])
        stats["yen"] = current_user.yen

    return stats


def get_task(current_user, request=None, task_master_id=None):

    # Get Task if it exists, otherwise create task
    task_blueprint = Task_Master.query.get(task_master_id)

    task = (
        Tasks.query.join(Task_Master)
        .filter(Tasks.user_id == current_user.id, Task_Master.task_type == task_blueprint.task_type, Tasks.status == -1)
        .first()
    )

    if not task:
        make_task(current_user, task_blueprint)

    task = (
        Tasks.query.join(Task_Master)
        .filter(Tasks.user_id == current_user.id, Task_Master.task_type == task_blueprint.task_type, Tasks.status == -1)
        .first()
    )

    return form_task(task_blueprint, task, request)


def form_task(task_blueprint, task, request):

    if task.task_id == 1:
        form = Multichoice(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().romanji
        )
        form.question_english.label = ""
        form.question_lang.label = "ja"
        form.mc.choices = [
            (task.place1, eval(task_blueprint.task_type).query.filter_by(id=task.place1).first().kana),
            (task.place2, eval(task_blueprint.task_type).query.filter_by(id=task.place2).first().kana),
            (task.place3, eval(task_blueprint.task_type).query.filter_by(id=task.place3).first().kana),
            (task.place4, eval(task_blueprint.task_type).query.filter_by(id=task.place4).first().kana),
            (task.place5, eval(task_blueprint.task_type).query.filter_by(id=task.place5).first().kana),
        ]

    elif task.task_id == 2:
        form = Multichoice(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        )
        form.question_english.label = ""
        form.question_lang.label = "ja"
        form.mc.choices = [
            (task.place1, eval(task_blueprint.task_type).query.filter_by(id=task.place1).first().romanji),
            (task.place2, eval(task_blueprint.task_type).query.filter_by(id=task.place2).first().romanji),
            (task.place3, eval(task_blueprint.task_type).query.filter_by(id=task.place3).first().romanji),
            (task.place4, eval(task_blueprint.task_type).query.filter_by(id=task.place4).first().romanji),
            (task.place5, eval(task_blueprint.task_type).query.filter_by(id=task.place5).first().romanji),
        ]

    elif task.task_id == 3:
        form = Multichoice(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().romanji
        )
        form.question_english.label = eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        form.question_lang.label = "ja"
        form.mc.choices = [
            (task.place1, eval(task_blueprint.task_type).query.filter_by(id=task.place1).first().kana),
            (task.place2, eval(task_blueprint.task_type).query.filter_by(id=task.place2).first().kana),
            (task.place3, eval(task_blueprint.task_type).query.filter_by(id=task.place3).first().kana),
            (task.place4, eval(task_blueprint.task_type).query.filter_by(id=task.place4).first().kana),
            (task.place5, eval(task_blueprint.task_type).query.filter_by(id=task.place5).first().kana),
        ]

    elif task.task_id == 4:
        form = WrittenResponse(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        )
        form.question_english.label = ""
        form.question_lang.label = "ja"

    elif task.task_id == 5:
        form = WrittenResponse(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        )
        form.question_english.label = eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        form.question_lang.label = "ja"

    elif task.task_id == 6:
        form = Multichoice(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().english
        )
        form.question_english.label = ""
        form.question_lang.label = "ja"
        form.mc.choices = [
            (task.place1, eval(task_blueprint.task_type).query.filter_by(id=task.place1).first().kana),
            (task.place2, eval(task_blueprint.task_type).query.filter_by(id=task.place2).first().kana),
            (task.place3, eval(task_blueprint.task_type).query.filter_by(id=task.place3).first().kana),
            (task.place4, eval(task_blueprint.task_type).query.filter_by(id=task.place4).first().kana),
            (task.place5, eval(task_blueprint.task_type).query.filter_by(id=task.place5).first().kana),
        ]

    elif task.task_id == 7:
        form = Multichoice(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        )
        form.question_english.label = ""
        form.question_lang.label = "ja"
        form.mc.choices = [
            (task.place1, eval(task_blueprint.task_type).query.filter_by(id=task.place1).first().english),
            (task.place2, eval(task_blueprint.task_type).query.filter_by(id=task.place2).first().english),
            (task.place3, eval(task_blueprint.task_type).query.filter_by(id=task.place3).first().english),
            (task.place4, eval(task_blueprint.task_type).query.filter_by(id=task.place4).first().english),
            (task.place5, eval(task_blueprint.task_type).query.filter_by(id=task.place5).first().english),
        ]

    elif task.task_id == 8:
        form = Multichoice(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().english
        )
        form.question_english.label = eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().english
        form.question_lang.label = "en"
        form.mc.choices = [
            (task.place1, eval(task_blueprint.task_type).query.filter_by(id=task.place1).first().kana),
            (task.place2, eval(task_blueprint.task_type).query.filter_by(id=task.place2).first().kana),
            (task.place3, eval(task_blueprint.task_type).query.filter_by(id=task.place3).first().kana),
            (task.place4, eval(task_blueprint.task_type).query.filter_by(id=task.place4).first().kana),
            (task.place5, eval(task_blueprint.task_type).query.filter_by(id=task.place5).first().kana),
        ]

    elif task.task_id == 9:
        form = Multichoice(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        )
        form.question_english.label = eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        form.question_lang.label = "ja"
        form.mc.choices = [
            (task.place1, eval(task_blueprint.task_type).query.filter_by(id=task.place1).first().english),
            (task.place2, eval(task_blueprint.task_type).query.filter_by(id=task.place2).first().english),
            (task.place3, eval(task_blueprint.task_type).query.filter_by(id=task.place3).first().english),
            (task.place4, eval(task_blueprint.task_type).query.filter_by(id=task.place4).first().english),
            (task.place5, eval(task_blueprint.task_type).query.filter_by(id=task.place5).first().english),
        ]

    elif task.task_id == 10:
        form = Multichoice(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().english
        )
        form.question_english.label = eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        form.question_lang.label = "ja"
        form.mc.choices = [
            (task.place1, eval(task_blueprint.task_type).query.filter_by(id=task.place1).first().kana),
            (task.place2, eval(task_blueprint.task_type).query.filter_by(id=task.place2).first().kana),
            (task.place3, eval(task_blueprint.task_type).query.filter_by(id=task.place3).first().kana),
            (task.place4, eval(task_blueprint.task_type).query.filter_by(id=task.place4).first().kana),
            (task.place5, eval(task_blueprint.task_type).query.filter_by(id=task.place5).first().kana),
        ]

    elif task.task_id == 11:
        form = WrittenResponse(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        )
        form.question_english.label = ""
        form.question_lang.label = "ja"

    elif task.task_id == 12:
        form = WrittenResponse(request.form)
        form.question.label = (
            "What is this: " + eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        )
        form.question_english.label = eval(task_blueprint.task_type).query.filter_by(id=task.answer).first().kana
        form.question_lang.label = "ja"

    # Temp to get needs set up
    elif task.task_id == 13:
        form = WrittenResponse(request.form)
        form.question.label = "What is this: " + task.answer
        form.question_english.label = ""
        form.question_lang.label = "en"
        form.answer_lang.label = "ja-JP"

    elif task.task_id == 14:
        form = WrittenResponse(request.form)
        form.question.label = "What is this: " + task.answer
        form.question_english.label = ""
        form.question_lang.label = "ja"
        form.answer_lang.label = "en-AU"

    elif task.task_id == 15:
        form = WrittenResponse(request.form)
        form.question.label = "What is this: " + task.answer
        form.question_english.label = ""
        form.question_lang.label = "ja"
        form.answer_lang.label = "ja-JP"

    elif task.task_id == 16:
        form = WrittenResponse(request.form)
        form.question.label = "What is this: " + task.answer
        form.question_english.label = task.answer
        form.question_lang.label = "en"
        form.answer_lang.label = "ja-JP"

    elif task.task_id == 17:
        form = WrittenResponse(request.form)
        form.question.label = "What is this: " + task.answer
        form.question_english.label = task.answer
        form.question_lang.label = "ja"
        form.answer_lang.label = "en-AU"

    return form


def submit_task(current_user, answer_id_list=None, task_type=None):

    task = (
        Tasks.query.join(Task_Master)
        .filter(Tasks.user_id == current_user.id, Task_Master.task_type == task_type, Tasks.status == -1)
        .first()
    )

    if task_type == "Needs":
        correct = task.place1.replace(" ", "") == answer_id_list.replace(" ", "")
    else:
        correct = int(task.answer) in answer_id_list

    message = "Correct! " if correct else "Incorrect, "
    task.status = 1 if correct else 0

    if task_type == "Kana":
        known = Kana_Known.query.filter_by(user_id=current_user.id, kana_id=task.answer).first()
    elif task_type == "Words":
        known = Words_Known.query.filter_by(user_id=current_user.id, word_id=task.answer).first()
    elif task_type == "Needs":
        known = Needs_Known.query.filter_by(user_id=current_user.id, english=task.answer).first()

    if correct:
        if known:
            known.tokens += 1
            known.level += 1
            last_practiced = datetime.now()
        else:
            if task_type == "Kana":
                new_known = Kana_Known(
                    user_id=current_user.id, kana_id=task.answer, level=1, last_practiced=datetime.now(), tokens=1
                )
            elif task_type == "Words":
                new_known = Words_Known(
                    user_id=current_user.id, word_id=task.answer, level=1, last_practiced=datetime.now(), tokens=1
                )
            elif task_type == "Needs":
                new_known = Needs_Known(
                    user_id=current_user.id,
                    english=task.answer,
                    japanese=task.answer,
                    level=1,
                    last_practiced=datetime.now(),
                    tokens=1,
                )
            db.session.add(new_known)

    else:
        if known:
            known.tokens = known.tokens - 1 if known.tokens > 0 else 0
            known.level = 0
            last_practiced = datetime.now()
        else:
            if task_type == "Kana":
                new_known = Kana_Known(
                    user_id=current_user.id, kana_id=task.answer, level=0, last_practiced=datetime.now(), tokens=0
                )
            elif task_type == "Words":
                new_known = Words_Known(
                    user_id=current_user.id, word_id=task.answer, level=0, last_practiced=datetime.now(), tokens=0
                )
            elif task_type == "Needs":
                new_known = Needs_Known(
                    user_id=current_user.id,
                    english=task.answer,
                    japanese=task.answer,
                    level=0,
                    last_practiced=datetime.now(),
                    tokens=0,
                )
            db.session.add(new_known)

    if task_type == "Kana":
        task.response = max(answer_id_list) if int(task.answer) >= 106 else min(answer_id_list)
    elif task_type == "Words":
        task.response = answer_id_list[0]
    elif task_type == "Needs":
        task.response = answer_id_list

    task.task_ended = datetime.now()
    db.session.commit()

    # todo, update show message
    try:
        message += eval(task_type).query.get(task.answer).romanji + " is " + eval(task_type).query.get(task.answer).kana
    except:
        message += "the answer was " + task.answer

    return message


def get_words_from_needs(sent):
    terms = []
    word = ""
    capture = False
    for c in sent:
        if c == "]":
            capture = False
            terms.append(word)
            word = ""

        if capture:
            word += c

        if c == "[":
            capture = True
    return terms


def make_task(current_user, task_blueprint):

    tag = [x.tags for x in eval(task_blueprint.task_type).query.all()]

    # kana_type = ['Hiragana',"Hiragana",'Katakana']
    if task_blueprint.task_type == "Kana":
        task_type_id = "kana_id"
        df = pd.read_sql(
            'SELECT user_id, kana_id, level from "Kana_Known" WHERE user_id=\'' + str(current_user.id) + "'",
            db.engine.connect().connection,
        )
    elif task_blueprint.task_type == "Words":
        task_type_id = "word_id"
        df = pd.read_sql(
            'SELECT user_id, word_id, level from "Words_Known" WHERE user_id=\'' + str(current_user.id) + "'",
            db.engine.connect().connection,
        )
    elif task_blueprint.task_type == "Needs":
        task_type_id = "need_id"
        df = pd.read_sql(
            'SELECT user_id, need_id, level from "Needs_Known" WHERE user_id=\'' + str(current_user.id) + "'",
            db.engine.connect().connection,
        )

    answer = None
    # If there are more than 16 knowns, choose one, otherwise choose at random
    if df.shape[0] >= 16:
        proportion = ((df["level"].max() - df["level"]) + 1) ** 3
        _id = df.loc[df.sample(weights=proportion).index[0], task_type_id]
        answer = eval(task_blueprint.task_type).query.filter_by(id=str(_id)).first()

    if not answer or random.random() < 0.1:

        # Make NEEDS
        if task_blueprint.task_type == "Needs":
            answer = random.choice(eval(task_blueprint.task_type).query.all())
            words = pd.read_sql(
                'SELECT * from "Words_Known" WHERE user_id=\'' + str(current_user.id) + "'",
                db.engine.connect().connection,
            )
            all_words = pd.read_sql('SELECT * from "Words"', db.engine.connect().connection)

            for term in get_words_from_needs(answer.english):
                try:
                    replace = words[words["tags"] == term].sample(1).transpose()
                    answer.english = answer.english.replace("[" + term + "]", replace.loc["english"].values[0])
                    answer.japanese = answer.japanese.replace("[" + term + "]", replace.loc["kana"].values[0])
                except:
                    replace = all_words[all_words["tags"] == term].sample(1).transpose()
                    answer.english = answer.english.replace("[" + term + "]", replace.loc["english"].values[0])
                    answer.japanese = answer.japanese.replace("[" + term + "]", replace.loc["kana"].values[0])

            if task_blueprint.id == 13 or task_blueprint.id == 16:
                task = Tasks(
                    user_id=current_user.id,
                    task_id=task_blueprint.id,
                    answer=answer.english,
                    place1=romanji_from_kana(answer.japanese),
                    status=-1,
                    task_made=datetime.now(),
                    task_ended=None,
                )
            elif task_blueprint.id == 15:
                task = Tasks(
                    user_id=current_user.id,
                    task_id=task_blueprint.id,
                    answer=answer.japanese,
                    place1=romanji_from_kana(answer.japanese),
                    status=-1,
                    task_made=datetime.now(),
                    task_ended=None,
                )
            else:
                task = Tasks(
                    user_id=current_user.id,
                    task_id=task_blueprint.id,
                    answer=answer.japanese,
                    place1=answer.english,
                    status=-1,
                    task_made=datetime.now(),
                    task_ended=None,
                )

            db.session.add(task)
            db.session.commit()

            # Done
            return None

        elif task_blueprint.task_type == "Words":
            answer = random.choice(eval(task_blueprint.task_type).query.filter_by(tags=random.choice(tag)).all())
        else:
            if df.shape[0] >= 16:

                tags_select = [
                    "Hiragana_Basic",
                    "Hiragana_Basic",
                    "Hiragana_Basic",
                    "Hiragana_Basic",
                    "Hiragana_Basic",
                    "Hiragana_Medium",
                    "Hiragana_Medium",
                    "Hiragana_Medium",
                    "Hiragana_Hard",
                    "Katagana_Basic",
                    "Katagana_Basic",
                    "Katagana_Basic",
                    "Katagana_Basic",
                    "Katagana_Medium",
                    "Katagana_Medium",
                    "Katagana_Hard",
                ]

                answer = random.choice(
                    eval(task_blueprint.task_type).query.filter_by(tags=random.choice(tags_select)).all()
                )
            else:
                answer = random.choice(eval(task_blueprint.task_type).query.filter_by(tags="Hiragana_Basic").all())

    question_set = [answer]

    df1 = pd.read_sql(
        'SELECT task_id, answer, response from "Tasks" WHERE task_id=\''
        + str(task_blueprint.id)
        + "' AND answer!=response AND answer='"
        + str(answer.id)
        + "'",
        db.engine.connect().connection,
    )
    df2 = pd.read_sql(
        'SELECT task_id, response as answer, answer as response from "Tasks" WHERE task_id=\''
        + str(task_blueprint.id)
        + "' AND answer!=response AND response='"
        + str(answer.id)
        + "'",
        db.engine.connect().connection,
    )
    df = pd.concat([df1, df2], axis=0)
    df = df[df["answer"] != "-1"]
    df = df[df["response"] != "-1"]
    everyone_df = df["response"].value_counts() / df["response"].count()

    df1 = pd.read_sql(
        'SELECT answer, response, user_id from "Tasks" WHERE task_id=\''
        + str(task_blueprint.id)
        + "' AND user_id='"
        + str(current_user.id)
        + "' AND answer!=response AND answer='"
        + str(answer.id)
        + "'",
        db.engine.connect().connection,
    )
    df2 = pd.read_sql(
        'SELECT response as answer, answer as response, user_id from "Tasks" WHERE task_id=\''
        + str(task_blueprint.id)
        + "' AND user_id='"
        + str(current_user.id)
        + "' AND answer!=response AND response='"
        + str(answer.id)
        + "'",
        db.engine.connect().connection,
    )
    df = pd.concat([df1, df2], axis=0)
    df = df[df["answer"] != "-1"]
    df = df[df["response"] != "-1"]
    me_df = df["response"].value_counts() / df["response"].count()

    for ind, row in everyone_df.iteritems():
        if int(ind) not in [int(x.id) for x in question_set]:
            question_set.append(eval(task_blueprint.task_type).query.get(ind))
            break

    added = 0
    for ind, row in me_df.iteritems():
        if int(ind) not in [int(x.id) for x in question_set]:
            question_set.append(eval(task_blueprint.task_type).query.get(ind))
            added += 1
            print(ind)
            print(everyone_df)
        if added > 1:
            break

    while len(question_set) < 5:
        # more likely to get random ones from the same tag set
        if random.random() < 0.5:
            option = random.choice(eval(task_blueprint.task_type).query.filter_by(tags=answer.tags).all())
        else:
            option = random.choice(eval(task_blueprint.task_type).query.all())
        if option not in question_set:
            question_set.append(option)

    random.shuffle(question_set)

    task = Tasks(
        user_id=current_user.id,
        task_id=task_blueprint.id,
        answer=answer.id,
        place1=question_set[0].id,
        place2=question_set[1].id,
        place3=question_set[2].id,
        place4=question_set[3].id,
        place5=question_set[4].id,
        response=None,
        status=-1,
        task_made=datetime.now(),
        task_ended=None,
    )

    db.session.add(task)
    db.session.commit()
