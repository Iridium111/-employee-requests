from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    @staticmethod
    async def create(session: AsyncSession,
               user_data: UserCreate,
                hashed_password: str) -> User:
        user_dict = user_data.model_dump(exclude={"password"})
        data_user = User(**user_dict,
                         hashed_password=hashed_password)

        session.add(data_user)
        await session.commit()
        await session.refresh(data_user)
        return data_user

    @staticmethod
    async def get_by_uuid(session: AsyncSession,
                        user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_login(session: AsyncSession,
                           login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(session: AsyncSession,
                           email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_employee_id(session: AsyncSession,
                                 employee_id: int) -> User | None:
        stmt = select(User).where(User.employee_id == employee_id)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

