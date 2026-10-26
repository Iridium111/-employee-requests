from uuid import UUID

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.core.security import decode_token
from app.models.user import User
from app.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme),
                           session: AsyncSession = Depends(get_async_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode_token(token)

        if payload.get('type') != 'access':
            raise credentials_exception

        user_id = UUID(payload['sub'])

    except (jwt.InvalidTokenError, ValueError, KeyError):
        raise credentials_exception

    user = await UserRepository.get_by_uuid(
        session=session,
        user_id=user_id
    )
    if user is None:
        raise credentials_exception

    return user
