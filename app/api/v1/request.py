from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repositories.employee import EmployeeRepository
from app.repositories.request import RequestRepository
from app.schemas.request import RequestResponse, RequestChangeStatus, RequestCreate, RequestUpdate
from app.services.request_service import RequestService

router = APIRouter(prefix="/requests", tags=["Requests"])

@router.get("/",
            response_model=list[RequestResponse],
            status_code=200)
async def get_requests(
        session: AsyncSession = Depends(get_async_session)
):
    return  await RequestRepository.get_all(session=session)

@router.post("/",
             response_model=RequestResponse,
             status_code=201)
async def create_request(
        request_data: RequestCreate,
        session: AsyncSession = Depends(get_async_session)
):
    author_id = request_data.author_id
    db_author = await EmployeeRepository.get_by_id(session, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found.")

    executor_id = request_data.executor_id
    db_executor = await EmployeeRepository.get_by_id(session=session, employee_id=executor_id)
    if not db_executor:
        raise HTTPException(status_code=404, detail="Executor not found.")

    return await RequestRepository.create(session=session, request_data=request_data)

@router.patch("/{request_id}/status",
             response_model=RequestResponse,
             status_code=200)
async def change_status(
        request_id: int,
        request_data: RequestChangeStatus,
        session: AsyncSession = Depends(get_async_session)
):
    db_request = await RequestRepository.find_by_id(session=session, id=request_id)

    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found.")

    try:
        RequestService.change_status(request=db_request, new_status=request_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await RequestRepository.save_changes(session=session, request=db_request)
    return db_request
@router.patch("/{request_id}",
              response_model=RequestResponse,
              status_code=200)
async def update_request(
        request_id: int,
        request_data: RequestUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    db_request = await RequestRepository.find_by_id(session=session, id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found.")

    update_request = request_data.model_dump(exclude_unset=True)
    if "executor_id" in update_request:
        executor_id = update_request["executor_id"]
        db_executor = await EmployeeRepository.get_by_id(session, executor_id)
        if not db_executor:
            raise HTTPException(status_code=404, detail="Executor not found.")

    return await RequestRepository.update_request(session=session,
                                                  request_data=request_data,
                                                  db_request=db_request)

@router.delete("/{request_id}",
               response_model=RequestResponse,
               status_code=200)
async def delete_request(
        request_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    db_request = await RequestRepository.find_by_id(session=session, id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found.")

    return await RequestRepository.delete_request(session=session,
                                            db_request=db_request)