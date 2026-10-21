from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.employee import EmployeeRepository
from app.repositories.user import UserRepository
from app.core.exceptions import (LoginAlreadyExistsError,
                                 EmailAlreadyExistsError,
                                 EmployeeAlreadyRegisteredError,
                                 EmployeeNotFoundError)
from app.schemas.user import UserCreate
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