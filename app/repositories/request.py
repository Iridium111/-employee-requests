from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request import Request

from sqlalchemy import select


class RequestRepository:
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
        stmt = select(Request).where(Request.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()




