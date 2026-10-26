from uuid import UUID

import bcrypt
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(
        password_bytes,
        salt
    )
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str,
                    hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(user_id: UUID) -> str:
    to_encode: dict[str, str | datetime] = {'sub': str(user_id)}
    expire = (datetime.now(timezone.utc)) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire, 'type': 'access'})

    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM,)
    return encoded_jwt

def create_refresh_token(user_id: UUID) -> str:
    to_encode: dict[str, str | datetime] = {'sub': str(user_id)}
    expire = (datetime.now(timezone.utc)) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({'exp': expire, 'type': 'refresh'})

    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM,)
    return encoded_jwt
def decode_token(token: str) -> dict:
    payload = jwt.decode(token,
                         settings.SECRET_KEY,
                         algorithms=[settings.ALGORITHM],
                         options={'require': ['sub', 'exp', 'type']})
    return payload