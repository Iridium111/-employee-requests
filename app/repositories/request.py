from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from collections.abc import Sequence

from app.models.employee import Employee
from app.models.request import Request
from app.schemas.request import RequestCreate, RequestUpdate


class RequestRepository:
    @staticmethod
    async def create(
            session: AsyncSession,
            request_data: RequestCreate
    ) -> Request | None:
        db_request = Request(**request_data.model_dump())
        session.add(db_request)

        await session.flush()
        db_request.number = f'REQ-{db_request.id:03d}'

        await session.commit()
        return await RequestRepository.find_by_id(session, db_request.id)

    @staticmethod
    async def save_changes(
            session: AsyncSession,
            request,
    ) -> Request:
        await session.commit()
        await session.refresh(request)

        return request

    @staticmethod
    async def find_by_id(
            session: AsyncSession,
            id: int
    ) -> Request | None:
        stmt = (select(Request)
                .where(Request.id == id)
                .options(selectinload(Request.author).selectinload(Employee.department),
                         selectinload(Request.executor).selectinload(Employee.department)))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
            session: AsyncSession
    ) -> Sequence[Request]:
        stmt = (select(Request)
                .options(selectinload(Request.author).selectinload(Employee.department),
                         selectinload(Request.executor).selectinload(Employee.department)))
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_request(
            session: AsyncSession,
            request_data: RequestUpdate,
            db_request: Request
    ) -> Request:
        update_data = request_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_request, key, value)

        await session.commit()
        await session.refresh(db_request)
        return db_request

    @staticmethod
    async def delete_request(
            session: AsyncSession,
            db_request: Request
    ) -> Request:
        await session.delete(db_request)
        await session.commit()

        return db_request




