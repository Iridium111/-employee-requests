from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from sqlalchemy import select


class DepartmentRepository:
    @staticmethod
    async def get_all(
            session: AsyncSession
    ):
        stmt = select(Department)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def find_by_id(
            session: AsyncSession,
            department_id: int
    ):
        stmt = select(Department).where(Department.id == department_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create(
            session: AsyncSession,
            department_data: DepartmentCreate
    ):
        db_department = Department(**department_data.model_dump())
        session.add(db_department)

        await session.commit()
        await session.refresh(db_department)
        return db_department

    @staticmethod
    async def delete(
            session: AsyncSession,
            db_department: Department
    ):
        await session.delete(db_department)
        await session.commit()
        return db_department

    @staticmethod
    async def update(
            session: AsyncSession,
            department_data: DepartmentUpdate,
            db_department: Department
    ):
        update_data = department_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_department, key, value)

        await session.commit()
        await session.refresh(db_department)
        return db_department

