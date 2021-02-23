import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.util.compat import contextmanager

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import func
from flaskapp import app
from flask_restplus import fields

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ledger.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)


Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=db.engine))


#@contextmanager
#def session_scope():
#    session = Session()
#    try:
#        yield session
#        session.commit()
#    except:
#        session.rollback()
#        raise
#    finally:
#        session.close()


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
