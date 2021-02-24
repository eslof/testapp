from datetime import datetime
from typing import Optional

from database import User, Auth, AuthSchema, UserSchema, Session, Ledger


def balance(token: str):
    session = Session()
    user_name = validate_token(session, token)
    if not user_name:
        return f'Token failure (expired or otherwise): {token}'

    user = get_user(session, user_name)
    if not user:
        return f'Unable to get user: {user_name}'

    session.close()
    return user['balance']


def deposit(token: str, amount: int):
    session = Session()
    user_name = validate_token(session, token)
    if not user_name:
        return f'Token failure (expired or otherwise): {token}'

    user = get_user(session, user_name)
    if not user:
        return f'Unable to get user: {user_name}'

    new_balance = user['balance'] + amount
    user_revision = User(
        name=user['name'],
        pin=user['pin'],
        balance=new_balance,
        version=user['version'] + 1)
    ledger_entry = Ledger(
        first_party='ATM',
        second_party=user['name'],
        amount=amount, time=datetime.utcnow())
    try:
        session.add_all((user_revision, ledger_entry))
    except:
        session.rollback()
        return f'Update user failure for withdraw.'

    session.commit()
    session.close()
    return f'Deposit success, new balance: {new_balance}'


def withdraw(token: str, amount: int):
    session = Session()
    user_name = validate_token(session, token)
    if not user_name:
        return f'Token failure (expired or otherwise): {token}'

    user = get_user(session, user_name)
    if not user:
        return f'Unable to get user: {user_name}'

    if user['balance'] < amount:
        return f'Insufficient funds, balance: {user["balance"]}'

    new_balance = user['balance'] - amount
    user_revision = User(
        name=user['name'],
        pin=user['pin'],
        balance=new_balance,
        version=user['version'] + 1)
    ledger_entry = Ledger(
        first_party=user['name'],
        second_party='ATM',
        amount=amount, time=datetime.utcnow())
    try:
        session.add_all((user_revision, ledger_entry))
    except:
        session.rollback()
        return f'Unable to update user for withdraw.'

    session.commit()
    session.close()
    return f'Withdraw success, new balance: {new_balance}'


def get_user(s: Session, name: str) -> Optional[User]:
    try:
        return UserSchema().dump(s.query(User).filter(User.name == name).order_by(User.version.desc()).first())
    except:
        return None


def validate_token(s: Session, token: str) -> Optional[str]:
    try:
        result = AuthSchema().dump(s.query(Auth.user).filter(Auth.expire > datetime.utcnow()).filter(Auth.token == token).order_by(Auth.expire.desc()).first())
        return result['user']
    except:
        return None
