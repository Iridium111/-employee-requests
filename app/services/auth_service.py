from uuid import UUID

import jwt
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token, decode_token, create_refresh_token
from app.models.user import User
from app.repositories.employee import EmployeeRepository
from app.repositories.user import UserRepository
from app.core.exceptions import (LoginAlreadyExistsError,
                                 EmailAlreadyExistsError,
                                 EmployeeAlreadyRegisteredError,
                                 EmployeeNotFoundError,
                                 InvalidCredentialsError,
                                 InvalidRefreshTokenError)
from app.schemas.user import UserCreate, LoginRequest, TokenResponse
from fastapi.concurrency import run_in_threadpool


class AuthService:
    @staticmethod
    async def register(session: AsyncSession,
                       user_data: UserCreate) -> User:
        existing_login = await UserRepository.get_by_login(session, user_data.login)
        if existing_login is not None:
            raise LoginAlreadyExistsError()

        existing_email = await UserRepository.get_by_email(session, user_data.email)
        if existing_email is not None:
            raise EmailAlreadyExistsError()

        existing_employee = await UserRepository.get_by_employee_id(session, user_data.employee_id)
        if existing_employee is not None:
            raise EmployeeAlreadyRegisteredError()

        employee = await EmployeeRepository.get_by_id(session, user_data.employee_id)
        if employee is None:
            raise EmployeeNotFoundError()

        hashed_password = await run_in_threadpool(hash_password,
                                                  user_data.password)

        return await UserRepository.create(session, user_data, hashed_password)

    @staticmethod
    async def login(session: AsyncSession,
                    credentials: LoginRequest) -> User:
        request_user = await UserRepository.get_by_login(session, credentials.login)
        if request_user is None:
            raise InvalidCredentialsError()

        if not verify_password(credentials.password, request_user.hashed_password):
            raise InvalidCredentialsError()

        return request_user

    @staticmethod
    async def refresh(session: AsyncSession,
                      refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise InvalidRefreshTokenError()

        user_id = payload.get('sub')
        if user_id is None:
            raise InvalidRefreshTokenError()

        token_type = payload.get('type')
        if token_type != 'refresh':
            raise InvalidRefreshTokenError()

        try:
            user_uuid = UUID(user_id)
        except Exception:
            raise InvalidRefreshTokenError()

        existing_user = await UserRepository.get_by_uuid(session, user_id=user_uuid)
        if existing_user is None:
            raise InvalidRefreshTokenError()

        if refresh_token != existing_user.refresh_token:
            raise InvalidRefreshTokenError()

        new_access_token = create_access_token(user_uuid)
        new_refresh_token = create_refresh_token(user_uuid)

        await UserRepository.update_refresh_token(session, user_uuid, new_refresh_token)

        return TokenResponse(access_token=new_access_token,
                             refresh_token=new_refresh_token)

    @staticmethod
    async def logout(session: AsyncSession,
                     refresh_token: str) -> None:
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise InvalidRefreshTokenError()

        user_id = payload.get('sub')
        if user_id is None:
            raise InvalidRefreshTokenError()

        try:
            user_uuid = UUID(user_id)
        except Exception:
            raise InvalidRefreshTokenError()

        user = await UserRepository.get_by_uuid(session, user_id=user_uuid)
        if user is None:
            raise InvalidRefreshTokenError()

        token_type = payload.get('type')
        if token_type != 'refresh':
            raise InvalidRefreshTokenError()

        if user.refresh_token != refresh_token:
            raise InvalidRefreshTokenError()

        await UserRepository.update_refresh_token(session, user_uuid, None)


