from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repositories.department import DepartmentRepository
from app.schemas.department import DepartmentResponse, DepartmentCreate, DepartmentUpdate

router = APIRouter(prefix='/departments', tags=['Department'])

@router.get('/',
           response_model=list[DepartmentResponse],
           status_code=200)
async def get_departments(
        session: AsyncSession = Depends(get_async_session)
):
  return await DepartmentRepository.get_all(session)

@router.post('/',
             response_model=DepartmentResponse,
             status_code=201)
async def create_department(
        department_data: DepartmentCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await DepartmentRepository.create(session, department_data)

@router.patch('/{department_id}',
             response_model=DepartmentResponse,
             status_code=200)
async def update_department(
        department_id: int,
        department_data: DepartmentUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    db_department = await DepartmentRepository.find_by_id(session, department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail='Department not found.')

    return await DepartmentRepository.update(session, department_data, db_department)


@router.delete('/{department_id}',
               response_model=DepartmentResponse,
               status_code=200)
async def delete_department(
        department_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    db_department = await DepartmentRepository.find_by_id(session, department_id)

    if db_department is None:
        raise HTTPException(status_code=404, detail='Department not found.')

    return await DepartmentRepository.delete(session, db_department)



