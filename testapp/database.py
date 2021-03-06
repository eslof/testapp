import os
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from sqlalchemy.orm import sessionmaker, scoped_session

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import func
from flaskapp import app
from flask_restplus import fields

# region fixes access of db file from -mzipapp .pyz
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
db_path = os.path.join(root_path, 'ledger.sqlite')
db_uri = 'sqlite:///{}'.format(db_path)
# endregion

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=db.engine))


class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(9), nullable=False, unique=True)
    expire = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String, nullable=False)


class AuthSchema(ma.Schema):
    class Meta:
        fields = ('id', 'token', 'expire', 'user')


class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_party = db.Column(db.String, nullable=False)
    second_party = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)


class LedgerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_party', 'second_party', 'amount', 'time', 'reason')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    pin = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    modified = db.Column(db.Integer, nullable=False, default=func.now())
    version = db.Column(db.Integer, nullable=False, default=0)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'pin', 'balance', 'created', 'modified', 'version')


#db.create_all()
