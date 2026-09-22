from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.models.request import Request
from app.schemas.request import RequestCreate


class RequestRepository:
    @staticmethod
    async def create(
            session: AsyncSession,
            request_data: RequestCreate
    ):
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
    ):
        await session.commit()
        await session.refresh(request)

        return request

    @staticmethod
    async def find_by_id(session: AsyncSession, id: int) -> Request | None:
        stmt = (select(Request)
                .where(Request.id == id)
                .options(selectinload(Request.author),
                         selectinload(Request.executor)))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()




