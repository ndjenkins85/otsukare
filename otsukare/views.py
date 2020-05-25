# coding: utf-8
from flask import Flask, flash, render_template, redirect, url_for, request, jsonify, session, make_response
import pandas as pd
import os
import random
import json
from datetime import datetime

from otsukare import app
from otsukare.my_forms import *
from otsukare.models import *
from otsukare.make_token import *
from otsukare.email import send_email
from otsukare.analysis import *

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/')
def home():

    kana_known = pd.read_sql('SELECT * from "Kana_Known"', db.engine.connect().connection)[["user_id","tokens"]].groupby("user_id").sum()
    kana_known.columns = ["Kana"]
    words_known = pd.read_sql('SELECT * from "Words_Known"', db.engine.connect().connection)[["user_id","tokens"]].groupby("user_id").sum()
    words_known.columns = ["Words"]
    sent_known = pd.read_sql('SELECT * from "Needs_Known"', db.engine.connect().connection)[["user_id","tokens"]].groupby("user_id").sum()
    sent_known.columns = ["Sentences"]
    usernames = pd.read_sql('SELECT * from "Users"', db.engine.connect().connection).set_index("id")[["username"]]
    usernames.columns = ["Username"]
    table = usernames.join(kana_known).join(words_known).join(sent_known).fillna(0)

    table = table.set_index("Username")
    for col in table.columns:
        table[col] = table[col].astype(int)

    html = (
    table.style
    .set_properties(**{'font-size': '9pt', 'font-family': 'Calibri', 'text-align':'center'})
    .set_table_attributes('class="dataframe table table-hover table-bordered"')
    .render()
    )    

    return render_template('index.html', table=html)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup_Form(request.form)
    if request.method == "POST":
        if form.validate():      
            add_new_user = Users(form.username.data,
                                form.email.data,
                                form.password.data)     
            db.session.add(add_new_user)
            db.session.commit()

            session['email'] = add_new_user.email
            token = generate_confirmation_token(add_new_user.email)

            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', 
                                    confirm_url=confirm_url, 
                                    username=add_new_user.username)
            subject = "Please confirm your email"
            send_email(add_new_user.email, subject, html)

            flash('Successfully signed up. Please check your email (and Junk folder) to complete the validation step.')
            return redirect(url_for('home'))

    return render_template('signup.html', form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
    user = Users.query.filter_by(email=email).first()
    if user.confirmed:
        flash('Account already confirmed. Please login.')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form(request.form)
    
    if request.method == "POST":
        if form.validate():      
            user = Users.query.filter_by(username=form.username.data.title()).first()
            login_user(user)
            flash('Logged in as ' + user.username.title() + '. Welcome!')
            return redirect(url_for('home'))
            
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out. See you soon!")
    return redirect(url_for('home'))

@app.route('/leaderboard')
def leaderboard():
    flash("This page is work in progress")
    leaders = (Users.query.filter_by(confirmed=True).
                with_entities(Users.icon, Users.username, Users.yen, Users.admin).
                order_by(Users.yen.desc()))
    return render_template('leaderboard.html', leaders=leaders)

@app.route('/delete_user')
@login_required
def delete_user():
    if not current_user.admin:
        flash("Admin only page requested, redirecting")
        return redirect(url_for('home'))

    username = request.args.get("username")
    delete_user = Users.query.filter_by(username=username).first()
    db.session.delete(delete_user)
    db.session.commit()    

    flash('User ' + username + ' deleted')
    return redirect(url_for('leaderboard'))

@app.route('/add_word', methods=['GET', 'POST'])
@login_required
def add_word():
    if not current_user.admin:
        flash("Admin only page requested, redirecting")
        return redirect(url_for('home'))

    form = Add_Term_Form(request.form)
    form.module.choices = [(x.modules, x.modules) for x in Modules.query.all()]
    form.lesson.choices = [(str(x),str(x)) for x in list(range(1,9))]  

    

    if form.validate_on_submit():
        romanji = romanji_from_kana(form.kana.data)

        add_new_word = Words(english=form.english.data, 
                             kana=form.kana.data, 
                             kanji=form.kanji.data,
                             tags=form.tags.data,
                             romanji=romanji,
                             module=form.module.data, 
                             lesson=form.lesson.data, 
                             user=current_user.id,
                             added_on=datetime.now())
        db.session.add(add_new_word)
        db.session.commit()
        flash("Term " + form.english.data + " added successfully")

    return render_template('add_word.html', form=form)


@app.route('/view_words')
@login_required
def view_words():
    if not current_user.admin:
        flash("Admin only page requested, redirecting")
        return redirect(url_for('home'))
    words = Words.query.all()
    return render_template('words.html', words=words)

@app.route('/save_words')
@login_required
def save_words():
    if not current_user.admin:
        flash("Admin only page requested, redirecting")
        return redirect(url_for('home'))
    try:
        sql_table_to_excel("Words", db)
        flash("Words saved to excel")
    except:
        flash("Unable to save words, error!")
    return redirect(url_for('add_word'))



@app.route('/delete_word')
@login_required
def delete_word():
    if not current_user.admin:
        flash("Admin only page requested, redirecting")
        return redirect(url_for('home'))

    word_id = request.args.get("word_id")
    delete_word = Words.query.filter_by(id=word_id).first()
    db.session.delete(delete_word)
    db.session.commit()    

    flash('Word ' + delete_word.english + ' deleted')
    return redirect(url_for('view_words'))

@app.route('/play')
def play():
    stats = get_stats(current_user)
    return render_template('how_to_play.html', stats=stats)


@app.route('/learn_kana', methods=['GET', 'POST'])
@login_required
def learn_kana():

    form = get_task(current_user, request=request, task_master_id=random.choice([1,2,3,4,5]))

    if form.validate_on_submit():
        if hasattr(form, "mc"):
            answer_id_list = [int(form.mc.data)]
        elif hasattr(form, "written_response"):
            answer_string = form.written_response.data.lower().strip()
            answer = Kana.query.filter_by(romanji=answer_string).all()
            if len(answer)>0:
                answer_id_list = [int(x.id) for x in answer]
            else:
                answer_id_list = [-1]

        message = submit_task(current_user, answer_id_list=answer_id_list, task_type="Kana")

        flash(message)
        return redirect(url_for("learn_kana"))

    return render_template('game.html', stats=get_stats(current_user), form=form)

@app.route('/learn_words', methods=['GET', 'POST'])
@login_required
def learn_words():

    form = get_task(current_user, request=request, task_master_id=random.choice([6,7,8,9,10,11,12]))     

    if form.validate_on_submit():
        if hasattr(form, "mc"):
            answer_id_list = [int(form.mc.data)]
        elif hasattr(form, "written_response"):
            answer_string = form.written_response.data.lower().strip()
            answer = Words.query.filter_by(english=answer_string).all()
            if len(answer)>0:
                answer_id_list = [int(x.id) for x in answer]
            else:
                answer_id_list = [-1]

        message = submit_task(current_user, answer_id_list=answer_id_list, task_type="Words")
        flash(message)
        return redirect(url_for("learn_words"))

    return render_template('game.html', stats=get_stats(current_user), form=form)

@app.route('/learn_sentences', methods=['GET', 'POST'])
@login_required
def learn_sentences():
    form = get_task(current_user, request=request, task_master_id=random.choice([13,14,15,16,17])) 

    if form.validate_on_submit():
        if hasattr(form, "written_response"):
            answer_string = form.written_response.data.lower().strip()

        message = submit_task(current_user, answer_id_list=answer_string, task_type="Needs")
        flash(message)
        return redirect(url_for("learn_sentences"))

    return render_template('game_record.html', stats=get_stats(current_user), form=form)

@app.route('/learn_key_phrases')
@login_required
def learn_tasks():

    flash("Not implemented")
    return redirect(url_for("how_to_play"))


    form = None
    return render_template('game.html', stats=get_stats(current_user), form=form)

@app.route('/stats_kana')
@login_required
def stats_kana():

    flash("Not implemented")
    return redirect(url_for("how_to_play"))

    stat_info = None
    return render_template('stats.html', stats=get_stats(current_user), stat_info=stat_info)

@app.route('/stats_words')
@login_required
def stats_words():

    flash("Not implemented")
    return redirect(url_for("how_to_play"))

    stat_info = None
    return render_template('stats.html', stats=get_stats(current_user), stat_info=stat_info)

@app.route('/stats_needs')
@login_required
def stats_needs():

    flash("Not implemented")
    return redirect(url_for("how_to_play"))

    stat_info = None
    return render_template('stats.html', stats=get_stats(current_user), stat_info=stat_info)

@app.route('/stats_tasks')
@login_required
def stats_tasks():

    flash("Not implemented")
    return redirect(url_for("how_to_play"))
    
    stat_info = None
    return render_template('stats.html', stats=get_stats(current_user), stat_info=stat_info)


@app.route('/record', methods=['GET', 'POST'])
def record_audio():
    """Record audio from user and capture data, including title and blob."""
    posted = "nothing yet"

    if request.method == 'POST':
        posted = request.values.get("output")

    return render_template('record.html', posted=posted)