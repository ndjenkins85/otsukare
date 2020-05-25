from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
import random
from otsukare import db

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.INT, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(120))

    admin = db.Column(db.Boolean, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    yen = db.Column(db.INT)
    icon = db.Column(db.String(10))
    
    def __init__(self, username, email, password, 
                admin=False, confirmed=False, confirmed_on=None,
                yen=0, xp=0, icon=None):
        self.username = username.title()
        self.email = email.lower()
        self.set_password(password)

        self.admin = admin
        self.registered_on = datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        
        self.yen = yen
        self.icon = random.choice(["br","gr","lr","pr","rr","yr"])


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Modules(db.Model):
    __tablename__ = 'Modules'
    index = db.Column(db.Integer, primary_key=True)
    modules = db.Column(db.String(100), unique=True)
    
    def __init__(self, modules=None):
        self.modules = modules

        
class Words(db.Model):
    __tablename__ = 'Words'
    id = db.Column(db.INT, primary_key=True)
    english = db.Column(db.String(100), nullable=False)
    kana = db.Column(db.String(100), nullable=False)
    kanji = db.Column(db.String(100))
    romanji = db.Column(db.String(100))
    tags = db.Column(db.String(250))
    module = db.Column(db.String(100), nullable=False)
    lesson = db.Column(db.INT, nullable=False)
    user = db.Column(db.String(100))
    added_on = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, english=None, kana=None, kanji=None, romanji=romanji, tags=None,
        module=None, lesson=None, user=None, added_on=datetime.now()):
        self.english = english
        self.kana = kana
        self.kanji = kanji
        self.romanji = romanji
        self.tags = tags
        self.module = module
        self.lesson = lesson
        self.user = user
        self.added_on = added_on        


class Words_Known(db.Model):
    __tablename__ = 'Words_Known'
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.INT, db.ForeignKey('Users.id'))
    word_id = db.Column(db.INT, db.ForeignKey('Words.id'))
    level = db.Column(db.INT, nullable=False)
    last_practiced = db.Column(db.DateTime, nullable=True)
    tokens = db.Column(db.INT)

    def __init__(self, user_id=None, word_id=None, 
        level=0, last_practiced=datetime.now(), tokens=None):
        self.user_id = user_id
        self.word_id = word_id
        self.level = level
        self.last_practiced = last_practiced
        self.tokens = tokens


class Kana(db.Model):
    __tablename__ = 'Kana'
    id = db.Column(db.INT, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    kana = db.Column(db.String(100), nullable=False)
    romanji = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.String(250))

    def __init__(self, type=None, kana=None, romanji=None, tags=None):
        self.type = type
        self.kana = kana
        self.romanji = romanji
        self.tags = tags


class Kana_Known(db.Model):
    __tablename__ = 'Kana_Known'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.INT, db.ForeignKey('Users.id'))
    kana_id = db.Column(db.INT, db.ForeignKey('Kana.id'))
    level = db.Column(db.INT, nullable=False)
    last_practiced = db.Column(db.DateTime, nullable=True)
    tokens = db.Column(db.INT)
    
    def __init__(self, user_id=None, kana_id=None,  
                 level=0, last_practiced=datetime.now(), tokens=None):
        self.user_id = user_id
        self.kana_id = kana_id
        self.level = level
        self.last_practiced = last_practiced
        self.tokens = tokens


class Task_Master(db.Model):
    __tablename__ = 'Task_Master'
    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.String(100), nullable=False)
    input = db.Column(db.String(100), nullable=False)
    in_ja = db.Column(db.String(100), nullable=False)
    output = db.Column(db.String(100), nullable=False)
    out_ja = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.INT, nullable=False)
    
    def __init__(self, task_type = None, 
        input = None, in_ja = None, output = None, out_ja = None, difficulty = None):
        self.task_type = task_type
        self.input = input
        self.in_ja = in_ja
        self.output = output
        self.out_ja = out_ja
        self.difficulty = difficulty


class Tasks(db.Model):
    __tablename__ = 'Tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.INT, db.ForeignKey('Users.id'))
    task_id = db.Column(db.INT, db.ForeignKey('Task_Master.id'))
    answer = db.Column(db.String(200), nullable=False)
    place1 = db.Column(db.String(200))
    place2 = db.Column(db.String(200))
    place3 = db.Column(db.String(200))
    place4 = db.Column(db.String(200))
    place5 = db.Column(db.String(200))

    response = db.Column(db.String(200))
    status = db.Column(db.INT, nullable=False)
    task_made = db.Column(db.DateTime, nullable=False)
    task_ended = db.Column(db.DateTime)
    
    def __init__(self, user_id = None, task_id = None, answer = None,
        place1 = None, place2 = None, place3 = None, place4 = None, place5 = None,
        response = None, status = -1, task_made = datetime.now(), task_ended = None):

        self.user_id = user_id
        self.task_id = task_id
        self.answer = answer

        self.place1 = place1
        self.place2 = place2
        self.place3 = place3
        self.place4 = place4
        self.place5 = place5

        self.response = response
        self.status = status
        self.task_made = task_made
        self.task_ended = task_ended


class Needs(db.Model):
    __tablename__ = 'Needs'
    id = db.Column(db.INT, primary_key=True)
    english = db.Column(db.String(500), nullable=False)
    japanese = db.Column(db.String(500), nullable=False)
    tags = db.Column(db.String(250))

    def __init__(self, english=None, japanese=None, tags=None):
        self.type = type
        self.english = english
        self.japanese = japanese
        self.tags = tags


class Needs_Known(db.Model):
    __tablename__ = 'Needs_Known'
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.INT, db.ForeignKey('Users.id'))
    need_id = db.Column(db.INT, db.ForeignKey('Needs.id'))
    english = db.Column(db.String(500), nullable=False)
    japanese = db.Column(db.String(500), nullable=False)
    level = db.Column(db.INT, nullable=False)
    last_practiced = db.Column(db.DateTime, nullable=True)
    tokens = db.Column(db.INT)

    def __init__(self, user_id=None, need_id=None, english=None, japanese=None,
        level=0, last_practiced=datetime.now(), tokens=None):
        self.user_id = user_id
        self.need_id = need_id
        self.english = english
        self.japanese = japanese
        self.level = level
        self.last_practiced = last_practiced
        self.tokens = tokens



