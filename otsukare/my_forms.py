from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired
from otsukare.models import db, Users

class Signup_Form(Form):
    username = StringField("Choose a username", 
        validators=[DataRequired("Please enter a username"),
                    Length(min=6, max=25)])
    email = StringField("Email address", 
        validators=[DataRequired("Please enter your email"),
                    Email("Please enter a valid email"),
                    Length(max=50)])
    password = PasswordField("Password", 
        validators=[DataRequired("Please enter a password"),
                    Length(min=6, max=25, message="Passwords must be a minimum of 6 characters")])
    password_two = PasswordField("Confirm Password", 
        validators=[DataRequired("Please confirm your password"),
                    EqualTo('password', message='Passwords must match.')])
    submit = SubmitField("Sign up")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
        self.em = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = Users.query.filter_by(username=self.username.data.title()).first()
        if user:
            self.username.errors.append('Username already exists')
            return False

        em = Users.query.filter_by(email=self.email.data.lower()).first()
        if em:
            self.email.errors.append('Email already exists')
            return False

        self.user = user
        self.em = em
        return True

class Login_Form(Form):
    username = StringField("Username", 
        validators=[DataRequired("Please your username"),
                    Length(min=6, max=25)])
    password = PasswordField("Password", 
        validators=[DataRequired("Please enter a password"),
                    Length(min=6, max=25, message="Passwords must be a minimum of 6 characters")])
    submit = SubmitField("Sign in")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        # self.user = None
        # self.pw = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = Users.query.filter_by(username=self.username.data.title()).first()
        if not user:
            self.username.errors.append('Username or password combination does not exist - Please ensure you are entering your username and not your email')
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append('Username or password combination does not exist  - Please ensure you are entering your username and not your email')
            return False

        # self.user = user
        # self.pw = pw
        return True

class Add_Term_Form(Form):
    english = StringField("English", validators=[DataRequired()])
    kana = StringField("Kana", validators=[DataRequired()])
    kanji = StringField("Kanji")
    tags = StringField("Tags")
    module = SelectField("Module")
    lesson = SelectField("Lesson")
    submit = SubmitField("Add word", id="new_submit")


class Multichoice(Form):
    question = StringField()
    question_english = StringField()
    question_lang = StringField()
    mc = RadioField("Select answer:", choices=[], validators=[InputRequired()])
    #submit = SubmitField("Enter")

class WrittenResponse(Form):
    question = StringField()
    question_english = StringField()
    question_lang = StringField()
    answer_lang = StringField()
    written_response = StringField("Please enter your answer in English: ", validators=[DataRequired()])
    submit = SubmitField("Enter")

class Ask_Question_Form(Form):
    answer = StringField("What is the translation of the above term?", validators=[DataRequired()])