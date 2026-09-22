from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repositories.employee import EmployeeRepository
from app.repositories.request import RequestRepository
from app.schemas.request import RequestResponse, RequestChangeStatus, RequestCreate
from app.services.request_service import RequestService

router = APIRouter(prefix="/requests", tags=["Requests"])

@router.post("/",
             response_model=RequestResponse,
             status_code=200)
async def create_request(
        request_data: RequestCreate,
        session: AsyncSession = Depends(get_async_session)
):
    author_id = request_data.author_id
    db_author = await EmployeeRepository.get_by_id(session, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found.")

    executor_id = request_data.executor_id
    db_executor = await EmployeeRepository.get_by_id(session, executor_id)
    if not db_executor:
        raise HTTPException(status_code=404, detail="Executor not found.")

    return await RequestRepository.create(session, request_data)

@router.patch("/{request_id}/status",
             response_model=RequestResponse,
             status_code=200)
async def change_status(
        request_id: int,
        request_data: RequestChangeStatus,
        session: AsyncSession = Depends(get_async_session)
):
    db_request = await RequestRepository.find_by_id(session, request_id)

    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    try:
        RequestService.change_status(db_request, request_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await RequestRepository.save_changes(session, db_request)
    return db_request