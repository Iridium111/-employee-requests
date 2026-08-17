from sqlalchemy.ext.asyncio import AsyncSession


class RequestRepository:
    @staticmethod
    async def save_changes(
            session: AsyncSession,
            request,
    ):
        await session.commit()
        await session.refresh(request)

        return request



