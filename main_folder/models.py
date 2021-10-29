from datetime import datetime
from pytz import unicode
from . import db


class User(db.Document):
    email = db.EmailField(max_length=40, blank=False, unique=True,
                          error_messages={'required': 'Please provide your email address.',
                                          'unique': 'An account with this email exist.'}, )
    password = db.StringField(max_length=200)
    name = db.StringField(max_length=20, blank=False)
    surname = db.StringField(max_length=20, blank=False)
    is_active = False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.name


class Currency(db.Document):
    currency_code = db.IntField()
    code = db.StringField(max_length=5, blank=False)
    name = db.StringField(max_length=40, blank=False)
    rate = db.FloatField()
    date = db.DateTimeField(default=datetime.now, blank=True)

    def __repr__(self):
        return '<Currency %r>' % self.name


class BlackJWTList(db.Document):
    data = db.StringField()
