from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repositories.department import DepartmentRepository
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeResponse, EmployeeCreate, EmployeeUpdate

router = APIRouter(prefix='/employees', tags=['Employee'])

@router.get('/',
            response_model=list[EmployeeResponse],
            status_code=200)
async def get_employees(
        session: AsyncSession = Depends(get_async_session)
):
    return await EmployeeRepository.get_all(session=session)

@router.post('/',
             response_model=EmployeeResponse,
             status_code=201)
async def create_employee(
        employee_data: EmployeeCreate,
        session: AsyncSession = Depends(get_async_session)
):
    department_id = employee_data.department_id
    db_department = await DepartmentRepository.find_by_id(session=session,
                                                          department_id=department_id)
    if not db_department:
        raise HTTPException(status_code=404,
                            detail='Department not found.')

    return await EmployeeRepository.create_employee(session=session,
                                                    employee_data=employee_data)

@router.patch('/{employee_id}',
              response_model=EmployeeResponse,
              status_code=200)
async def update_employee(
        employee_id: int,
        employee_data: EmployeeUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    db_employee = await EmployeeRepository.get_by_id(session=session,
                                                     employee_id=employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail='Employee not found.')

    update_data = employee_data.model_dump(exclude_unset=True)
    if "department_id" in update_data:
        department_id = update_data["department_id"]
        db_department = await DepartmentRepository.find_by_id(session, department_id)
        if not db_department:
            raise HTTPException(status_code=404, detail='Department not found.')

    return await EmployeeRepository.update_employee(session=session,
                                                    employee_data=employee_data,
                                                    db_employee=db_employee)

@router.delete('/{employee_id}',
               response_model=EmployeeResponse,
               status_code=200)
async def delete_employee(
        employee_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    db_employee = await EmployeeRepository.get_by_id(session=session,
                                                     employee_id=employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail='Employee not found.')

    return await EmployeeRepository.delete_employee(session=session,
                                                    db_employee=db_employee)
