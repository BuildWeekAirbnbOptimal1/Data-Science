from flask_sqlalchemy import SQLAlchemy
from .app import DB


class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    user_name = DB.Column(DB.String(15), default='')
    password = DB.Column(DB.PickleType, nullable = False)
    def __repr__(self):
        return '<User {} was created>'.format(self.user_name)


class functionx(DB.Model):

    def __repr__(self):
        return ''
