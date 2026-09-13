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

from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class Add_Term_Form(FlaskForm):
    english = StringField("English", validators=[DataRequired()])
    kana = StringField("Kana", validators=[DataRequired()])
    kanji = StringField("Kanji")
    tags = StringField("Tags")
    module = SelectField("Module")
    lesson = SelectField("Lesson")
    submit = SubmitField("Add word", id="new_submit")


class Multichoice(FlaskForm):
    question = StringField()
    question_english = StringField()
    question_lang = StringField()
    mc = RadioField("Select answer:", choices=[], validators=[InputRequired()])
    # submit = SubmitField("Enter")


class WrittenResponse(FlaskForm):
    question = StringField()
    question_english = StringField()
    question_lang = StringField()
    answer_lang = StringField()
    written_response = StringField("Please enter your answer in English: ", validators=[DataRequired()])
    submit = SubmitField("Enter")


class Ask_Question_Form(FlaskForm):
    answer = StringField("What is the translation of the above term?", validators=[DataRequired()])
