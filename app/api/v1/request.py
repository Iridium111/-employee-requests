from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repositories.request import RequestRepository
from app.schemas.request import RequestResponse, RequestChangeStatus
from app.services.request_service import RequestService

router = APIRouter(prefix="/requests", tags=["Requests"])

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