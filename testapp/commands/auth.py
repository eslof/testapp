import string
from datetime import datetime, timedelta
from random import choices
from typing import Optional

from database import Auth, User, UserSchema, Session


def login(user_name: str, pin: int) -> str:
    session = Session()
    user = get_user(session, user_name)
    if not user:
        if not new_user(session, user_name, pin):
            session.rollback()
            return f'Unable to create new user: {user_name}'
        else:
            session.commit()
    elif user['pin'] != pin:
        return f'Wrong pin for user: {user_name}'

    token = new_auth(session, user_name)
    if not token:
        session.rollback()
        return f'Unable to produce token for: {user_name}'

    session.commit()
    session.close()
    return f'Session token: {token}'


def logout(token: str) -> str:
    session = Session()
    try:
        session.query(Auth).filter(
            Auth.token == token
        ).filter(
            Auth.expire > datetime.utcnow()
        ).update({"expire": datetime.utcnow()})
    except:
        session.rollback()
        return f'Token failure (expired or otherwise): {token}'

    session.commit()
    session.close()
    return f'Token invalidated: {token}'


def new_user(s, user_name: str, pin: int) -> bool:
    try:
        s.add(User(name=user_name, pin=pin))
    except:
        return False
    return True


def new_auth(s, user_name: str) -> Optional[str]:
    token = generate_token()
    try:
        # TODO: should probably check if the token is unique
        s.add(Auth(
            token=token,
            expire=datetime.utcnow() + timedelta(days=7),
            user=user_name
        ))
    except:
        return None
    return token


def generate_token() -> str:
    # TODO: this is incredibly unsafe
    return "".join(choices("".join([string.ascii_letters, string.digits]), k=9))


def get_user(s: Session, name: str) -> Optional[User]:
    try:
        return UserSchema().dump(s.query(User).filter(User.name == name).order_by(User.version.desc()).first())
    except:
        return None
