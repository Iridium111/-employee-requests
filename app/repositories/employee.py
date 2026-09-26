from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.employee import Employee
from sqlalchemy import select
from collections.abc import Sequence

from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository:
    @staticmethod
    async def get_all(
            session: AsyncSession
    ) -> Sequence[Employee]:
        stmt = (select(Employee)
                .options(selectinload(Employee.department)))
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(
            session: AsyncSession,
            employee_id: int,
    ) -> Employee | None:
        stmt = (select(Employee)
                .where(Employee.id == employee_id)
                .options(selectinload(Employee.department)))
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def create_employee(
            session: AsyncSession,
            employee_data: EmployeeCreate,
    ) -> Employee | None:
        db_employee = Employee(**employee_data.model_dump())
        session.add(db_employee)

        await session.commit()
        await session.refresh(db_employee)
        return await EmployeeRepository.get_by_id(session, db_employee.id)

    @staticmethod
    async def update_employee(
            session: AsyncSession,
            employee_data: EmployeeUpdate,
            db_employee: Employee,
    ) -> Employee | None:
        update_data = employee_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_employee, key, value)

        await session.commit()
        await session.refresh(db_employee)
        return await EmployeeRepository.get_by_id(session, db_employee.id)

    @staticmethod
    async def delete_employee(
            session: AsyncSession,
            db_employee: Employee
    ) -> Employee:
        await session.delete(db_employee)
        await session.commit()

        return db_employee





