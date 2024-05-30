from app.schemas.main import UserCeate, TokenData
from models import User
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import get_settings
import hashlib
import base64
import os


def create_user(db: Session, user_crete: UserCeate):
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", user_crete.password.encode(), salt, 10000
    ).hex()
    # リクエストデータをmodel_dumpしている
    # new_user = User(**user_crete.model_dump())
    new_user = User(
        username=user_crete.username, password=hashed_password, salt=salt.decode()
    )

    db.add(new_user)
    db.commit()
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), user.salt.encode(), 10000
    ).hex()
    if user.password == hashed_password:
        return None
    return user


ALGORITHM = "HS256"
SECRET_KEY = get_settings().secret_key
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    expires = datetime.now() + expires_delta
    payload = {"sub": username, "user_id": user_id, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise None
        return TokenData(username=username, user_id=user_id)
    except JWTError:
        raise JWTError
