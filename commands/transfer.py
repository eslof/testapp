from datetime import datetime
from typing import Optional

from database import Ledger, User, Auth, Session, AuthSchema, UserSchema


def do_transfer(token: str, second_party: str, amount: int) -> str:
    session = Session()
    first_party_name = validate_token(session, token)
    if not first_party_name:
        return f'Token failure (expired or otherwise): {token}'

    first_party_user = get_user(session, first_party_name)
    if not first_party_user:
        return f'Unable to get user: {first_party_name}'

    balance = first_party_user['balance']
    if balance < amount:
        return f'Insufficient funds: {first_party_user["balance"]}'

    second_party_user = get_user(session, second_party)
    if not second_party_user:
        return f'Unable to get user: {second_party}'

    if not do_transaction(session, amount, first_party_user, second_party_user):
        session.rollback()
        return f'Unable to complete transaction'

    session.commit()
    session.close()
    return f'Transfer complete, new balance: {balance-amount}'


def do_transaction(s: Session, amount: int, first_party: User, second_party: User) -> bool:
    ledger_entry = Ledger(
        first_party=first_party['name'],
        second_party=second_party['name'],
        amount=amount, time=datetime.utcnow())

    first_party_revision = User(
        name=first_party['name'],
        pin=first_party['pin'],
        balance=first_party['balance'] - amount,
        version=first_party['version']+1)
    second_party_revision = User(
        name=second_party['name'],
        pin=second_party['pin'],
        balance=second_party['balance'] + amount,
        version=second_party['version'] + 1)
    try:
        s.add_all((ledger_entry, first_party_revision, second_party_revision))
    except:
        return False
    return True


def validate_token(s: Session, token: str) -> Optional[str]:
    try:
        result = AuthSchema().dump(s.query(Auth.user).filter(Auth.expire > datetime.utcnow()).filter(Auth.token == token).order_by(Auth.expire.desc()).first())
    except:
        return None

    return result['user']


def get_user(s: Session, name: str) -> Optional[User]:
    try:
        result = UserSchema().dump(s.query(User).filter(User.name == name).order_by(User.version.desc()).first())
    except:
        return None

    return result
